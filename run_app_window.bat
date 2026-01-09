@echo off
echo ====================================================
echo   F1 Telemetry Analyzer - Autostart (Windows)
echo ====================================================

:: 1. Sprawdzanie czy Python istnieje
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo BLAD: Python nie jest zainstalowany lub nie dodano go do PATH!
    pause
    exit
)

:: 2. Tworzenie wirtualnego srodowiska jesli nie istnieje
if not exist "venv_win" (
    echo Tworzenie srodowiska wirtualnego venv_win...
    python -m venv venv_win
)

:: 3. Aktywacja i instalacja bibliotek
echo Aktywacja srodowiska i sprawdzanie bibliotek...
call .\venv_win\Scripts\activate.bat

echo Instalowanie wymagan (moze to potrwac chwile)...
pip install streamlit fastf1 matplotlib pandas typing-extensions

:: 4. Uruchomienie aplikacji
echo Uruchamianie aplikacji Streamlit...
set PYTHONPATH=.
streamlit run F1_ANALYSIS/main.py

pause