# 🏐 Biało-czerwoni w Twoim kalendarzu

**iOS · Android · Google Calendar · Apple Calendar · Outlook · ICS**

**Dodaj raz i kibicuj przez cały sezon.** Terminy, rywale i miejsca meczów polskich siatkarzy trafią prosto do Twojej aplikacji kalendarzowej. Liga Narodów, mistrzostwa Europy i świata, igrzyska, kwalifikacje i spotkania towarzyskie — w jednej subskrypcji, z codzienną kontrolą oficjalnego terminarza.

Godziny uwzględniają strefy czasowe, nowe spotkania pojawiają się po publikacji przez PZPS, a dziennik aktualizacji pozwala sprawdzić, kiedy skrypt działał i co zmienił. Bez ręcznego przepisywania dat. Aktualizacje na urządzeniu pojawiają się po odświeżeniu przez dostawcę kalendarza.

[Otwórz stronę i dodaj kalendarz](https://erasmous03.github.io/kalendarz-siatkowka-polska/) · [Adres ICS do subskrypcji](https://erasmous03.github.io/kalendarz-siatkowka-polska/calendar.ics)

Kalendarz i kod projektu zostały wygenerowane z pomocą **AI (ChatGPT)**. Terminy pochodzą z oficjalnych danych PZPS i CEV. Jest to niezależny projekt kibicowski.

Mecze seniorskiej reprezentacji Polski mężczyzn w siatkówce halowej, we wszystkich rozgrywkach publikowanych w [kalendarium PZPS](https://www.pzps.pl/pl/kalendarium): VNL, ME, MŚ, igrzyska, kwalifikacje, turnieje i mecze towarzyskie. Filtr obejmuje wyłącznie kategorię `VOLLEYBALL/NATIONAL-TEAMS/MEN` i spotkania z udziałem Polski. Nie ma ograniczenia do nazwy turnieju ani sezonu 2026.

## Opis do sekcji About na GitHubie

> 🏐 Biało-czerwoni w Twoim kalendarzu! Mecze polskich siatkarzy, aktualizowane codziennie: terminy, rywale i miejsca. iOS, Android, Google Calendar i Outlook. Niezależny projekt kibicowski stworzony z pomocą AI.

Opis można wkleić po kliknięciu koła zębatego przy **About**. Pole **Website**: `https://erasmous03.github.io/kalendarz-siatkowka-polska/`.

## Licznik kliknięć

Strona pokazuje wspólną liczbę kliknięć pięciu przycisków: Apple, Google/Android, Outlook, kopiowanie adresu i pobranie ICS. Samo wyświetlenie strony nie zwiększa licznika. Ponowne kliknięcia tej samej osoby są liczone ponownie. Kliknięcie nie potwierdza dodania subskrypcji ani pomyślnego importu.

Wynik przechowuje zewnętrzna [usługa CountAPI](https://countapi.mileshilliard.com/) — GitHub Pages nie zapisuje danych odwiedzających na serwerze. Integracja nie wymaga rejestracji ani klucza API. Kod naszej strony nie ustawia plików cookie ani identyfikatorów użytkowników; wysyła żądania odczytu i zwiększenia licznika, bez danych formularzy i bez nagłówka Referer. Operator usługi otrzymuje zwykłe dane połączenia sieciowego, w tym adres IP.

To statystyka orientacyjna: publiczny licznik można zmodyfikować poza stroną, blokery lub awarie usługi mogą pominąć kliknięcia, a dostawca nie gwarantuje dostępności. Nie służy do rozliczeń ani pomiaru unikalnych użytkowników. Nie rekonstruuje kliknięć sprzed wdrożenia.

Przy niedostępności API strona wyświetla komunikat; dodawanie kalendarza działa niezależnie. Nie pokazuje wymyślonego wyniku i nie zastępuje wspólnego licznika liczbą zapisaną lokalnie. Żądania zapisu nie blokują otwierania linków. Nie ma automatycznych ponowień zapisu, które mogłyby policzyć to samo kliknięcie dwa razy.

Stały identyfikator licznika jest w końcowym skrypcie `site/index.html`. Zachowaj go przy aktualizacjach. Fork projektu powinien używać własnego identyfikatora, aby nie mieszać statystyk.

### Wdrożenie tej aktualizacji

Podmień `site/index.html` i `README.md`, następnie wybierz **Actions → Aktualizuj kalendarz reprezentacji → Run workflow → main → Run workflow**. Obecny workflow nie uruchamia się automatycznie po zmianie samego HTML lub README. Nie trzeba zmieniać adresu subskrypcji, skryptu pobierającego mecze ani plików danych.

Po publikacji sprawdź, czy sekcja licznika wyświetla liczbę. Kliknij raz jeden z przycisków, następnie otwórz stronę w innym oknie i porównaj wynik. Ten test będzie rzeczywistym kliknięciem. Jeżeli API odmawia dostępu, widoczny będzie komunikat o niedostępności zamiast liczby; trzeba wtedy rozwiązać problem z dostawcą lub zmienić usługę.

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
