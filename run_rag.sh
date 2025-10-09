#!/bin/bash
# Quick launcher script for RAG system
# Usage: ./run_rag.sh

echo "🚀 Starting RAG System..."
echo ""

# Check if env_setup.sh exists
if [ ! -f "env_setup.sh" ]; then
    echo "❌ Error: env_setup.sh not found!"
    echo "Please create it with your API key:"
    echo "  GOOGLE_API_KEY=\"your_key_here\""
    echo "  GEMINI_MODEL=\"gemini-2.0-flash-exp\""
    exit 1
fi

# Load environment variables
echo "📝 Loading environment variables..."
source env_setup.sh

# Navigate to lab_rag directory
cd lab_rag

# Run the main script using uv (ensures proper virtual environment)
echo ""
echo "▶️  Running RAG system..."
echo ""
uv run python main.py

echo ""
echo "✅ RAG system finished!"

