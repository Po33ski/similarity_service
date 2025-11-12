# Quick Start Guide

## Two AI-Powered Systems

This project contains **two production-ready vector search systems**:

### 1. AI Basics RAG Service (Milvus + Gemini)
**Location:** `lab_rag/`  
**Purpose:** Q&A system analyzing PDF documents  
**Database:** Milvus Lite (embedded)  
**AI Model:** Google Gemini 2.0 Flash (Experimental)  
**Requirements:** Google API key  

### 2. Steam Game Search Service (PostgreSQL + pgvectorscale)
**Location:** `similarity_service/`  
**Purpose:** Semantic search engine for video games  
**Database:** PostgreSQL with pgvectorscale  
**Dataset:** Steam Games (40,000+ available)  
**Requirements:** Docker Desktop  

---

## AI Basics RAG Service - Quick Start

### Setup (One-time)

```bash
# 1. Navigate to project directory (wherever you cloned it)
cd IPUM_Lab02

# 2. Install dependencies
uv sync

# 3. Configure API key
cp env_setup.sh.example env_setup.sh
nano env_setup.sh  # Add your Google API key

# 4. Load environment variables
source env_setup.sh
```

### Run

```bash
# Recommended: use main launcher
./main.sh

# OR run directly
./run_rag.sh

# OR manually
cd lab_rag
uv run python main.py
```

**What happens:**
- First time: Downloads PDF, creates embeddings (5-10 min), starts chat
- Subsequent runs: Shows menu → Choose chat or rebuild

**Example interaction:**
```
 Your question: What is artificial intelligence?
 Answer: Systems or machines that mimic human intelligence...
```

 **Full documentation:** `lab_rag/README.md`

---

## Steam Game Search Service - Quick Start

### Prerequisites

- Docker Desktop installed
- WSL2 integration enabled (Windows users)

### Run (Simple - Recommended)

```bash
# Recommended: use main launcher
./main.sh

# OR run directly
./run_search.sh
```

**What happens automatically:**
-  Checks if Docker is running
-  Starts PostgreSQL database if needed
-  Loads sample data on first run (200 games, ~2 min)
-  Launches interactive search interface

### Load Data (Optional, ~30 minutes)

```bash
cd similarity_service
uv run python tests/test_games.py
```

This loads 40,000 games. To load fewer games faster, edit `test_games.py`:
```python
dataset = dataset["train"].select(range(1000))  # Change 40000 to 1000
```

### Run Demo

```bash
cd similarity_service
uv run python demo_search.py
```

**What happens:**
- Shows 4 example searches
- Enters interactive mode
- You describe a game, it finds similar ones

**Example interaction:**
```
 Describe the game you're looking for: space exploration game
Max price (press Enter for no limit): 20
Platform (windows/linux/mac, or Enter for any): 

 Found 5 similar games:
1. No Man's Sky - $29.99
   Platforms: Windows, Linux
   Description: Explore infinite procedurally generated universe...
```

 **Full documentation:** `similarity_service/README.md`

---

## Stopping Services

### RAG System
No need to stop - uses embedded database

### Similarity Search
```bash
cd vectorscale_db
docker compose down
```

---

## Troubleshooting

### RAG System

**Problem:** `GOOGLE_API_KEY not found`  
**Solution:** Run `source env_setup.sh` before starting

**Problem:** Slow embedding generation  
**Solution:** Normal on CPU, ~5-10 minutes for 119 pages

### Similarity Search

**Problem:** `docker: command not found`  
**Solution:** 
1. Install Docker Desktop
2. Enable WSL2 integration in settings
3. Restart WSL terminal

**Problem:** `Connection refused` to database  
**Solution:**
```bash
# Check if container is running
docker ps | grep vectorscaledb

# If not running, start it
cd vectorscale_db
docker compose up -d
```

**Problem:** No games found in search  
**Solution:** Load data first: `uv run python tests/test_games.py`

---

## Comparison

| Feature | RAG System | Similarity Search |
|---------|-----------|-------------------|
| **Database** | Milvus Lite | PostgreSQL |
| **Use Case** | QA from documents | Find similar items |
| **Setup** | Easy (no Docker) | Needs Docker |
| **Data Source** | PDF documents | Steam games |
| **AI Model** | Gemini (answers) | SentenceTransformer (search) |
| **Filters** | None | Price, platform, score |

---

## Next Steps

1. **Explore RAG system**: 
   - Try different questions
   - Upload your own PDF (edit `main.py`)
   - Change Gemini model in `env_setup.sh`

2. **Explore Similarity Search**:
   - Search for different game types
   - Adjust filters (price, platform)
   - Use as API in your application

3. **Read full documentation**:
   - RAG: `lab_rag/README.md`
   - Similarity: `similarity_service/README.md`

4. **Check the code**:
   - RAG interface: `lab_rag/milvus_rag_interface.py`
   - Search queries: `similarity_service/game_queries.py`

