@echo off
setlocal

REM Set up environment variables
set JAVA_HOME=C:\Program Files\Microsoft\jdk-17.0.16.8-hotspot
set ANDROID_HOME=C:\Users\bryan\AppData\Local\Android\Sdk
set PATH=%JAVA_HOME%\bin;%ANDROID_HOME%\platform-tools;%PATH%

REM Change to the project directory
cd /d C:\Users\bryan\Desktop\MAYA

REM Stop any existing daemons
gradlew.bat --stop

REM Try to build the project
echo Building the APK...
gradlew.bat assembleDebug

echo.
echo Build process completed.
pause