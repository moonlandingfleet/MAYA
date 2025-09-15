@echo off
echo Populating councils in Supabase database...
cd /d "c:\Users\bryan\Desktop\MAYA\backend"
python populate_councils.py
echo Council population complete.
pause