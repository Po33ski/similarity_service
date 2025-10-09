# 🚀 Quick Start Guide

## Two Systems in This Project

This project contains **two different vector similarity search systems**:

### 1. 🤖 RAG System (Milvus + Gemini)
**Location:** `lab_rag/`  
**Purpose:** Question-answering system using PDF documents  
**Database:** Milvus Lite (embedded)  
**Requirements:** Google API key  

### 2. 🎮 Similarity Search Service (PostgreSQL + pgvectorscale)
**Location:** `similarity_service/`  
**Purpose:** Find similar games based on descriptions  
**Database:** PostgreSQL with pgvectorscale  
**Requirements:** Docker Desktop  

---

## 🤖 RAG System - Quick Start

### Setup (One-time)

```bash
# 1. Navigate to project
cd /home/jarek/AGH/IPUM/IPUM_Lab02

# 2. Install dependencies
uv sync

# 3. Configure API key (edit with your key)
nano env_setup.sh

# 4. Load environment variables
source env_setup.sh
```

### Run

```bash
# Simple run
./run_rag.sh

# Or manually
cd lab_rag
uv run python main.py
```

**What happens:**
- First time: Downloads PDF, creates embeddings (5-10 min), starts chat
- Subsequent runs: Shows menu → Choose chat or rebuild

**Example interaction:**
```
❓ Your question: What is artificial intelligence?
💡 Answer: Systems or machines that mimic human intelligence...
```

📖 **Full documentation:** `lab_rag/README.md`

---

## 🎮 Similarity Search - Quick Start

### Setup (One-time)

```bash
# 1. Enable Docker Desktop WSL2 integration
#    Docker Desktop → Settings → Resources → WSL Integration
#    Enable for your distro, click Apply & Restart

# 2. Start the service
cd /home/jarek/AGH/IPUM/IPUM_Lab02
./run_similarity_service.sh
```

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
🎮 Describe the game you're looking for: space exploration game
Max price (press Enter for no limit): 20
Platform (windows/linux/mac, or Enter for any): 

✅ Found 5 similar games:
1. No Man's Sky - $29.99
   Platforms: Windows, Linux
   Description: Explore infinite procedurally generated universe...
```

📖 **Full documentation:** `similarity_service/README.md`

---

## 🛑 Stopping Services

### RAG System
No need to stop - uses embedded database

### Similarity Search
```bash
cd vectorscale_db
docker compose down
```

---

## 🔧 Troubleshooting

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

## 📊 Comparison

| Feature | RAG System | Similarity Search |
|---------|-----------|-------------------|
| **Database** | Milvus Lite | PostgreSQL |
| **Use Case** | QA from documents | Find similar items |
| **Setup** | Easy (no Docker) | Needs Docker |
| **Data Source** | PDF documents | Steam games |
| **AI Model** | Gemini (answers) | SentenceTransformer (search) |
| **Filters** | None | Price, platform, score |

---

## 📚 Next Steps

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

