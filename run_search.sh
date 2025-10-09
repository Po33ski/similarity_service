#!/bin/bash
# Quick launcher for Similarity Search System
# Usage: ./run_search.sh

echo "🎮 Starting Similarity Search System..."
echo ""

# Navigate to similarity_service directory
cd similarity_service

# Run the main search script
uv run python main_search.py

echo ""
echo "✅ Similarity Search System finished!"

