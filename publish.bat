@echo off
echo.
echo ========================================
echo   BOB Events 2 - Publishing to Live Site
echo ========================================
echo.
cd /d "%~dp0"
git add -A
git commit -m "Update events %date%"
git push
echo.
echo Done! Site will be live in about 1 minute.
echo https://crinow-sketch.github.io/bob-events-2/
echo.
pause
