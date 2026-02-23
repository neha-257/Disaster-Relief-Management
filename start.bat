@echo off
echo Starting Disaster Relief Management System...
echo.

rem Check if Node.js is installed
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo Node.js is not installed or not in your PATH.
  echo.
  echo Starting Flask server directly...
  cd backend
  python app.py
  exit /b
)

echo Starting with Node.js...
node start.js
pause 