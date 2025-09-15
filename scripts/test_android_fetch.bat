@echo off
echo Testing Android App Council Fetch
echo ================================

echo Make sure the MAYA Core server is running on http://localhost:8000
echo If not, start it with scripts\start_maya_with_venv.bat

echo.
echo Testing council fetch from Android app...
cd /d "c:\Users\bryan\Desktop\MAYA\backend"
python test_android_connection.py

pause