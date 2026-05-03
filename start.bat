@echo off
echo Starting Quality Inspection Dashboard...
set PYTHONPATH=%~dp0
.\.venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload
