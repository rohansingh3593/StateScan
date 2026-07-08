param(
    [string]$TestTarget = ".\tests",
    [switch]$Verbose,
    [switch]$InstallDependencies
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

if ($InstallDependencies) {
    Write-Host "Installing dependencies from requirements.txt..."
    python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Dependency installation failed."
        exit $LASTEXITCODE
    }
}

$pytestArgs = @($TestTarget)
if ($Verbose) {
    $pytestArgs += '-v'
}

Write-Host "Running pytest against: $TestTarget"
python -m pytest @pytestArgs
exit $LASTEXITCODE
