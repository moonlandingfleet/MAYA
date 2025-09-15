@echo off
echo MAYA King's App MVP Development Setup
echo ====================================

echo.
echo This script will help you set up the development environment for the MAYA King's App MVP.
echo.

echo 1. Activating Python virtual environment...
call ..\maya-env\Scripts\activate.bat

echo.
echo 2. Verifying Python dependencies...
pip list | findstr "fastapi uvicorn web3 supabase"

echo.
echo 3. Checking Supabase credentials...
if exist "..\backend\.env.manual" (
    echo Supabase credentials file found.
) else (
    echo WARNING: Supabase credentials file not found!
    echo Please create a .env.manual file in the backend directory with your credentials.
)

echo.
echo 4. Testing Supabase connection...
cd ..\backend
python test_supabase_connection.py

echo.
echo 5. Populating councils in database...
python populate_councils.py

echo.
echo 6. Verifying councils...
python verify_councils.py

echo.
echo Development setup completed!
echo.
echo To start the server, run: scripts\start_maya_with_venv.bat
echo.
pause