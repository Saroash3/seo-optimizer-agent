@echo off
REM Quick Deployment Setup Script

echo ================================================
echo   Adding Deployment Files
echo ================================================
echo.

echo Creating Procfile...
echo web: gunicorn app:app --bind 0.0.0.0:$PORT > Procfile
echo ✓ Created Procfile

echo.
echo Creating runtime.txt...
echo python-3.11.0 > runtime.txt
echo ✓ Created runtime.txt

echo.
echo Creating render.yaml...
(
echo services:
echo   - type: web
echo     name: seo-optimizer-agent
echo     env: python
echo     buildCommand: pip install -r requirements.txt
echo     startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
echo     envVars:
echo       - key: PYTHON_VERSION
echo         value: 3.11.0
) > render.yaml
echo ✓ Created render.yaml

echo.
echo Updating requirements.txt...
(
echo Flask==3.0.0
echo Werkzeug==3.0.1
echo python-dateutil==2.8.2
echo flask-swagger-ui==4.11.1
echo PyYAML==6.0.1
echo gunicorn==21.2.0
) > requirements.txt
echo ✓ Updated requirements.txt

echo.
echo ================================================
echo   ✓ All deployment files created!
echo ================================================
echo.
echo Next steps:
echo 1. git add Procfile render.yaml runtime.txt requirements.txt
echo 2. git commit -m "Add deployment files"
echo 3. git push
echo 4. Go to https://render.com and deploy
echo.
pause
