# 📊 Project Summary

## Vector Search & RAG Systems - MLOps Lab Project

Complete implementation of two production-ready AI systems demonstrating vector databases, semantic search, and RAG (Retrieval-Augmented Generation).

---

## 🎯 Project Overview

| System | Purpose | Technology | Dataset |
|--------|---------|------------|---------|
| **AI Basics RAG Service** | Q&A from documents | Milvus + Gemini | AI Guide (119 pages) |
| **Steam Game Search Service** | Find similar games | PostgreSQL + pgvector | Steam Games (83k+) |

---

## 🚀 For New Users - Getting Started

### Clone & Setup (5 minutes)

\`\`\`bash
# 1. Clone repository
git clone <repo-url>
cd IPUM_Lab02

# 2. Install dependencies
uv sync

# 3. Configure API key
cp env_setup.sh.example env_setup.sh
nano env_setup.sh  # Add your Google API key
source env_setup.sh

# 4. Run!
./main.sh
\`\`\`

### What You Get

✅ **AI Basics RAG Service**
- Interactive Q&A about AI concepts
- No Docker required (uses Milvus Lite)
- Instant setup

✅ **Steam Game Search Service**  
- Semantic game discovery
- Advanced filtering (price, platform)
- Requires Docker Desktop

---

## 📁 Repository Structure

\`\`\`
IPUM_Lab02/
├── 🚀 Launchers
│   ├── main.sh              # Main launcher (choose system)
│   ├── run_rag.sh          # AI Basics RAG Service
│   └── run_search.sh       # Steam Game Search Service
│
├── 📖 Documentation
│   ├── START_HERE.md       # Quick reference (start here!)
│   ├── SETUP.md            # Complete setup guide
│   ├── QUICKSTART.md       # Quick start for both systems
│   ├── CONSOLE_GUIDE.md    # All console commands
│   └── PROJECT_SUMMARY.md  # This file
│
├── 🤖 AI Basics RAG Service
│   └── lab_rag/
│       ├── main.py                    # Interactive menu
│       ├── milvus_rag_interface.py   # RAG interface class
│       ├── milvus_db/                # Milvus Lite database
│       └── README.md                 # System documentation
│
├── 🎮 Steam Game Search Service
│   ├── similarity_service/
│   │   ├── main_search.py          # Auto-setup & search
│   │   ├── search.py               # Simple search tool
│   │   ├── game_queries.py         # Search API
│   │   ├── models.py               # Database models
│   │   ├── embeddings.py           # Embedding generation
│   │   └── README.md               # System documentation
│   │
│   └── vectorscale_db/
│       ├── docker-compose.yml      # PostgreSQL setup
│       └── initdb/                 # Database init scripts
│
└── 🔧 Configuration
    ├── env_setup.sh           # Your API keys (git-ignored)
    ├── env_setup.sh.example   # Template
    ├── pyproject.toml         # Python dependencies
    └── .gitignore             # Git ignore rules
\`\`\`

---

## 🛠️ Technology Stack

### AI Basics RAG Service
- **Vector Database:** Milvus Lite 2.4 (embedded)
- **AI Model:** Google Gemini 2.0 Flash
- **Embeddings:** ipipan/silver-retriever-base-v1.1 (768-dim, Polish-optimized)
- **Framework:** Python 3.12, PyMilvus
- **Document Processing:** PyMuPDF (fitz)
- **No Docker Required** ✅

### Steam Game Search Service
- **Vector Database:** PostgreSQL 16 + TimescaleDB + pgvectorscale 0.8
- **Embeddings:** distiluse-base-multilingual-cased-v2 (512-dim)
- **Framework:** Python 3.12, SQLAlchemy 2.0, psycopg3
- **Dataset:** Steam Games via HuggingFace
- **Requires Docker** 🐳

---

## 💡 Key Features

### AI Basics RAG Service Features
- ✅ Automatic PDF download and processing
- ✅ Intelligent menu system (auto-detect embeddings)
- ✅ Interactive chat interface
- ✅ Multi-language support (Polish/English prompts)
- ✅ Semantic search with L2 distance
- ✅ Context-aware AI responses

### Steam Game Search Service Features
- ✅ Semantic similarity search (not keyword-based!)
- ✅ Advanced filtering (price, platform, similarity score)
- ✅ Auto-setup (database + data loading)
- ✅ Interactive search interface
- ✅ SQL + Vector operations combined
- ✅ Scalable to millions of records

---

## 📊 Datasets

### AI Guide Document
- **Source:** IAB Polska
- **Format:** PDF
- **Size:** 119 pages (~6 MB)
- **Language:** Polish
- **Content:** AI fundamentals, tools, legal aspects
- **Auto-downloaded:** Yes

### Steam Games
- **Source:** HuggingFace (FronkonGames/steam-games-dataset)
- **Total:** 83,560 games
- **Fields:** Name, description, price, platforms
- **Demo size:** 200 games (quick start)
- **Full size:** 40,000 games (recommended)
- **Auto-downloaded:** Yes

---

## 🎓 Educational Value

This project demonstrates:

### Vector Databases
- **Milvus:** Purpose-built vector database
- **PostgreSQL + pgvectorscale:** SQL database with vector extensions
- **Comparison:** When to use each approach

### RAG (Retrieval-Augmented Generation)
- Document processing pipeline
- Embedding generation
- Context retrieval
- AI response generation
- Prompt engineering

### MLOps Best Practices
- Modular code structure
- Object-oriented design
- Docker containerization
- Environment configuration
- Comprehensive documentation
- Production-ready error handling

### Vector Search Techniques
- Semantic similarity (cosine distance, L2)
- Index optimization (HNSW, AUTOINDEX)
- Hybrid filtering (vector + SQL)
- Embedding models (SentenceTransformers)

---

## 🔧 Configuration Files

### env_setup.sh (User-created)
\`\`\`bash
export GOOGLE_API_KEY="your_key_here"
export GEMINI_MODEL="gemini-2.0-flash-exp"
\`\`\`

### pyproject.toml (Dependencies)
- google-genai (Gemini API)
- pymilvus (Milvus client)
- psycopg (PostgreSQL driver)
- sentence-transformers (Embeddings)
- sqlalchemy (ORM)
- datasets (HuggingFace)
- And more...

---

## 📈 Performance Characteristics

### AI Basics RAG Service
- **First run:** 5-10 minutes (download + embeddings)
- **Subsequent runs:** Instant (uses cache)
- **Query latency:** 1-3 seconds (search + AI generation)
- **Storage:** ~50 MB (embeddings + database)

### Steam Game Search Service
- **First run:** 2-3 minutes (200 games)
- **Full dataset:** 30+ minutes (40,000 games)
- **Query latency:** <100ms (vector search only)
- **Storage:** ~500 MB (40k games with embeddings)

---

## 🔐 Security

- ✅ API keys in `.gitignore`
- ✅ Example config file provided
- ✅ Database credentials configurable
- ✅ Local-only by default (no external exposure)

---

## 🤝 For Developers

### AI Basics RAG Service
- Class: `MilvusRAGInterface` (lab_rag/milvus_rag_interface.py)
- Methods: `rag()`, `search()`, `process_document()`
- Import: `from milvus_rag_interface import MilvusRAGInterface`

### Steam Game Search Service
- Functions: `find_similar_games()` (similarity_service/game_queries.py)
- Models: `Games`, `Images` (similarity_service/models.py)
- Import: `from game_queries import find_similar_games`

---

## 📝 Usage Examples

### AI Basics RAG
\`\`\`python
from milvus_rag_interface import MilvusRAGInterface

rag = MilvusRAGInterface()
answer = rag.rag("What is machine learning?")
print(answer)
\`\`\`

### Steam Game Search
\`\`\`python
from game_queries import find_similar_games

games = find_similar_games(
    "fantasy RPG with magic",
    max_price=20.0,
    limit=5
)
\`\`\`

---

## 🎯 Use Cases

### AI Basics RAG Service
- Research assistance
- Document Q&A
- Knowledge base querying
- Educational applications
- Technical documentation search

### Steam Game Search Service
- Game recommendation systems
- Product discovery platforms
- E-commerce similarity search
- Content-based filtering
- Catalog exploration

---

## 📚 Documentation Index

1. **START_HERE.md** - Quick reference (read this first!)
2. **SETUP.md** - Complete setup instructions
3. **QUICKSTART.md** - Quick start for both systems
4. **CONSOLE_GUIDE.md** - All console commands
5. **lab_rag/README.md** - AI Basics RAG details
6. **similarity_service/README.md** - Steam Game Search details
7. **PROJECT_SUMMARY.md** - This file (overview)

---

## 🔗 External Resources

- [Milvus Documentation](https://milvus.io/docs)
- [pgvectorscale](https://github.com/timescale/pgvectorscale)
- [Sentence Transformers](https://www.sbert.net/)
- [Google Gemini API](https://ai.google.dev/)
- [Steam Games Dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset)
- [uv Package Manager](https://docs.astral.sh/uv/)

---

## 🏆 Project Highlights

✨ **Production-ready code**
✨ **Comprehensive documentation**
✨ **Two different vector database approaches**
✨ **Interactive user interfaces**
✨ **Automated setup and deployment**
✨ **Real-world datasets**
✨ **MLOps best practices**

---

**Ready to explore?** Run `./main.sh` and choose your adventure! 🚀

---

*Educational Project - AGH University, IPUM Lab 02*
