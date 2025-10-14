# start.ps1 - Cockpit launch script for Flask application
Write-Host "🚀 Starter PorteføljePilot cockpit..."

# Skift til projektmappe
Set-Location "\\DS420j\workspace\AI\AI-Active\AI-Python-PortefoeljePilot"

# Aktivér virtuel miljø
. .venv\Scripts\Activate.ps1

# Sæt miljøvariabler (Windows-style)
$env:FLASK_APP = "./app/app.py"
$env:FLASK_ENV = "development"

# Start Flask
python -m flask run --host=0.0.0.0 --port=5000

# Start browser automatisk
Start-Process "http://localhost:5000"
