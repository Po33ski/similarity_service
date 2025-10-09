# 🖥️ Console Guide - Similarity Search System

Quick reference for using the Similarity Search system from command line.

## 🚀 Quick Start Commands

### Start the system (RECOMMENDED - All-in-one)
```bash
cd ./similarity_service
./run_search.sh
```

This automatically:
- Checks Docker
- Starts database if needed
- Loads data on first run
- Launches interactive search

### Start database only (Manual)
```bash
cd /home/jarek/AGH/IPUM/IPUM_Lab02
./run_similarity_service.sh
```

### Stop the system
```bash
cd vectorscale_db
docker compose down
```

---

## 🔍 SEARCHING FOR GAMES

### Method 1: Simple interactive search (RECOMMENDED)
```bash
cd similarity_service
uv run python search.py
```

**What happens:**
- Asks what you're looking for
- Optional: set max price
- Optional: choose platform
- Shows top 5 results

**Example session:**
```
🎮 What game are you looking for? strategy game
💰 Max price (Enter for any): 20
💻 Platform (windows/linux/mac or Enter for any): 

✅ Found 5 games:
1. 🎯 Oxygen Not Included
   💵 Price: $24.99
   ...
```

---

### Method 2: Full demo with examples
```bash
cd similarity_service
uv run python demo_search.py
```

**Shows:**
- 4 pre-made example searches
- Then interactive mode

---

### Method 3: Python code (for scripts)
```bash
cd similarity_service
uv run python
```

Then in Python:
```python
from game_queries import find_similar_games

# Simple search
games = find_similar_games("fantasy RPG")
for game in games:
    print(f"{game.name} - ${game.price}")

# With filters
games = find_similar_games(
    "action shooter",
    max_price=30.0,
    windows=True,
    limit=10
)

# Advanced filters
games = find_similar_games(
    "indie platformer",
    max_price=10.0,
    linux=True,
    min_score=0.5,  # Minimum similarity
    limit=5
)
```

---

## 💾 MANAGING DATA

### Load sample data (200 games, ~2 minutes)
```bash
cd similarity_service
uv run python quick_demo.py
```

### Load full dataset (1000 games, ~10 minutes)
```bash
cd similarity_service

# Edit the file first to set number of games:
nano tests/test_games.py
# Change: range(40000) to range(1000)

# Then run:
uv run python tests/test_games.py
```

### Check how many games you have
```bash
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db \
  -c "SELECT COUNT(*) FROM games;"
```

### See some games in database
```bash
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db \
  -c "SELECT name, price FROM games LIMIT 10;"
```

### Clear all games (start fresh)
```bash
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db \
  -c "DELETE FROM games;"
```

---

## 🔧 DATABASE COMMANDS

### Connect to database
```bash
docker exec -it vectorscaledb psql -U postgres -d similarity_search_service_db
```

Once connected, you can run SQL:
```sql
-- See all tables
\dt

-- Count games
SELECT COUNT(*) FROM games;

-- See expensive games
SELECT name, price FROM games WHERE price > 50 ORDER BY price DESC;

-- See free games
SELECT name FROM games WHERE price = 0 LIMIT 10;

-- See Linux games
SELECT name, price FROM games WHERE linux = true LIMIT 10;

-- Exit
\q
```

### View database structure
```bash
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db \
  -c "\d games"
```

### Check database size
```bash
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db \
  -c "SELECT pg_size_pretty(pg_database_size('similarity_search_service_db'));"
```

---

## 🐳 DOCKER COMMANDS

### Check if running
```bash
docker ps | grep vectorscaledb
```

### View logs
```bash
docker logs vectorscaledb
```

### Follow logs in real-time
```bash
docker logs -f vectorscaledb
```

### Restart database
```bash
cd vectorscale_db
docker compose restart
```

### Stop database
```bash
cd vectorscale_db
docker compose down
```

### Stop and remove all data
```bash
cd vectorscale_db
docker compose down -v  # WARNING: Deletes all games!
```

### Start database
```bash
cd vectorscale_db
docker compose up -d
```

---

## 📊 USEFUL QUERIES

### Find games by description (SQL)
```bash
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db -c \
  "SELECT name, description FROM games WHERE description LIKE '%space%' LIMIT 5;"
```

### Most expensive games
```bash
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db -c \
  "SELECT name, price FROM games ORDER BY price DESC LIMIT 10;"
```

### Cheapest games
```bash
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db -c \
  "SELECT name, price FROM games WHERE price > 0 ORDER BY price ASC LIMIT 10;"
```

### Games by platform
```bash
# Windows only
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db -c \
  "SELECT COUNT(*) FROM games WHERE windows = true;"

# Linux only  
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db -c \
  "SELECT COUNT(*) FROM games WHERE linux = true;"

# Mac only
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db -c \
  "SELECT COUNT(*) FROM games WHERE mac = true;"
```

---

## 🎯 EXAMPLE WORKFLOWS

### Workflow 1: Quick search session
```bash
# 1. Make sure system is running
docker ps | grep vectorscaledb

# 2. Start search tool
cd /home/jarek/AGH/IPUM/IPUM_Lab02/similarity_service
uv run python search.py

# 3. Search for games!
```

### Workflow 2: Load more data
```bash
# 1. Check current count
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db \
  -c "SELECT COUNT(*) FROM games;"

# 2. Load 200 more games
cd /home/jarek/AGH/IPUM/IPUM_Lab02/similarity_service
uv run python quick_demo.py

# 3. Verify
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db \
  -c "SELECT COUNT(*) FROM games;"
```

### Workflow 3: Reset and start fresh
```bash
# 1. Stop database
cd /home/jarek/AGH/IPUM/IPUM_Lab02/vectorscale_db
docker compose down -v

# 2. Start fresh
docker compose up -d
sleep 5

# 3. Create tables
cd ../similarity_service
uv run python main.py

# 4. Load data
uv run python quick_demo.py
```

---

## 🆘 TROUBLESHOOTING

### Database not responding
```bash
# Check if running
docker ps | grep vectorscaledb

# If not running, start it
cd vectorscale_db
docker compose up -d

# Wait and check again
sleep 5
docker ps | grep vectorscaledb
```

### Can't connect to database
```bash
# Check logs for errors
docker logs vectorscaledb | tail -50

# Try restarting
cd vectorscale_db
docker compose restart

# Check if port is in use
lsof -i :5556
```

### Search returns no results
```bash
# Check if you have games
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db \
  -c "SELECT COUNT(*) FROM games;"

# If 0, load data
cd similarity_service
uv run python quick_demo.py
```

### Python errors
```bash
# Make sure dependencies are installed
cd /home/jarek/AGH/IPUM/IPUM_Lab02
uv sync

# Check Python version
python --version  # Should be 3.11+
```

---

## 📚 CHEAT SHEET

```bash
# Quick commands you'll use most often:

# Start system
./run_similarity_service.sh

# Search for games
cd similarity_service && uv run python search.py

# Load 200 sample games
cd similarity_service && uv run python quick_demo.py

# Check game count
docker exec vectorscaledb psql -U postgres -d similarity_search_service_db -c "SELECT COUNT(*) FROM games;"

# Stop system
cd vectorscale_db && docker compose down
```

---

## 🔗 Related Files

- Main search tool: `similarity_service/search.py`
- Demo with examples: `similarity_service/demo_search.py`
- Load data: `similarity_service/quick_demo.py`
- Full documentation: `similarity_service/README.md`

