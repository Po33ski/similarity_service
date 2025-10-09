#!/bin/bash
# Script to run the similarity service system

echo "🚀 Starting Similarity Service System"
echo "=" * 80

# Step 1: Start PostgreSQL with vectorscale
echo ""
echo "📦 Step 1: Starting PostgreSQL + pgvectorscale..."
cd vectorscale_db
docker compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Error: Docker not available or failed to start"
    echo "Please ensure Docker Desktop is running and WSL2 integration is enabled"
    exit 1
fi

echo "✅ PostgreSQL started on port 5556"
echo ""

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Step 2: Check if database is accessible
echo ""
echo "🔍 Step 2: Checking database connection..."
docker exec vectorscaledb psql -U postgres -c "SELECT version();" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Database is accessible"
else
    echo "⚠️  Database not ready yet, waiting 5 more seconds..."
    sleep 5
fi

# Step 3: Initialize database tables
echo ""
echo "🏗️  Step 3: Initializing database tables..."
cd ../similarity_service
uv run python main.py

if [ $? -eq 0 ]; then
    echo "✅ Database tables created"
else
    echo "❌ Failed to create tables"
    exit 1
fi

echo ""
echo "=" * 80
echo "✅ Similarity Service is ready!"
echo ""
echo "📚 Next steps:"
echo "   1. Load data: cd similarity_service && uv run python tests/test_games.py"
echo "   2. Test search: Use the Python scripts in similarity_service/"
echo ""
echo "🛑 To stop: cd vectorscale_db && docker compose down"
echo "=" * 80

