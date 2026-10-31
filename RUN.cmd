@echo off
REM Kadans Timeline - Gran Laku Company (Getho Guerrier)
cd /d "%~dp0"
echo Ap louvri Kadans Timeline nan navigate ou a...
python tools\migrate_folders.py 2>nul || py tools\migrate_folders.py
python -m kadans timeline "Analyseur-Kadans/Pwoje-1"
if errorlevel 1 py -m kadans timeline "Analyseur-Kadans/Pwoje-1"
pause
