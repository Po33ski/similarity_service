#!/bin/bash
# Main launcher for Vector Search & RAG Systems
# Allows user to choose between two systems

clear
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║         VECTOR SEARCH & RAG SYSTEMS - MLOps Lab Project                   ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "This project contains two AI-powered systems:"
echo ""
echo "┌────────────────────────────────────────────────────────────────────────────┐"
echo "│ 1️⃣  AI BASICS RAG SERVICE                                                  │"
echo "│    📚 Question & Answer system using PDF documents                         │"
echo "│    🤖 Powered by: Milvus + Google Gemini AI                                │"
echo "│    📖 Dataset: AI Guide document (119 pages)                               │"
echo "│    💬 Use case: Ask questions about AI and get intelligent answers         │"
echo "└────────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "┌────────────────────────────────────────────────────────────────────────────┐"
echo "│ 2️⃣  STEAM GAME SEARCH SERVICE                                              │"
echo "│    🎮 Semantic search engine for video games                               │"
echo "│    🔍 Powered by: PostgreSQL + pgvectorscale                               │"
echo "│    🗂️  Dataset: Steam Games (40,000+ games available)                      │"
echo "│    🎯 Use case: Find similar games by description                          │"
echo "└────────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "┌────────────────────────────────────────────────────────────────────────────┐"
echo "│ 0️⃣  EXIT                                                                   │"
echo "└────────────────────────────────────────────────────────────────────────────┘"
echo ""
read -p "Select a system [0-2]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting AI Basics RAG Service..."
        echo "════════════════════════════════════════════════════════════════════════════"
        echo ""
        ./run_rag.sh
        ;;
    2)
        echo ""
        echo "🚀 Starting Steam Game Search Service..."
        echo "════════════════════════════════════════════════════════════════════════════"
        echo ""
        ./run_search.sh
        ;;
    0)
        echo ""
        echo "👋 Goodbye!"
        echo ""
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Invalid option. Please run again and select 0, 1, or 2."
        echo ""
        exit 1
        ;;
esac

