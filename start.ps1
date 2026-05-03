$env:PYTHONPATH = $PSScriptRoot
Write-Host "Starting Quality Inspection Dashboard..." -ForegroundColor Cyan
& "$PSScriptRoot\.venv\Scripts\uvicorn.exe" "app.main:app" "--host" "0.0.0.0" "--port" "8000" "--reload"
