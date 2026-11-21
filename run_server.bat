@echo off
echo Starting VYBERS SkinSight-AI FastAPI Server...
echo API Docs will be available at http://localhost:8000/docs
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
