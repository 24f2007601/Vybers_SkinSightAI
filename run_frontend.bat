@echo off
echo Starting React Vite Dev Server...
cd frontend
if not exist node_modules (
    echo Installing npm dependencies...
    npm install
)
npm run dev
