@echo off
echo ========================================================
echo  VYBERS SkinSight-AI: Launching Full-Stack Services
echo ========================================================
echo.
echo 1. Starting Backend FastAPI Server on http://localhost:8000
start "SkinSight-AI Backend" cmd /k "python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload"
echo.
echo 2. Starting Frontend React (Vite) Dev Server on http://localhost:5173
start "SkinSight-AI Frontend" cmd /k "cd frontend && npm install && npm run dev"
echo.
echo Both servers are launching in separate windows!
echo Backend Docs: http://localhost:8000/docs
echo Frontend App: http://localhost:5173
echo ========================================================
pause
