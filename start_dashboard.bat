@echo off
REM ===========================
REM 1️⃣ Kết nối ADB với LDPlayer
REM ===========================
echo [*] Connecting ADB to LDPlayer...
"C:\LDPlayer\LDPlayer9\adb.exe" connect 127.0.0.1:5555
if %errorlevel% neq 0 (
    echo [!] Failed to connect ADB. Check LDPlayer and adb path.
    pause
    exit /b
)
echo [*] ADB connected!

REM ===========================
REM 2️⃣ Chạy Flask server
REM ===========================
cd /d C:\Users\jloy5\OneDrive\Desktop\Rage_of_demonking\bot_project
echo [*] Starting Flask server...
start python app.py

REM Chờ 3 giây để Flask khởi động
timeout /t 3

@REM REM ===========================
@REM REM 3️⃣ (Tùy chọn) Chạy ngrok
@REM REM ===========================
@REM REM cd /d C:\ngrok
@REM REM echo [*] Starting ngrok...
@REM REM start ngrok http 5000

echo [*] Done! Flask + ADB connected.
pause
