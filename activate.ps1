Write-Host "====================================="
Write-Host "Branch Pull setup Started."
Write-Host "====================================="
Write-Host "====================================="
# $BRANCH_NAME = "main"
$BRANCH_NAME = "codex/implement-crud-operations-and-validation"
git fetch origin
git checkout $BRANCH_NAME
git pull origin $BRANCH_NAME
Write-Host "====================================="
Write-Host "Branch Pull setup completed."
Write-Host "====================================="

Write-Host "====================================="
Write-Host "Environment setup Started."
Write-Host "====================================="

# docker compose up --build