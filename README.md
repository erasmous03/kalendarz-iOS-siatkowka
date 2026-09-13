# Subskrybowany kalendarz – polska reprezentacja siatkarzy

Kalendarz i dziennik kontroli dla **męskiej reprezentacji seniorów na ME 2026**. Oficjalne źródło: [CEV](https://www-old.cev.eu/Competition-Area/CompetitionView.aspx?CID=12862&ID=1572&PID=2990). Dopisanie VNL, MŚ lub następnego sezonu wymaga wskazania i zaimplementowania osobnego oficjalnego źródła; obecna wersja nie udaje, że je monitoruje.

## Pierwsze uruchomienie (GitHub Pages)

1. Utwórz **publiczne** repozytorium na GitHubie, np. `polska-siatkowka-kalendarz`, i prześlij całą zawartość paczki do gałęzi `main`. Publiczny kalendarz nie zawiera danych osobowych. Nie używaj skopiowanego osobnego pliku `.ics` jako subskrypcji – użyj opublikowanego URL.
2. W repozytorium przejdź do **Settings → Pages → Build and deployment → Source → GitHub Actions**. W **Settings → Actions → General → Workflow permissions** ustaw **Read and write permissions**, jeśli są wyłączone (skrypt zapisuje historię do repozytorium). Pozwól na korzystanie z GitHub Pages w organizacji, jeżeli konto tego wymaga.
3. W zakładce **Actions → Aktualizuj kalendarz reprezentacji → Run workflow** uruchom pierwszy przebieg z `main`. Po jego zakończeniu adres strony to zwykle `https://NAZWA-UZYTKOWNIKA.github.io/NAZWA-REPOZYTORIUM/`, a adres subskrypcji: `https://NAZWA-UZYTKOWNIKA.github.io/NAZWA-REPOZYTORIUM/calendar.ics`.
4. Na iPhonie wybierz **Ustawienia → Aplikacje → Kalendarz → Konta kalendarza → Dodaj konto → Inne → Dodaj kalendarz subskrybowany**, wklej adres HTTPS do `calendar.ics` i zapisz. Nazwy ustawień mogą się nieznacznie różnić między wersjami iOS. Nie importuj lokalnego pliku, bo to nie daje aktualizacji.

Zadanie sprawdza źródło codziennie o **07:23 UTC** (09:23 latem i 08:23 zimą w Polsce); można też uruchomić je ręcznie. Godziny CEV są lokalne dla miast rozgrywania meczów. Skrypt przelicza je na UTC w ICS, więc iPhone poprawnie pokaże godzinę polską. Zakładany czas trwania wpisu to trzy godziny od rozpoczęcia – mecz może skończyć się wcześniej lub później.

## Kontrola pracy

Strona główna pokazuje datę ostatniego przebiegu, jego wynik, liczbę wydarzeń oraz 30 ostatnich kontroli. `site/history.json` przechowuje 90 ostatnich wpisów, a `data/history.jsonl` pełną historię w repozytorium. Każdy przebieg, także bez nowych meczów, tworzy wpis. Błędy pobrania nie kasują poprzedniego kalendarza; w Actions przebieg ma stan błędu. Brak kontroli przez 36 godzin jest sygnalizowany na stronie. Zmiany godziny, rywala i miejsca poprawiają istniejący wpis dzięki stałemu UID; nowi rywale fazy pucharowej trafiają dopiero po potwierdzeniu przez CEV.

GitHub może opóźnić start zaplanowanego zadania; uruchomienia widać w Actions. Publiczny adres subskrypcji i dziennika można udostępniać. URL pobierania ICS przez iPhone jest ten sam każdego dnia, ale moment odświeżenia na telefonie zależy od Apple.

## Lokalna kontrola

W katalogu projektu wykonaj `python3 updater.py`. Skrypt używa tylko biblioteki standardowej Python 3.12. Jeśli CEV zmieni układ strony, otrzymasz błąd w logach i zachowasz dotychczasowe wydarzenia.
