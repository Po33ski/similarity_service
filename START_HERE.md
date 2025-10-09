# 🚀 START HERE - Quick Reference

## Two Systems, Two Commands

### 1️⃣ RAG System (Q&A with Documents)
```bash
./run_rag.sh
```
**What it does:**
- 📄 Loads PDF documents (AI guide, 119 pages)
- 🧠 Creates semantic embeddings
- 💬 Interactive Q&A chat
- 🤖 Uses Gemini AI for answers

**Example:**
```
❓ Your question: What is machine learning?
💡 Answer: Algorithms capable of learning without direct programming.
```

---

### 2️⃣ Similarity Search (Find Similar Games)
```bash
./run_search.sh
```
**What it does:**
- 🔍 Searches 200+ games from Steam
- 🎮 Finds similar games semantically
- 💰 Filters by price, platform
- ⚡ Fast vector similarity search

**Example:**
```
🎮 What game are you looking for? space exploration
💰 Max price: 30
✅ Found 5 games:
1. Oxygen Not Included - $24.99
```

---

## 📋 Prerequisites

### For RAG System:
- ✅ Already set up!
- Just run: `./run_rag.sh`

### For Similarity Search:
- Docker Desktop with WSL2 integration
- First run auto-loads 200 games (~2 min)

---

## 🎯 Which One To Use?

| Need | Use This |
|------|----------|
| Answer questions from documents | `./run_rag.sh` |
| Find similar products/items | `./run_search.sh` |
| Learn about AI from PDF | `./run_rag.sh` |
| Search Steam games | `./run_search.sh` |

---

## 🆘 Quick Troubleshooting

### RAG System
```bash
# Not working? Set API key:
source env_setup.sh
./run_rag.sh
```

### Similarity Search
```bash
# Docker not running?
# 1. Start Docker Desktop
# 2. Enable WSL2 integration in settings
# 3. Run: ./run_search.sh
```

---

## 📚 Full Documentation

- `QUICKSTART.md` - Quick start for both systems
- `CONSOLE_GUIDE.md` - All console commands
- `lab_rag/README.md` - RAG system details
- `similarity_service/README.md` - Search system details

---

## ⚡ Super Quick Start

```bash
# Install dependencies (one time)
uv sync

# Set up environment (one time)
source env_setup.sh

# Run RAG system
./run_rag.sh

# OR run Similarity Search
./run_search.sh
```

That's it! 🎉

