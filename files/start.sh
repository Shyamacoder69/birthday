#!/bin/bash
# National Birthday Aptitude Test — Quick Start

echo "🎂 Starting National Birthday Aptitude Test..."
echo ""

# Start FastAPI backend in background
echo "🚀 Starting FastAPI backend on port 8000..."
uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

sleep 2

# Start Streamlit frontend
echo "🎨 Starting Streamlit frontend on port 8501..."
echo ""
echo "═══════════════════════════════════════════"
echo "  Open: http://localhost:8501"
echo "  API:  http://localhost:8000/docs"
echo "═══════════════════════════════════════════"
echo ""

streamlit run frontend/app.py --server.port 8501

# Cleanup on exit
kill $BACKEND_PID 2>/dev/null
