#!/usr/bin/env python3
"""Synchronize Poland's senior men's fixtures from PZPS and CEV (stdlib only)."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

SOURCE = "https://www-old.cev.eu/Competition-Area/CompetitionView.aspx?CID=12862&ID=1572&PID=2990"
PZPS = "https://www.pzps.pl/strapi/api/events"
CATEGORY = "VOLLEYBALL/NATIONAL-TEAMS/MEN"
DATA = Path("data")
SITE = Path("site")
MATCH = re.compile(r'<span id="([^"]+)_LB_FederationMatchNumber"[^>]*>(.*?)</span>', re.S)
TAG = re.compile(r"<[^>]*>")
TIME = re.compile(r"^\s*(\d{2})/(\d{2})/(\d{4})\s+(\d{2}):(\d{2})\s*$")
ZONE_BY_CITY = {
    "SOFIA": ("Sofia, Bułgaria", "Europe/Sofia"),
    "TAMPERE": ("Tampere, Finlandia", "Europe/Helsinki"),
    "CLUJ-NAPOCA": ("Kluż-Napoka, Rumunia", "Europe/Bucharest"),
    "NAPOLI": ("Neapol, Włochy", "Europe/Rome"),
    "MODENA": ("Modena, Włochy", "Europe/Rome"),
    "TORINO": ("Turyn, Włochy", "Europe/Rome"),
    "MILANO": ("Mediolan, Włochy", "Europe/Rome"),
    "ASSAGO": ("Assago, Włochy", "Europe/Rome"),
}
TEAMS = {
    "POLAND": "Polska", "ISRAEL": "Izrael", "NORTH MACEDONIA": "Macedonia Północna",
    "PORTUGAL": "Portugalia", "UKRAINE": "Ukraina", "BULGARIA": "Bułgaria",
    "ITALY": "Włochy", "GERMANY": "Niemcy", "FRANCE": "Francja",
    "FINLAND": "Finlandia", "ROMANIA": "Rumunia", "SLOVENIA": "Słowenia",
    "SERBIA": "Serbia", "CZECHIA": "Czechy", "SWEDEN": "Szwecja",
    "GREECE": "Grecja", "DENMARK": "Dania", "ESTONIA": "Estonia",
    "SLOVAKIA": "Słowacja", "LATVIA": "Łotwa", "SWITZERLAND": "Szwajcaria",
    "THE NETHERLANDS": "Holandia", "TÜRKIYE": "Turcja",
}
STAGES = {"MEF": "1/8 finału", "MQF": "ćwierćfinał", "MSF": "półfinał", "MFF": "mecz medalowy"}


def plain(markup: str) -> str:
    return " ".join(html.unescape(TAG.sub(" ", markup)).split())


def field(chunk: str, prefix: str, suffix: str) -> str:
    found = re.search(r'<span id="' + re.escape(prefix + suffix) + r'"[^>]*>(.*?)</span>', chunk, re.S)
    return plain(found.group(1)) if found else ""


def parse_fixtures(page: str) -> tuple[list[dict], int]:
    markers = list(MATCH.finditer(page))
    if len(markers) < 60:  # A valid CEV 2026 page has 60 group games alone.
        raise ValueError(f"Niepełny terminarz CEV: odczytano tylko {len(markers)} pozycji")
    found: list[dict] = []
    waiting = 0
    for index, marker in enumerate(markers):
        prefix, code = marker.group(1), plain(marker.group(2))
        chunk = page[marker.end():markers[index + 1].start() if index + 1 < len(markers) else marker.end() + 12000]
        # Constrain extraction to the row; embedded referee tables do not contain these IDs.
        home = field(chunk, prefix, "_Label2").upper()
        away = field(chunk, prefix, "_Label4").upper()
        if "POLAND" not in (home, away):
            continue  # Never publish possible bracket positions as actual fixtures.
        link = re.search(r"MatchPage\.aspx\?mID=(\d+)&amp;ID=|MatchPage\.aspx\?mID=(\d+)&ID=", chunk)
        if not link:
            raise ValueError(f"Brak stałego identyfikatora meczu: {code}")
        match_id = link.group(1) or link.group(2)
        date_text = field(chunk, prefix, "_LB_DataOra")
        venue = field(chunk, prefix, "_LB_Palasport")
        if not TIME.match(date_text) or not venue:
            waiting += 1
            continue
        city = next((city for city in sorted(ZONE_BY_CITY, key=len, reverse=True) if venue.upper().endswith(city)), None)
        if not city:
            raise ValueError(f"Nieznana strefa dla miejsca meczu {code}: {venue}")
        city_label, zone = ZONE_BY_CITY[city]
        day, month, year, hour, minute = map(int, TIME.match(date_text).groups())
        local = datetime(year, month, day, hour, minute, tzinfo=ZoneInfo(zone))
        start = local.astimezone(timezone.utc)
        stage = "faza grupowa, grupa " + code[2] if code.startswith("MF") and code[2] in "ABCD" else STAGES.get(code[:3], "faza pucharowa")
        home_pl, away_pl = TEAMS.get(home, home.title()), TEAMS.get(away, away.title())
        found.append({
            "id": match_id, "code": code, "start_utc": start.isoformat().replace("+00:00", "Z"),
            "title": f"{home_pl} – {away_pl} | ME 2026", "stage": stage,
            "location": f"{venue[: -len(city)].strip().rstrip(',')}, {city_label}",
            "url": f"https://www-old.cev.eu/Competition-Area/MatchPage.aspx?mID={match_id}&ID=1572",
        })
    if not found:
        raise ValueError("CEV nie zwrócił żadnego potwierdzonego meczu Polski")
    if len({event["id"] for event in found}) != len(found):
        raise ValueError("CEV zwrócił zduplikowane identyfikatory meczu")
    return sorted(found, key=lambda item: (item["start_utc"], item["id"])), waiting


def fetch(url: str = SOURCE) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "PolandVolleyballCalendar/2.0 (personal calendar)", "Accept": "application/json,text/html"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=35) as response:
                content = response.read(3_000_001)
                if len(content) > 3_000_000:
                    raise ValueError("Odpowiedź źródła przekracza dopuszczalny rozmiar")
                return content.decode("utf-8-sig", errors="replace")
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == 2:
                raise RuntimeError(f"Błąd pobierania {urllib.parse.urlsplit(url).hostname}: {exc}") from exc
            time.sleep(2 ** attempt)
    raise AssertionError("unreachable")


def polish_wall_time(value: str) -> datetime:
    # PZPS's public calendar renders startsAt.split('T')[1] directly (getStartTime).
    # Its trailing Z is a storage convention, NOT UTC: e.g. 2026-09-13T18:00Z
    # means 18:00 Warsaw, matching CEV's 19:00 Sofia. Never convert it twice.
    local = datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    zone = ZoneInfo("Europe/Warsaw")
    candidates = {local.replace(tzinfo=zone, fold=fold).astimezone(timezone.utc)
                  for fold in (0, 1)
                  if local.replace(tzinfo=zone, fold=fold).astimezone(timezone.utc)
                  .astimezone(zone).replace(tzinfo=None) == local}
    if len(candidates) != 1:
        raise ValueError(f"Niejednoznaczna lub nieistniejąca godzina PZPS: {value}")
    return candidates.pop()


def parse_pzps(payload: dict, year: int) -> tuple[list[dict], int]:
    data = payload.get("data")
    if not isinstance(data, dict) or not all(isinstance(data.get(k), list) for k in ("matches", "events")):
        raise ValueError("Nieprawidłowa struktura kalendarium PZPS")
    if len(data["events"]) >= 100 or len(data["matches"]) >= 100:
        raise ValueError("Możliwe obcięcie odpowiedzi PZPS (limit 100)")
    # The flat list omits some last matches. Include tournament children as well.
    rows = {str(m["id"]): m for m in data["matches"]}
    for tournament in data["events"]:
        for match in tournament.get("matches", []):
            rows.setdefault(str(match["id"]), match)
    fixtures, waiting = [], 0
    for match in rows.values():
        if ((match.get("category") or {}).get("categoryType") != CATEGORY
                or match.get("_softDeletedAt") or not match.get("publishedAt")):
            continue
        title = plain(match.get("title") or "")
        # Category includes other countries' games in tournaments held in Poland.
        sides = re.split(r"\s*[-–—]\s*", title.split("|")[-1].strip())
        if len(sides) != 2 or not any(s.casefold() == "polska" for s in sides):
            continue
        if any(not s or re.search(r"\b(tbd|zwycięzca|przegrany|\d+[a-z])\b|\?", s, re.I) for s in sides):
            waiting += 1
            continue
        value = match.get("startsAt")
        if not value:
            waiting += 1
            continue
        if not year <= int(value[:4]) <= year + 1:
            continue
        competition = plain(match.get("tournamentTitle") or "Mecz reprezentacji Polski")
        url = match.get("otherLinkLink") or "https://www.pzps.pl/pl/kalendarium"
        if urllib.parse.urlsplit(url).scheme not in ("https", "http"):
            url = "https://www.pzps.pl/pl/kalendarium"
        cev_id = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query).get("mID", [None])[0]
        is_cev_2026 = (urllib.parse.urlsplit(url).hostname == "www-old.cev.eu"
                       and "2026" in competition and "EuroVolley" in competition and cev_id)
        event_id = cev_id if is_cev_2026 else "pzps-" + str(match["id"])
        item = {"id": event_id, "pzps_id": str(match["id"]), "code": "PZPS-" + str(match["id"]),
                "title": " – ".join(sides) + " | " + competition,
                "competition": competition, "stage": title.split("|")[0].strip() if "|" in title else "",
                "location": plain(match.get("place") or "Miejsce do potwierdzenia"), "url": url}
        if match.get("isStartHourHidden") is True:
            # Publish a known date without inventing a kick-off time.
            item["start_date"] = value[:10]
            waiting += 1
        else:
            item["start_utc"] = polish_wall_time(value).isoformat().replace("+00:00", "Z")
        fixtures.append(item)
    return fixtures, waiting


def fetch_pzps(year: int) -> tuple[list[dict], int]:
    urls = []
    for y in (year, year + 1):
        for month in (1, 4, 7, 10):
            end = f"{y + 1}-01-01" if month == 10 else f"{y}-{month + 3:02d}-01"
            params = {"pagination[limit]": 100, "locale": "pl-PL", "category": CATEGORY,
                      "start": f"{y}-{month:02d}-01T00:00:00.000Z", "end": end + "T00:00:00.000Z"}
            urls.append(PZPS + "?" + urllib.parse.urlencode(params))
    merged = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for page in pool.map(fetch, urls):
            fixtures, _ = parse_pzps(json.loads(page), year)
            for item in fixtures:
                merged[item["id"]] = item
    return list(merged.values()), sum("start_date" in item for item in merged.values())


def identity_match(item: dict, candidates: dict) -> dict | None:
    if item["id"] in candidates:
        return candidates[item["id"]]
    if item.get("pzps_id"):
        found = [v for v in candidates.values() if v.get("pzps_id") == item["pzps_id"]]
        if len(found) == 1:
            return found[0]
    # Some PZPS rows link to the tournament instead of the individual CEV match.
    # Only coalesce this known competition, same opponents and same Polish date.
    def signature(event):
        comp = event.get("competition", "CEV Mistrzostwa Europy 2026" if event["id"].isdigit() else "")
        if "2026" not in comp or not ("EuroVolley" in comp or "Mistrzostwa Europy" in comp):
            return None
        date = event.get("start_date")
        if not date:
            date = datetime.fromisoformat(event["start_utc"].replace("Z", "+00:00")).astimezone(ZoneInfo("Europe/Warsaw")).date().isoformat()
        teams = tuple(sorted(s.strip().casefold() for s in re.split(r"[-–—]", event["title"].split("|")[0])))
        return date, teams
    key = signature(item)
    found = [v for v in candidates.values() if key and signature(v) == key]
    return found[0] if len(found) == 1 else None


def read_json(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def save_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ics_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace(";", "\\;").replace(",", "\\,")


def fold(line: str) -> str:
    # RFC 5545: physical lines limited to 75 octets, continuation starts with SP.
    lines, current = [], ""
    for char in line:
        if len((current + char).encode("utf-8")) > 75:
            lines.append(current)
            current = " " + char
        else:
            current += char
    return "\r\n".join(lines + [current])


def render_ics(events: list[dict]) -> bytes:
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Polska Siatkowka//Mecze seniorow//PL", "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:Polska siatkówka – seniorzy", "X-WR-TIMEZONE:Europe/Warsaw", "REFRESH-INTERVAL;VALUE=DURATION:P1D", "X-PUBLISHED-TTL:P1D"]
    lines.append("X-WR-CALDESC:Kalendarz wygenerowany z pomocą AI (ChatGPT). Terminy z PZPS i CEV.")
    for event in events:
        modified = datetime.fromisoformat(event["modified_utc"].replace("Z", "+00:00"))
        fmt = lambda dt: dt.strftime("%Y%m%dT%H%M%SZ")
        uid = (f"{event['id']}@polska-siatkowka" if event['id'].startswith("pzps-")
               else f"cev-eurovolley-2026-men-{event['id']}@polska-siatkowka")
        if "start_date" in event:
            start = datetime.fromisoformat(event["start_date"])
            dates = [f"DTSTART;VALUE=DATE:{start:%Y%m%d}", f"DTEND;VALUE=DATE:{start + timedelta(days=1):%Y%m%d}"]
            time_note = "Godzina rozpoczęcia do potwierdzenia."
        else:
            start = datetime.fromisoformat(event["start_utc"].replace("Z", "+00:00"))
            dates = [f"DTSTART:{fmt(start)}", f"DTEND:{fmt(start + timedelta(hours=3))}"]
            time_note = "Godzina w Polsce: " + start.astimezone(ZoneInfo("Europe/Warsaw")).strftime("%d.%m.%Y %H:%M") + ". Czas trwania wpisu: szacunkowe 3 godziny."
        description = "Reprezentacja Polski seniorów (mężczyźni). " + event.get("competition", "CEV Mistrzostwa Europy 2026")
        if event.get("stage"):
            description += ", " + event["stage"]
        description += ". " + time_note
        lines.extend([
            "BEGIN:VEVENT", f"UID:{uid}", f"SEQUENCE:{event['sequence']}",
            f"DTSTAMP:{fmt(modified)}", f"LAST-MODIFIED:{fmt(modified)}", *dates,
            f"SUMMARY:{ics_escape(event['title'])}",
            f"LOCATION:{ics_escape(event['location'])}",
            f"DESCRIPTION:{ics_escape(description)}",
            f"URL:{event['url']}", "END:VEVENT",
        ])
    lines.append("END:VCALENDAR")
    return ("\r\n".join(fold(line) for line in lines) + "\r\n").encode("utf-8")


def update(page: str | None = None, pzps_payload: dict | None = None) -> dict:
    DATA.mkdir(exist_ok=True)
    SITE.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    old = read_json(DATA / "matches.json", [])
    previous = {event["id"]: event for event in old}
    status = read_json(DATA / "status.json", {})
    entry = {"checked_at_utc": now, "result": "ok", "added": [], "updated": [], "confirmed_in_source": 0, "awaiting_schedule": 0, "sources": {}}
    year = datetime.now(ZoneInfo("Europe/Warsaw")).year
    collected = {}
    for name, loader in [
        ("PZPS", lambda: parse_pzps(pzps_payload, year) if pzps_payload is not None else fetch_pzps(year)),
        *([("CEV ME 2026", lambda: parse_fixtures(page if page is not None else fetch()))] if year <= 2026 or page is not None else []),
    ]:
        try:
            fixtures, waiting = loader()
            entry["sources"][name] = {"result": "ok", "matches": len(fixtures), "awaiting_schedule": waiting}
            entry["awaiting_schedule"] += waiting
            for item in fixtures:
                item = dict(item)
                if name.startswith("CEV"):
                    item["competition"] = "CEV Mistrzostwa Europy 2026"
                former = identity_match(item, previous)
                if former:
                    item["id"] = former["id"]
                    if former.get("pzps_id"):
                        item.setdefault("pzps_id", former["pzps_id"])
                peer = identity_match(item, collected)
                if peer:
                    collected.pop(peer["id"])
                    item = {**peer, **item}
                # CEV has venue-local times, exact halls and stages; prefer those.
                item = {**collected.get(item["id"], {}), **item}
                if "start_utc" in item:
                    item.pop("start_date", None)
                collected[item["id"]] = item
        except Exception as exc:
            entry["sources"][name] = {"result": "error", "error": str(exc)}
    errors = [name + ": " + value["error"] for name, value in entry["sources"].items() if value["result"] == "error"]
    if errors:
        entry["result"] = "partial" if any(v["result"] == "ok" for v in entry["sources"].values()) else "error"
        entry["error"] = " | ".join(errors)
    try:
        if entry["result"] == "error":
            raise ValueError(entry["error"])
        entry["confirmed_in_source"] = len(collected)
        merged = dict(previous)
        for item in collected.values():
            former = previous.get(item["id"])
            if former is None and item.get("pzps_id"):
                former = next((v for v in previous.values() if v.get("pzps_id") == item["pzps_id"]), None)
                if former:
                    item["id"] = former["id"]  # Preserve UID if a CEV link appears later.
            if former is None:
                item["sequence"], item["modified_utc"] = 0, now
                entry["added"].append(item["code"])
            elif any(former.get(key) != value for key, value in item.items()):
                item["sequence"], item["modified_utc"] = former["sequence"] + 1, now
                entry["updated"].append(item["code"])
            else:
                item["sequence"], item["modified_utc"] = former["sequence"], former["modified_utc"]
            merged[item["id"]] = item
        all_events = sorted(merged.values(), key=lambda x: (x.get("start_utc", x.get("start_date", "")), x["id"]))
        # No event is removed merely because a source has a temporary omission.
        calendar = render_ics(all_events)
        save_json(DATA / "matches.json", all_events)
        (SITE / "calendar.ics").write_bytes(calendar)
        if entry["result"] == "ok":
            status["last_success_utc"] = now
        status["match_count"] = len(all_events)
    except Exception as exc:
        entry["result"], entry["error"] = "error", str(exc)
    if entry.get("error"):
        status["last_error"] = entry["error"]
    else:
        status.pop("last_error", None)
    status["sources"] = entry["sources"]
    status["last_run_utc"], status["last_result"] = now, entry["result"]
    status["last_added"], status["last_updated"] = entry["added"], entry["updated"]
    save_json(DATA / "status.json", status)
    with (DATA / "history.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False) + "\n")
    history = [json.loads(line) for line in (DATA / "history.jsonl").read_text(encoding="utf-8").splitlines()[-90:]]
    save_json(SITE / "status.json", status)
    save_json(SITE / "history.json", list(reversed(history)))
    print(json.dumps(entry, ensure_ascii=False))
    return entry


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", help="Local CEV HTML fixture for testing")
    parser.add_argument("--pzps-fixture", help="Local PZPS JSON fixture for testing")
    args = parser.parse_args()
    outcome = update(Path(args.fixture).read_text(encoding="utf-8-sig") if args.fixture else None,
                     read_json(Path(args.pzps_fixture), {}) if args.pzps_fixture else None)
    sys.exit(0 if outcome["result"] == "ok" else 1)
