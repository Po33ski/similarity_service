# 🚀 START HERE - Quick Reference

## Two AI-Powered Systems

This project contains two vector search and RAG (Retrieval-Augmented Generation) systems for different use cases.

---

## 🎯 Main Launcher (Recommended)

```bash
./main.sh
```

Choose between:
1. **AI Basics RAG Service** - Q&A with documents
2. **Steam Game Search Service** - Find similar games

---

## 1️⃣ AI Basics RAG Service

### What it does:
- 📄 Analyzes PDF documents (AI guide, 119 pages)
- 🧠 Creates semantic embeddings using Milvus
- 💬 Interactive Q&A chat interface
- 🤖 Generates answers using Google Gemini AI

### Quick Start:
```bash
./run_rag.sh
```

### Example:
```
❓ Your question: What is machine learning?
💡 Answer: Algorithms capable of learning without direct programming.
```

### Technology:
- **Vector DB:** Milvus Lite (embedded)
- **AI Model:** Google Gemini 2.0 Flash
- **Embeddings:** ipipan/silver-retriever-base-v1.1
- **Dataset:** AI Guide PDF (auto-downloaded)

---

## 2️⃣ Steam Game Search Service

### What it does:
- 🎮 Searches 200+ games from Steam dataset
- 🔍 Finds similar games semantically
- 💰 Filters by price, platform (Windows/Linux/Mac)
- ⚡ Fast vector similarity search using PostgreSQL

### Quick Start:
```bash
./run_search.sh
```

### Example:
```
🎮 What game are you looking for? space exploration
💰 Max price: 30
💻 Platform: windows

✅ Found 5 games:
1. Oxygen Not Included - $24.99
   Platforms: Windows, Linux, Mac
   Description: Space-colony simulation game...
```

### Technology:
- **Vector DB:** PostgreSQL + pgvectorscale
- **Embeddings:** distiluse-base-multilingual-cased-v2
- **Dataset:** Steam Games (HuggingFace)
- **Requires:** Docker Desktop

---

## 📋 Prerequisites

### For AI Basics RAG Service:
- ✅ Python 3.11+
- ✅ uv package manager
- ✅ **Google Gemini API key** - [Get it here (FREE!)](API_KEY_SETUP.md)

### For Steam Game Search Service:
- ✅ All of the above, plus:
- ✅ Docker Desktop
- ✅ WSL2 integration (Windows users)

---

## 🚀 First Time Setup

### 1. Install Dependencies

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync
```

### 2. Configure API Key

**🔑 Get your FREE Google Gemini API key:**

See **[API_KEY_SETUP.md](API_KEY_SETUP.md)** for step-by-step instructions with screenshots!

Quick version:
```bash
# Copy example configuration
cp env_setup.sh.example env_setup.sh

# Edit with your API key
nano env_setup.sh

# Load environment variables
source env_setup.sh
```

### 3. Run!

```bash
# Use main launcher
./main.sh

# OR run systems directly
./run_rag.sh      # AI Basics RAG
./run_search.sh   # Steam Game Search
```

---

## 🎯 Which One To Use?

| Need | Use This | Command |
|------|----------|---------|
| Answer questions from documents | AI Basics RAG | `./run_rag.sh` |
| Find similar products/games | Steam Game Search | `./run_search.sh` |
| Learn about AI concepts | AI Basics RAG | `./run_rag.sh` |
| Discover new games | Steam Game Search | `./run_search.sh` |

---

## 🆘 Quick Troubleshooting

### "GOOGLE_API_KEY not found"

```bash
source env_setup.sh
```

If file doesn't exist:
```bash
cp env_setup.sh.example env_setup.sh
nano env_setup.sh  # Add your API key
source env_setup.sh
```

**Need help?** See [API_KEY_SETUP.md](API_KEY_SETUP.md)

### "Docker not available"

1. Install Docker Desktop
2. Enable WSL2 integration (Settings → Resources → WSL Integration)
3. Restart terminal

### "ModuleNotFoundError"

```bash
uv sync
```

---

## 📚 Full Documentation

- **[API_KEY_SETUP.md](API_KEY_SETUP.md)** ← **How to get Google API key (FREE, with screenshots)**
- **[FIRST_TIME_USER.md](FIRST_TIME_USER.md)** ← Step-by-step for beginners
- **[SETUP.md](SETUP.md)** - Complete setup guide
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start for both systems
- **[CONSOLE_GUIDE.md](CONSOLE_GUIDE.md)** - All console commands
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview

---

## ⚡ Super Quick Start

```bash
# 1. Setup (one time)
uv sync
cp env_setup.sh.example env_setup.sh
nano env_setup.sh  # Add API key (see API_KEY_SETUP.md)
source env_setup.sh

# 2. Run main launcher
./main.sh

# 3. Choose your system and enjoy!
```

**That's it!** 🎉

---

## 📊 Comparison

| Feature | AI Basics RAG | Steam Game Search |
|---------|---------------|-------------------|
| **Purpose** | Q&A from documents | Find similar items |
| **Database** | Milvus Lite | PostgreSQL |
| **Setup** | Easy (no Docker) | Needs Docker |
| **Data Source** | PDF documents | Steam games |
| **AI Model** | Gemini (answers) | SentenceTransformer |
| **Filters** | None | Price, platform, score |
| **First Run** | 5-10 min | 2-3 min |
| **Use Case** | Research, learning | Discovery, search |

---

## 🔗 Quick Links

### Get API Key (FREE)
📖 **[Detailed Setup Guide](API_KEY_SETUP.md)** with screenshots

Quick links:
- Get API key: https://ai.google.dev/pricing?hl=pl#1_5flash
- Google AI Studio: https://aistudio.google.com/

### Install Tools
- uv: https://docs.astral.sh/uv/
- Docker: https://www.docker.com/products/docker-desktop/

### Datasets
- Steam Games: https://huggingface.co/datasets/FronkonGames/steam-games-dataset
- AI Guide: Auto-downloaded on first run

---

## 🎓 Project Structure

```
IPUM_Lab02/
├── main.sh                  # Main launcher ← START HERE
├── run_rag.sh              # AI Basics RAG Service
├── run_search.sh           # Steam Game Search Service
├── env_setup.sh.example    # Configuration template
├── env_setup.sh            # Your API keys (YOU create this, git-ignored)
│
├── lab_rag/                # AI Basics RAG Service
├── similarity_service/     # Steam Game Search Service
├── vectorscale_db/         # PostgreSQL database
│
└── Documentation:
    ├── API_KEY_SETUP.md    # How to get API key ⭐
    ├── FIRST_TIME_USER.md  # For beginners ⭐
    ├── START_HERE.md       # This file
    ├── SETUP.md            # Complete setup
    ├── QUICKSTART.md       # Quick start
    ├── CONSOLE_GUIDE.md    # All commands
    └── PROJECT_SUMMARY.md  # Overview
```

---

**Enjoy exploring vector search and RAG systems!** 🚀
