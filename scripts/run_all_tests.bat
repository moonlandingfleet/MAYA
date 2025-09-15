@echo off
echo Running Full Test Suite for MAYA King's App MVP
echo =================================================

cd /d "c:\Users\bryan\Desktop\MAYA\backend"

echo.
echo 1. Testing Supabase Connection...
python test_supabase_connection.py
if %errorlevel% neq 0 (
    echo ERROR: Supabase connection test failed
    pause
    exit /b %errorlevel%
)

echo.
echo 2. Populating Councils...
python populate_councils.py
if %errorlevel% neq 0 (
    echo ERROR: Council population failed
    pause
    exit /b %errorlevel%
)

echo.
echo 3. Verifying Councils...
python verify_councils.py
if %errorlevel% neq 0 (
    echo ERROR: Council verification failed
    pause
    exit /b %errorlevel%
)

echo.
echo 4. Testing Android Connection...
python test_android_connection.py
if %errorlevel% neq 0 (
    echo ERROR: Android connection test failed
    pause
    exit /b %errorlevel%
)

echo.
echo All tests completed successfully!
pause