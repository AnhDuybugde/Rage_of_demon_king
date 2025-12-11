@echo off

echo [*] Connecting ADB to LDPlayer...
"C:\LDPlayer\LDPlayer9\adb.exe" connect 127.0.0.1:5555
echo [*] ADB connected!

REM ===========================
REM 2️⃣ Activate virtual env + run Flask
REM ===========================
cd /d C:\Users\jackw\Desktop\JLOY\Rage_of_demon_king\bot_project

echo [*] Activating venv...
call venv\Scripts\activate

echo [*] Starting Flask server...
python app.py

pause
