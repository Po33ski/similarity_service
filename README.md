# Vector Search and RAG Applications in MLOps

Two production-ready AI systems demonstrating vector search, vector databases, and Retrieval-Augmented Generation (RAG) in MLOps context.

## 🎯 Two Systems, One Project

### 1️⃣ **AI Basics RAG Service**
Question & Answer system using Milvus vector database and Google Gemini AI.
- 📄 Analyzes PDF documents
- 🧠 Semantic search with embeddings
- 🤖 AI-powered answers

### 2️⃣ **Steam Game Search Service**  
Semantic similarity search engine using PostgreSQL with pgvectorscale.
- 🎮 Find similar games by description
- 💰 Filter by price, platform
- ⚡ Fast vector similarity search

## 🚀 Quick Start

### For First-Time Users

```bash
# 1. Clone repository
git clone <repo-url>
cd IPUM_Lab02

# 2. Install dependencies
uv sync

# 3. Setup API key
cp env_setup.sh.example env_setup.sh
nano env_setup.sh  # Add your Google API key from https://aistudio.google.com/apikey
source env_setup.sh

# 4. Run!
./main.sh
```

**Choose between:**
- **Option 1:** AI Basics RAG Service (easier, no Docker)
- **Option 2:** Steam Game Search Service (needs Docker)

### Quick Access

```bash
./run_rag.sh      # AI Basics RAG Service
./run_search.sh   # Steam Game Search Service
./main.sh         # Main launcher (choose system)
```

## 📋 Requirements

### Required
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Google Gemini API key - **[Setup Guide](API_KEY_SETUP.md)** ← Get your free key here!

### For Steam Game Search Service
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- WSL2 integration enabled (Windows users)

## 📁 Project Structure

```
IPUM_Lab02/
├── main.sh                 # Main launcher
├── run_rag.sh             # AI Basics RAG Service
├── run_search.sh          # Steam Game Search Service
│
├── lab_rag/               # RAG System (Milvus + Gemini)
│   ├── main.py
│   ├── milvus_rag_interface.py
│   └── milvus_db/
│
├── similarity_service/    # Search System (PostgreSQL)
│   ├── main_search.py
│   ├── game_queries.py
│   └── models.py
│
└── vectorscale_db/       # PostgreSQL + pgvectorscale
    ├── docker-compose.yml
    └── initdb/
```

## 🛠️ Technology Stack

### AI Basics RAG Service
- **Vector DB:** Milvus Lite (embedded)
- **AI Model:** Google Gemini 2.0 Flash
- **Embeddings:** ipipan/silver-retriever-base-v1.1 (Polish-optimized)
- **Dataset:** AI Guide PDF (119 pages)
- **Framework:** Python, SQLAlchemy

### Steam Game Search Service
- **Vector DB:** PostgreSQL 16 + TimescaleDB + pgvectorscale
- **Embeddings:** distiluse-base-multilingual-cased-v2
- **Dataset:** Steam Games ([HuggingFace](https://huggingface.co/datasets/FronkonGames/steam-games-dataset))
- **Framework:** Python, SQLAlchemy, Docker

## 📚 Documentation

**New to this project?** → Read **[FIRST_TIME_USER.md](FIRST_TIME_USER.md)** ← **Start here!**

Complete documentation:
- **[FIRST_TIME_USER.md](FIRST_TIME_USER.md)** - Step-by-step for beginners
- **[API_KEY_SETUP.md](API_KEY_SETUP.md)** - How to get Google API key (with screenshots)
- **[START_HERE.md](START_HERE.md)** - Quick reference
- **[SETUP.md](SETUP.md)** - Complete setup guide
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[CONSOLE_GUIDE.md](CONSOLE_GUIDE.md)** - All console commands
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview

System-specific:
- **[lab_rag/README.md](lab_rag/README.md)** - AI Basics RAG details
- **[similarity_service/README.md](similarity_service/README.md)** - Steam Game Search details

## 💡 Use Cases

### AI Basics RAG Service
- Research assistance
- Document Q&A
- Knowledge base querying
- Learning about AI concepts

### Steam Game Search Service
- Game discovery
- Similar product search
- Semantic catalog search
- Recommendation systems

## 🎓 Educational Value

This project demonstrates:
- Vector databases (Milvus vs PostgreSQL+pgvector)
- Semantic search with embeddings
- RAG (Retrieval-Augmented Generation)
- MLOps best practices
- Production-ready code structure
- Docker deployment
- API integration (Google Gemini)

## 📊 Datasets

### AI Basics RAG
- **Source:** [IAB Polska AI Guide](https://www.iab.org.pl/wp-content/uploads/2024/04/Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.pdf)
- **Size:** 119 pages (Polish language)
- **Auto-downloaded:** Yes

### Steam Game Search
- **Source:** [Steam Games Dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset)
- **Total:** 83,560 games
- **Default demo:** 200 games
- **Auto-downloaded:** Yes

## 🔧 Configuration

All configuration in `env_setup.sh`:
```bash
export GOOGLE_API_KEY="your_key_here"
export GEMINI_MODEL="gemini-2.0-flash-exp"
```

**Note:** This file is git-ignored for security!

## 🐳 Docker Services

### Steam Game Search Service
```bash
# Start PostgreSQL
cd vectorscale_db
docker compose up -d

# Stop
docker compose down
```

## 🤝 Contributing

This is an educational project for MLOps course (AGH University).

## 📝 License

Educational project - AGH IPUM Lab 02

## 🔗 Resources

- [Milvus Documentation](https://milvus.io/docs)
- [pgvectorscale](https://github.com/timescale/pgvectorscale)
- [Sentence Transformers](https://www.sbert.net/)
- [Google Gemini API](https://ai.google.dev/)
- [Steam Games Dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset)

---

**Ready to start?** Run `./main.sh` and choose your system! 🚀
