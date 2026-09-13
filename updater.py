#!/usr/bin/env python3
"""Synchronize confirmed Poland men's EuroVolley 2026 fixtures from CEV."""

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
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

SOURCE = "https://www-old.cev.eu/Competition-Area/CompetitionView.aspx?CID=12862&ID=1572&PID=2990"
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


def fetch() -> str:
    request = urllib.request.Request(SOURCE, headers={"User-Agent": "PolandVolleyballCalendar/1.0 (personal calendar)", "Accept": "text/html"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=35) as response:
                content = response.read(3_000_001)
                if len(content) > 3_000_000:
                    raise ValueError("Odpowiedź CEV przekracza dopuszczalny rozmiar")
                return content.decode("utf-8-sig", errors="replace")
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == 2:
                raise RuntimeError(f"Błąd pobierania CEV: {exc}") from exc
            time.sleep(2 ** attempt)
    raise AssertionError("unreachable")


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
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Polska Siatkowka//Mecze seniorow CEV//PL", "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:Polska siatkówka – seniorzy (ME 2026)", "X-WR-TIMEZONE:Europe/Warsaw", "REFRESH-INTERVAL;VALUE=DURATION:P1D", "X-PUBLISHED-TTL:P1D"]
    for event in events:
        start = datetime.fromisoformat(event["start_utc"].replace("Z", "+00:00"))
        modified = datetime.fromisoformat(event["modified_utc"].replace("Z", "+00:00"))
        fmt = lambda dt: dt.strftime("%Y%m%dT%H%M%SZ")
        lines.extend([
            "BEGIN:VEVENT", f"UID:cev-eurovolley-2026-men-{event['id']}@polska-siatkowka", f"SEQUENCE:{event['sequence']}",
            f"DTSTAMP:{fmt(modified)}", f"LAST-MODIFIED:{fmt(modified)}", f"DTSTART:{fmt(start)}",
            f"DTEND:{fmt(start + timedelta(hours=3))}", f"SUMMARY:{ics_escape(event['title'])}",
            f"LOCATION:{ics_escape(event['location'])}",
            f"DESCRIPTION:{ics_escape('Reprezentacja Polski seniorów (mężczyźni). CEV Mistrzostwa Europy 2026, ' + event['stage'] + '. Godzina rozpoczęcia meczu.')}",
            f"URL:{event['url']}", "END:VEVENT",
        ])
    lines.append("END:VCALENDAR")
    return ("\r\n".join(fold(line) for line in lines) + "\r\n").encode("utf-8")


def update(page: str | None = None) -> dict:
    DATA.mkdir(exist_ok=True)
    SITE.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    old = read_json(DATA / "matches.json", [])
    previous = {event["id"]: event for event in old}
    status = read_json(DATA / "status.json", {})
    entry = {"checked_at_utc": now, "result": "ok", "added": [], "updated": [], "confirmed_in_source": 0, "awaiting_schedule": 0}
    try:
        fixtures, waiting = parse_fixtures(page if page is not None else fetch())
        entry["confirmed_in_source"], entry["awaiting_schedule"] = len(fixtures), waiting
        merged = dict(previous)
        for item in fixtures:
            former = previous.get(item["id"])
            if former is None:
                item["sequence"], item["modified_utc"] = 0, now
                entry["added"].append(item["code"])
            elif any(former.get(key) != value for key, value in item.items()):
                item["sequence"], item["modified_utc"] = former["sequence"] + 1, now
                entry["updated"].append(item["code"])
            else:
                item["sequence"], item["modified_utc"] = former["sequence"], former["modified_utc"]
            merged[item["id"]] = item
        all_events = sorted(merged.values(), key=lambda x: (x["start_utc"], x["id"]))
        # No event is removed merely because CEV has a temporary omission.
        save_json(DATA / "matches.json", all_events)
        (SITE / "calendar.ics").write_bytes(render_ics(all_events))
        status["last_success_utc"] = now
        status["match_count"] = len(all_events)
    except Exception as exc:
        entry["result"], entry["error"] = "error", str(exc)
        status["last_error"] = str(exc)
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
    args = parser.parse_args()
    outcome = update(Path(args.fixture).read_text(encoding="utf-8-sig") if args.fixture else None)
    sys.exit(0 if outcome["result"] == "ok" else 1)
