@echo off
echo Verifying councils in Supabase database...
cd /d "c:\Users\bryan\Desktop\MAYA\backend"
python verify_councils.py
echo Council verification complete.
pause