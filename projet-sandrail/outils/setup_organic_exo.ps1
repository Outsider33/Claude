# ============================================================================
#  ORGANIC EXO — Préparation du poste de travail (Windows x64)
#  Télécharge les installeurs dans  ~\Downloads\Setup_ORGANIC_EXO  puis
#  installe PlatformIO Core via uv. N'installe PAS les logiciels (les .exe
#  restent à lancer manuellement — vous gardez la main).
#
#  Usage : clic droit > Exécuter avec PowerShell, ou dans un terminal :
#     powershell -ExecutionPolicy Bypass -File .\setup_organic_exo.ps1
# ============================================================================
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$dir = Join-Path ([Environment]::GetFolderPath('UserProfile')) 'Downloads\Setup_ORGANIC_EXO'
New-Item -ItemType Directory -Force -Path $dir | Out-Null
Write-Host "Dossier cible : $dir" -ForegroundColor Green
$report = @()

function Get-Installer([string]$name, [string]$url, [string]$out) {
    $dest = Join-Path $script:dir $out
    if (Test-Path $dest) {
        Write-Host ">> $name : déjà présent, on saute." -ForegroundColor Yellow
    } else {
        Write-Host ">> $name" -ForegroundColor Cyan
        Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing
    }
    $mb = [math]::Round((Get-Item $dest).Length / 1MB, 1)
    $script:report += "{0,-28} {1,8} Mo  {2}" -f $name, $mb, $out
}

# --- 1. KiCad 10.0.4 (miroir officiel GitHub) -------------------------------
Get-Installer 'KiCad 10.0.4 x64' `
    'https://github.com/KiCad/kicad-source-mirror/releases/download/10.0.4/kicad-10.0.4-x86_64.exe' `
    'kicad-10.0.4-x86_64.exe'

# --- 2. FreeCAD : dernier stable via l'API GitHub ----------------------------
Write-Host '>> FreeCAD : résolution du dernier stable...' -ForegroundColor Cyan
$fc = Invoke-RestMethod 'https://api.github.com/repos/FreeCAD/FreeCAD/releases/latest' -UseBasicParsing
$fcAsset = $fc.assets | Where-Object { $_.name -match 'Windows-x86_64.*\.exe$' } | Select-Object -First 1
if (-not $fcAsset) { $fcAsset = $fc.assets | Where-Object { $_.name -match 'Windows.*x86_64' } | Select-Object -First 1 }
Get-Installer "FreeCAD $($fc.tag_name)" $fcAsset.browser_download_url $fcAsset.name

# --- 3. Blender : dernier stable via l'index officiel ------------------------
Write-Host '>> Blender : résolution du dernier stable...' -ForegroundColor Cyan
$idx = (Invoke-WebRequest 'https://download.blender.org/release/' -UseBasicParsing).Content
$serie = ([regex]::Matches($idx, 'Blender(\d+\.\d+)/') | ForEach-Object { [version]$_.Groups[1].Value } |
          Sort-Object | Select-Object -Last 1).ToString()
$sidx = (Invoke-WebRequest "https://download.blender.org/release/Blender$serie/" -UseBasicParsing).Content
$msi = ([regex]::Matches($sidx, "blender-$serie\.\d+-windows-x64\.msi") | ForEach-Object { $_.Value } |
        Sort-Object | Select-Object -Last 1)
Get-Installer "Blender $serie (msi)" "https://download.blender.org/release/Blender$serie/$msi" $msi

# --- 4. Foxglove (visualisation télémétrie) ----------------------------------
try {
    Get-Installer 'Foxglove (dernier)' `
        'https://get.foxglove.dev/desktop/latest/foxglove-studio-latest-win.exe' `
        'foxglove-studio-latest-win.exe'
} catch {
    Write-Host "   Lien direct indisponible -> installation via winget :" -ForegroundColor Yellow
    winget install --id Foxglove.Studio -e --accept-source-agreements --accept-package-agreements
    $script:report += 'Foxglove                      (installé via winget)'
}

# --- 5. PlatformIO Core via uv ----------------------------------------------
Write-Host '>> PlatformIO Core (uv tool install)...' -ForegroundColor Cyan
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host '   uv absent -> installation (winget Astral.uv)...' -ForegroundColor Yellow
    winget install --id astral-sh.uv -e --accept-source-agreements --accept-package-agreements
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + $env:Path
}
uv tool install platformio
$pio = (uv tool run --from platformio pio --version) 2>$null
$script:report += "PlatformIO Core               $pio (global via uv)"

# --- Compte-rendu ------------------------------------------------------------
Write-Host "`n================ COMPTE-RENDU ================" -ForegroundColor Green
$report | ForEach-Object { Write-Host $_ }
Write-Host "Fichiers dans : $dir"
Write-Host 'Prochaine étape : lancer les installeurs, puis dérouler l''Annexe A du PDF (MCP FreeCAD/Blender).'
