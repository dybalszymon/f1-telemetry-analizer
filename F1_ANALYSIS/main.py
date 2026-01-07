import sys
# Importujemy Fabrykę (Creation)
from creation.QualifyingFactory import QualifyingFactory
# Importujemy Fasadę (tylko do pobrania listy wyścigów, jeśli potrzebujesz)
from data.F1DataFacade import F1DataFacade


def print_menu():
    print("\n=== F1 TELEMETRY ANALYZER ===")
    print("1. Pokaż dostępne wyścigi (2024)")
    print("2. Generuj raport: Ranking Kwalifikacji (Najszybsze okrążenie) TODO!!")#TODO
    print("3. Generuj raport: Porównanie Telemetrii (H2H - Wykresy)")
    print("0. Wyjście")
    print("=============================")


def main():
    # Inicjalizacja głównych komponentów
    facade = F1DataFacade()
    factory = QualifyingFactory()

    while True:
        print_menu()
        choice = input("Wybierz opcję: ")

        if choice == "1":
            # --- STARA FUNKCJONALNOŚĆ (Bezpieczna) ---
            print("\nPobieranie listy wyścigów...")
            races = facade.get_meetings(2024)
            for r in races:
                print(f"[{r['meeting_key']}] {r['meeting_official_name']}")

        elif choice == "2":
            # --- RAPORT PROSTY (Ranking) ---
            s_key = input("Podaj Session Key (np. 9158): ")
            if s_key.isdigit():
                print(f"\nGenerowanie rankingu dla sesji {s_key}...")
                report = factory.create_ranking_report(int(s_key))
                report.generate_report()

        elif choice == "3":
            # --- NOWY RAPORT (Telemetria Composite + PlotRenderer) ---
            # Tutaj używamy nowej metody, którą dopisaliśmy do fabryki
            print("\n--- Konfiguracja Porównania ---")
            # Domyślne wartości dla testów (Bahrajn 2023, VER vs LEC)
            default_session = 9632

            s_key = input(f"Podaj Session Key [Enter dla {default_session}]: ")
            s_key = int(s_key) if s_key else default_session

            d1 = 1
            d2 = 16 #TODO methods to chose drivers from race and assign to this variables, race also

            if d1 and d2:
                print(f"\nPobieranie i przetwarzanie danych (to może chwilę potrwać)...")

                report = factory.create_telemetry_comparison(s_key, int(d1), int(d2))
                report.generate_report()
            else:
                print("Błąd: Musisz podać numery obu kierowców.")

        elif choice == "0":
            print("Zamykanie aplikacji...")
            sys.exit()

        else:
            print("Niepoprawny wybór.")


if __name__ == "__main__":
    main()