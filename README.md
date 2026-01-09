# 🏎️ F1 Telemetry Analyzer

**F1 Telemetry Analyzer** to profesjonalne narzędzie analityczne stworzone w języku Python. Aplikacja pozwala na pobieranie, przetwarzanie i wizualizację oficjalnych danych telemetrycznych Formuły 1, korzystając z biblioteki `FastF1`.

---

## 📌 Główne Funkcjonalności

Aplikacja dostarcza interaktywny interfejs (Streamlit), który umożliwia:
* **Analizę Sesji GP:** Pobieranie danych z dowolnego weekendu wyścigowego (treningi, kwalifikacje, wyścig).
* **Speed Trace Comparison:** Porównywanie wykresów prędkości kierowców "okrążenie w okrążenie" w celu znalezienia różnic w punktach hamowania.
* **Telemetria Zakrętów:** Szczegółowy wgląd w operowanie gazem (`Throttle`), hamulcem (`Brake`) oraz zmiany biegów (`Gear`).
* **Strategie Oponiarskie:** Wizualizacja zużycia opon oraz historii pit-stopów dla całej stawki.

---

## 🏗️ Architektura i Wzorce Projektowe

Projekt został zaprojektowany z myślą o skalowalności i czystości kodu, implementując klasyczne wzorce projektowe:

### ⚙️ Wzorce Strukturalne
* **Kompozyt (Composite):** System traktuje dane o sesji jako drzewo (Sezon -> Sesja -> Okrążenia). Pozwala to na jednolite zarządzanie statystykami dla pojedynczego przejazdu oraz całego wyścigu.
* **Fasada (Facade):** Stworzono warstwę abstrakcji nad biblioteką `FastF1`. Ukrywa ona złożoność logowania do API, zarządzania cache'em oraz czyszczenia danych (handling brakujących wartości w Pandas) przed warstwą UI.

### ⚙️ Wzorce Kreacyjne
* **Fabryka Abstrakcyjna (Abstract Factory):** Służy do generowania spójnych zestawów komponentów wizualnych. Dzięki niej aplikacja może dynamicznie tworzyć dedykowane panele wykresów dla trybu wyścigowego (Race) lub kwalifikacyjnego (Quali).

### ⚙️ Wzorce Behawioralne
* **Strategia (Strategy):** Wykorzystywana do implementacji różnych algorytmów obliczeniowych, np. wyboru metody interpolacji danych telemetrycznych (liniowa vs. spline) w zależności od zagęszczenia punktów GPS.
* **Metoda Szablonowa (Template Method):** Definiuje szkielet procesu analizy: `Pobierz` -> `Oczyść` -> `Przetwórz` -> `Wizualizuj`. Pozwala to na łatwe dodawanie nowych modułów analizy (np. zużycie paliwa) przy zachowaniu spójnego przepływu danych.

---

## 🛠️ Stack Technologiczny

* **Język:** Python 3.x
* **Dane:** [FastF1](https://github.com/theOehrly/Fast-F1) (oficjalne dane FIA)
* **Analiza danych:** Pandas, NumPy
* **Wizualizacja:** Matplotlib, Plotly (interaktywne wykresy)
* **Interfejs:** Streamlit

---
