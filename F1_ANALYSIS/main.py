import typer

app = typer.Typer()

@app.command()
def stworz_plik(nazwa: str, rozszerzenie: str = "txt", force: bool = False):
    """
    Tworzy plik o podanej nazwie.
    """
    pelna_nazwa = f"{nazwa}.{rozszerzenie}"
    if force:
        print(f"Wymuszam nadpisanie pliku: {pelna_nazwa}")
    else:
        print(f"Tworzę bezpiecznie plik: {pelna_nazwa}")

@app.command()
def policz(a: int, b: int, operacja: str = "dodaj"):
    """
    Wykonuje proste obliczenia matematyczne.
    """
    if operacja == "dodaj":
        print(f"Wynik: {a + b}")
    elif operacja == "mnoz":
        print(f"Wynik: {a * b}")
    else:
        print(f"Nieznana operacja: {operacja}")

# 4. Uruchamiamy aplikację (zamiast typer.run)
if __name__ == "__main__":
    app()