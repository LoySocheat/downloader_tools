@echo off
pip install --no-cache-dir -r requirements.txt
echo "Installed Library Successfully! Please close the script. "
pause
@RD /S /Q ".\history"
@RD /S /Q ".\module"