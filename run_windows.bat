@echo off
echo Installing required libraries...
python -m pip install -r requirements.txt
echo.
echo Starting Invisible Cloak...
python main.py
pause
