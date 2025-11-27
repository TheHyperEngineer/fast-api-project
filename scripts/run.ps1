#!/usr/bin/env pwsh
Write-Host "Starting uvicorn app (app.main:app) on 127.0.0.1:8005"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8005 --reload --log-level debug
