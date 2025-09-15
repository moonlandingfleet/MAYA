@echo off
echo Activating Python virtual environment and starting MAYA Core Server...
echo.

cd /d "c:\Users\bryan\Desktop\MAYA"

REM Activate the virtual environment
call maya-env\Scripts\activate.bat

REM Change to the backend directory
cd backend

REM Start the server
python main.py

pause