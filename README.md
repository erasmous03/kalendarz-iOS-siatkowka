# Subskrybowany kalendarz polskiej reprezentacji siatkarzy

**iOS · Android · Google Calendar · Apple Calendar · Outlook · ICS**

Kalendarz i kod projektu zostały wygenerowane z pomocą **AI (ChatGPT)**. Terminy pochodzą z oficjalnych danych PZPS i CEV. Jest to niezależny projekt kibicowski.

Mecze seniorskiej reprezentacji Polski mężczyzn w siatkówce halowej, we wszystkich rozgrywkach publikowanych w [kalendarium PZPS](https://www.pzps.pl/pl/kalendarium): VNL, ME, MŚ, igrzyska, kwalifikacje, turnieje i mecze towarzyskie. Filtr obejmuje wyłącznie kategorię `VOLLEYBALL/NATIONAL-TEAMS/MEN` i spotkania z udziałem Polski. Nie ma ograniczenia do nazwy turnieju ani sezonu 2026.

## Aktualizacja działającego projektu

Zastąp `updater.py`, `site/index.html` i `README.md`. Zachowaj istniejące foldery `data`, pliki JSON/ICS w `site` oraz workflow. Paczka aktualizacyjna zawiera wyłącznie te trzy zmienione pliki i nie zawiera plików ukrytych.

Zmiana `updater.py` w gałęzi `main` uruchomi istniejące zadanie. Poczekaj na zakończenie w Actions. Adres kalendarza pozostaje taki sam:

https://erasmous03.github.io/kalendarz-iOS-siatkowka/calendar.ics

Przy zachowaniu nazwy repozytorium istniejącej subskrypcji nie trzeba dodawać ponownie. Zmiany pojawią się po odświeżeniu przez dostawcę kalendarza. Stary workflow może nadal wyświetlać słowo „CEV” w nazwie kroku lub commita — uruchamia nowy skrypt sprawdzający oba źródła.

## Nazwa i opis repozytorium

Docelowa nazwa: `kalendarz-siatkowka-polska`.

W ustawieniach repozytorium wybierz **Settings → General → Repository name**, wpisz tę nazwę i kliknij **Rename**. Następnie na głównej stronie repozytorium kliknij koło zębate przy **About** i wklej opis:

> Subskrybowany kalendarz meczów reprezentacji Polski mężczyzn w siatkówce. iOS, Android, Google Calendar i Outlook. Codzienne aktualizacje i logi. Projekt wygenerowany z pomocą AI.

Po zmianie nazwy uruchom **Actions → Aktualizuj kalendarz reprezentacji → Run workflow**. Po zakończeniu publikacji docelowa strona będzie pod adresem:

https://erasmous03.github.io/kalendarz-siatkowka-polska/

Nowy adres subskrypcji:

https://erasmous03.github.io/kalendarz-siatkowka-polska/calendar.ics

Wpisz adres strony także w polu **Website** przy **About**. Przyciski na stronie same wyliczają adres ICS na podstawie miejsca publikacji.

**Zmiana nazwy zmienia adres Pages.** GitHub przekierowuje repozytorium, ale nie stronę projektu. Po sprawdzeniu nowego adresu zmień subskrypcję na urządzeniach; jeśli aplikacja nie pozwala edytować URL, usuń starą subskrypcję i dodaj nową. [Dokumentacja GitHub](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).

## Dodawanie na urządzeniach

Wybierz subskrypcję, aby otrzymywać nowe mecze. Na opublikowanej stronie są przyciski, adres do skopiowania i pełne instrukcje.

| Urządzenie / aplikacja | Sposób dodania |
| --- | --- |
| iPhone / iPad | Przycisk Apple (webcal) albo Ustawienia → Aplikacje → Kalendarz → Konta kalendarza → Dodaj konto → Inne → Dodaj kalendarz subskrybowany; wklej HTTPS ICS. |
| Mac | Kalendarz → Plik → Nowa subskrypcja kalendarza; wklej HTTPS ICS. |
| Android / Google Calendar | Na komputerze, na tym samym koncie Google: Inne kalendarze → + → Z adresu URL. Wklej ICS. Następnie zaznacz kalendarz i włącz synchronizację w aplikacji na Androidzie. |
| Outlook / Microsoft 365 | W kalendarzu w przeglądarce: Dodaj kalendarz → Subskrybuj z internetu. Wklej ICS i zapisz. |
| Inna aplikacja obsługująca ICS | Użyj subskrypcji kalendarza internetowego iCal/ICS lub webcal, jeśli aplikacja ją obsługuje. |
| Jednorazowy import | Pobierz plik przyciskiem „Pobierz plik ICS” i zaimportuj go w aplikacji obsługującej ten format. Ta kopia nie aktualizuje się automatycznie. |

Google pozwala dodać subskrypcję z URL przez przeglądarkę na komputerze, nie w aplikacji mobilnej. Samo pobranie pliku ICS na Androida nie zastępuje subskrypcji. [Instrukcja Google](https://support.google.com/calendar/answer/37100?hl=pl&co=GENIE.Platform%3DDesktop), [instrukcja Outlook](https://support.microsoft.com/en-us/outlook/import-or-subscribe-to-a-calendar-in-outlook-com-or-outlook-on-the-web).

Odświeżaniem zmian zarządza Google, Apple lub Microsoft; nie należy oczekiwać natychmiastowej aktualizacji na urządzeniu po uruchomieniu skryptu. Import i subskrypcja tego samego kalendarza mogą powodować duplikaty.

## Zakres i źródła

- Główne źródło: publiczne API oficjalnego kalendarium PZPS, to samo, którego używa strona związku. Skrypt sprawdza bieżący oraz następny rok w ośmiu kwartalnych zapytaniach. Rok zmienia się automatycznie według `Europe/Warsaw`.
- Uzupełnienie do końca 2026 roku: [terminarz CEV ME 2026](https://www-old.cev.eu/Competition-Area/CompetitionView.aspx?CID=12862&ID=1572&PID=2990), zapewniający dokładne hale, etapy i lokalne godziny tych spotkań.
- Pobierane są zarówno mecze samodzielne, jak i mecze wewnątrz turniejów PZPS, ponieważ płaska lista pomija niektóre spotkania. Stałe identyfikatory PZPS i odnośniki CEV zapobiegają duplikowaniu tych samych wydarzeń.
- Nowe turnieje nie wymagają dopisywania do kodu. Mecze muszą jednak zostać opublikowane w kalendarium PZPS. Nie jest to gwarancja kompletności terminarza związku; skrypt nie wyciąga dat z artykułów prasowych i nie zgaduje nieustalonych rywali.
- Wpisy z bieżącego sezonu obejmują także rozegrane spotkania. Znane wcześniej wydarzenia są zachowywane, również po zmianie roku. Brak meczu w odpowiedzi źródła nie jest traktowany jako odwołanie — automatyczne usuwanie lub rozpoznawanie odwołań nie jest obsługiwane.

## Godziny

CEV podaje czas lokalny hali. Skrypt stosuje odpowiednią strefę IANA, np. `Europe/Sofia`, a następnie zapisuje rzeczywistą chwilę w UTC w ICS.

PZPS stosuje inną konwencję: `startsAt` ma końcówkę `Z`, ale zawiera godzinę polską. Frontend PZPS wyświetla bezpośrednio część godzinową pola (`getStartTime`), bez przeliczenia UTC. Przykład zweryfikowany z CEV: `2026-09-13T18:00:00.000Z` w PZPS oznacza 18:00 w Warszawie, czyli 19:00 w Sofii i 16:00 UTC. Skrypt interpretuje tę wartość według `Europe/Warsaw`, z uwzględnieniem zmiany czasu. Nie przelicza jej ponownie według miejsca meczu. Zmiana tej konwencji przez PZPS będzie wymagać dostosowania parsera.

ICS zawiera UTC oraz polską godzinę w opisie. iPhone w polskiej strefie pokaże godzinę polską; podczas podróży może wyświetlać lokalny czas telefonu. Potwierdzona data bez godziny (`isStartHourHidden`) daje wpis całodniowy z wyraźną adnotacją, a ustalenie godziny aktualizuje ten sam wpis. Nieznane miejsce jest oznaczone jako „Miejsce do potwierdzenia”. Czas trwania spotkania to szacunkowe trzy godziny.

## Codzienna kontrola i logi

Istniejący GitHub Actions uruchamia skrypt codziennie o 07:23 UTC (09:23 latem, 08:23 zimą w Polsce). Można użyć również `Run workflow`. GitHub może opóźnić start, a odświeżaniem subskrypcji na telefonie zarządza Apple.

Strona pokazuje wynik każdego źródła osobno, czas ostatniej kontroli, liczbę wydarzeń oraz dodane i zmienione identyfikatory. `data/history.jsonl` zachowuje pełny dziennik, `site/history.json` ostatnie 90 wpisów, a strona pokazuje ostatnie 30. Każde uruchomienie zapisuje log także wtedy, gdy nic się nie zmieniło. Po 36 godzinach bez kontroli pojawia się ostrzeżenie.

Awaria jednego źródła daje wynik `partial`: działające źródło może dodać mecze, a wcześniejsze wydarzenia pozostają. Awaria obu daje `error` i pozostawia plik kalendarza bez zmian. Oba wyniki powodują czerwony przebieg Actions, po opublikowaniu logów. `last_success_utc` oznacza ostatnią kontrolę, w której udało się odczytać wszystkie aktywne źródła. Zmiana terminu lub szczegółów podnosi `SEQUENCE`, zachowując UID.

## Uruchomienie lokalne

Wymagany Python 3.12 i systemowa baza stref czasowych (obecne na `ubuntu-latest`). Bez dodatkowych bibliotek:

```sh
python3 updater.py
```

Test bez sieci, na zapisanych odpowiedziach źródeł:

```sh
python3 updater.py --fixture cev.html --pzps-fixture pzps.json
```

Polecenia zapisują stan w bieżącym katalogu; testy wykonuj w katalogu tymczasowym, aby nie zastąpić produkcyjnego stanu.

## Pierwsza konfiguracja nowego repozytorium

W działającym repozytorium niczego nie zmieniaj w ustawieniach. Przy instalacji od zera potrzebny jest istniejący workflow `.github/workflows/update-calendar.yml`, GitHub Pages ze źródłem „GitHub Actions” oraz uprawnienia workflow do zapisu zawartości i publikacji Pages. Sam pakiet aktualizacyjny nie jest instalatorem nowego projektu.
