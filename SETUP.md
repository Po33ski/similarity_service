# 🛠️ Project Setup Guide

Complete setup instructions for Vector Search & RAG Systems.

## 📋 Prerequisites

Before you begin, ensure you have:

### Required:
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **uv package manager** - [Install Guide](https://docs.astral.sh/uv/getting-started/installation/)
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### For AI Basics RAG Service (Required):
- **Google Gemini API Key** - [Get it here](https://aistudio.google.com/apikey)

### For Steam Game Search Service (Required):
- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
- **WSL2 integration enabled** (for Windows users)

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd IPUM_Lab02
```

### Step 2: Install Dependencies

```bash
uv sync
```

This will:
- Create a virtual environment (`.venv/`)
- Install all Python dependencies
- Download required models (~700MB for first time)

### Step 3: Configure API Key

**Get your API key first:** See [API_KEY_SETUP.md](API_KEY_SETUP.md) for detailed instructions with screenshots.

Quick setup:

```bash
# 1. Copy the example file
cp env_setup.sh.example env_setup.sh

# 2. Edit with your API key
nano env_setup.sh

# 3. Replace YOUR_API_KEY_HERE with your actual key
export GOOGLE_API_KEY="AIzaSy..."  # Your actual key here
export GEMINI_MODEL="gemini-2.0-flash-exp"

# 4. Save and load
source env_setup.sh
```

**Important:** This file (`env_setup.sh`) is git-ignored for security!

### Step 4: Load Environment

```bash
source env_setup.sh
```

### Step 5: (Optional) Setup Docker for Game Search

If you want to use the Steam Game Search Service:

1. Install Docker Desktop
2. For Windows/WSL2 users:
   - Open Docker Desktop
   - Go to: Settings → Resources → WSL Integration
   - Enable integration for your WSL distribution
   - Click "Apply & Restart"

---

## ✅ Verify Installation

### Test AI Basics RAG Service:

```bash
./run_rag.sh
```

You should see:
```
🤖 RAG System - Retrieval-Augmented Generation with Milvus and Gemini
🔧 Initializing RAG Interface...
✅ Collection 'rag_texts_and_embeddings' ready
```

### Test Steam Game Search Service:

```bash
./run_search.sh
```

You should see:
```
🎮 SIMILARITY SEARCH SYSTEM
🔍 Step 1: Checking Docker... ✅
🔍 Step 2: Checking database... 
```

---

## 📂 Project Structure

```
IPUM_Lab02/
├── main.sh                 # Main launcher (start here!)
├── run_rag.sh             # AI Basics RAG Service
├── run_search.sh          # Steam Game Search Service
├── env_setup.sh           # Your API keys (git-ignored)
│
├── lab_rag/               # RAG System
│   ├── main.py           # RAG main script
│   ├── milvus_rag_interface.py
│   ├── milvus_db/        # Milvus Lite database
│   └── README.md
│
├── similarity_service/    # Game Search System
│   ├── main_search.py    # Search main script
│   ├── search.py
│   ├── game_queries.py
│   ├── models.py
│   └── README.md
│
├── vectorscale_db/       # PostgreSQL setup
│   ├── docker-compose.yml
│   └── initdb/
│
└── Documentation:
    ├── SETUP.md          # This file
    ├── START_HERE.md     # Quick reference
    ├── QUICKSTART.md     # Quick start guide
    └── CONSOLE_GUIDE.md  # All console commands
```

---

## 🔧 Configuration Details

### Environment Variables

The `env_setup.sh` file contains:

```bash
# Required for AI Basics RAG Service
export GOOGLE_API_KEY="your_key_here"

# Optional: Change AI model
export GEMINI_MODEL="gemini-2.0-flash-exp"
```

### Database Configuration

**AI Basics RAG:**
- Uses Milvus Lite (embedded, no setup needed)
- Data stored in: `lab_rag/milvus_db/`

**Steam Game Search:**
- Uses PostgreSQL with pgvectorscale
- Requires Docker
- Port: 5556 (localhost)
- Database: `similarity_search_service_db`

---

## 🎯 Usage

### Recommended: Use Main Launcher

```bash
./main.sh
```

This shows a menu to choose between:
1. AI Basics RAG Service
2. Steam Game Search Service

### Direct Access

```bash
# AI Basics RAG
./run_rag.sh

# Steam Game Search
./run_search.sh
```

---

## 📚 Datasets

### AI Basics RAG Service

**Document:** AI Guide (Polish)
- **Source:** IAB Polska
- **Pages:** 119
- **Size:** ~6 MB
- **Auto-downloaded** on first run

### Steam Game Search Service

**Dataset:** Steam Games
- **Source:** HuggingFace (FronkonGames/steam-games-dataset)
- **Total games:** 83,560
- **Default loaded:** 200 (for demo)
- **Auto-downloaded** on first run

To load more games:
```bash
cd similarity_service
# Edit tests/test_games.py to change amount
uv run python tests/test_games.py
```

---

## 🐛 Troubleshooting

### "GOOGLE_API_KEY not found"

**Problem:** Environment variables not loaded

**Solution:**
```bash
source env_setup.sh
```

Add to your `~/.bashrc` for permanence:
```bash
echo "source ~/path/to/project/env_setup.sh" >> ~/.bashrc
```

### "Docker not available"

**Problem:** Docker not installed or WSL integration disabled

**Solution:**
1. Install Docker Desktop
2. Enable WSL2 integration (Windows)
3. Restart terminal

### "ModuleNotFoundError"

**Problem:** Dependencies not installed

**Solution:**
```bash
uv sync
```

### "CUDA capability sm_120 is not compatible"

**Problem:** GPU not supported by current PyTorch (RTX 50xx series)

**Solution:** This is normal - the system automatically uses CPU. Performance is still good for this project.

### Database connection failed

**Problem:** PostgreSQL not running

**Solution:**
```bash
cd vectorscale_db
docker compose up -d
```

---

## 🔒 Security Notes

### API Keys

- `env_setup.sh` is in `.gitignore` - never commit it!
- Keep your API key private
- Regenerate if exposed

### Docker

- PostgreSQL uses default password (`password`)
- Only accessible on localhost
- For production: change credentials in `vectorscale_db/docker-compose.yml`

---

## 📈 Performance Notes

### First Run

- **AI Basics RAG:** Downloads PDF + generates embeddings (~5-10 min)
- **Steam Game Search:** Downloads dataset + generates embeddings (~2-3 min for 200 games)

### Subsequent Runs

- **AI Basics RAG:** Instant (uses cached embeddings)
- **Steam Game Search:** Instant (uses database)

### Hardware Requirements

**Minimum:**
- CPU: Dual-core 2GHz+
- RAM: 4GB
- Disk: 5GB free

**Recommended:**
- CPU: Quad-core 3GHz+
- RAM: 8GB+
- Disk: 10GB free
- GPU: Optional (CUDA compatible)

---

## 🔄 Updating

### Update Dependencies

```bash
uv sync --upgrade
```

### Update Project

```bash
git pull origin main
uv sync
```

### Reset Databases

**AI Basics RAG:**
```bash
cd lab_rag
rm -rf milvus_db/milvus_lite.db
rm -rf milvus_db/data/*.json
```

**Steam Game Search:**
```bash
cd vectorscale_db
docker compose down -v
docker compose up -d
```

---

## 📞 Support

### Documentation

- `START_HERE.md` - Quick reference
- `QUICKSTART.md` - Quick start guide  
- `CONSOLE_GUIDE.md` - All console commands
- `lab_rag/README.md` - RAG system details
- `similarity_service/README.md` - Search system details

### Common Issues

Check the Troubleshooting section above or the documentation files.

---

## 🎓 Learning Resources

### Technologies Used

- **Milvus:** Vector database - [docs](https://milvus.io/docs)
- **pgvectorscale:** PostgreSQL vector extension - [docs](https://github.com/timescale/pgvectorscale)
- **Sentence Transformers:** Embedding models - [docs](https://www.sbert.net/)
- **Google Gemini:** AI for response generation - [docs](https://ai.google.dev/)

### Datasets

- **Steam Games:** [HuggingFace](https://huggingface.co/datasets/FronkonGames/steam-games-dataset)
- **AI Guide:** [IAB Polska](https://www.iab.org.pl/)

---

## ✅ You're All Set!

Run the main launcher:
```bash
./main.sh
```

Enjoy exploring vector search and RAG systems! 🚀

