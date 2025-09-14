@echo off
setlocal enabledelayedexpansion

echo MAYA Auth Server - Token Test Script
echo ======================================

REM Check if token is provided as argument
if "%1"=="" (
    echo Usage: test_with_token.bat ^<your_supabase_token^>
    echo.
    echo Please provide a valid Supabase token as a command line argument.
    echo.
    echo Example:
    echo test_with_token.bat eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.EkN-DOsnsuRjRO6BxXemmJDm3HbxrbRzXglbN2S4sOkopdU4IsDxTI8jO19W_A4K8ZPJijNLis4EZsHeY559a4DFOd50_OqgHGuERTqYZyuhtF39y
    echo.
    exit /b 1
)

set TOKEN=%1

echo Testing protected endpoint with provided token...
echo.

curl -H "Authorization: Bearer %TOKEN%" http://localhost:8000/protected

echo.
echo.
echo If you received a 200 OK response with user data, the RS256 validation is working correctly.
echo If you received a 401 error, check the server console for validation error details.

pause