# startlocaldocker.ps1

Write-Host "🚀 Starter lokal Docker cockpit..."

# Skift til projektmappe
Set-Location "\\DS420J\workspace\AI\AI-Active\AI-Python-PortefoeljePilot"

# Tjek om Docker kører
try {
    docker info | Out-Null
}
catch {
    Write-Host "🐳 Docker Desktop er ikke aktiv. Start venligst Docker og prøv igen."
    exit 1
}

# Tjek om override-fil findes
$overrideExists = Test-Path ".\docker-compose.override.yaml"

# Byg compose-kommando
$composeCmd = "docker-compose -f docker-compose-local.yaml"
if ($overrideExists) {
    $composeCmd += " -f docker-compose.override.yaml"
}
$composeCmd += " up -d"

# Kør compose
Write-Host "📦 Kører: $composeCmd"
Invoke-Expression $composeCmd

# Vis status
Write-Host "`n📊 Containerstatus:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host "`n✅ Cockpit er startet. Flask bør være tilgængelig på http://localhost:5050"