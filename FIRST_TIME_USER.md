# Welcome! First Time User Guide

## Never used this before? Follow these simple steps!

### Super Quick Start (3 steps)

```bash
# Step 1: Install dependencies
uv sync

# Step 2: Setup API key
cp env_setup.sh.example env_setup.sh
nano env_setup.sh  # Replace YOUR_API_KEY_HERE with your actual key
source env_setup.sh

# Step 3: Run!
./main.sh
```

**That's it!** Choose option 1 or 2 and follow the prompts.

---

## What You Need

### Before You Start

1. **Get Google Gemini API Key** (free):
   
   **Quick version:**
   - Go to: https://ai.google.dev/pricing?hl=pl#1_5flash
   - Click "Try it now in Google AI Studio"
   - Click "Get API Key" → "Create API Key"
   - Copy the key 
   
   **Detailed instructions with screenshots:** See [API_KEY_SETUP.md](API_KEY_SETUP.md)

2. **For Steam Game Search only**: Install Docker Desktop
   - Download: https://www.docker.com/products/docker-desktop/
   - Install and start it
   - Windows users: Enable WSL2 integration in settings

### Check If You Have Required Tools

```bash
# Check Python
python --version  # Should be 3.11+

# Check uv
uv --version  # If missing: curl -LsSf https://astral.sh/uv/install.sh | sh

# Check Docker (for game search only)
docker --version
```

---

## Choose Your System

### Option 1: AI Basics RAG Service (Easier)
**Try it:**
```bash
./main.sh
# Choose option 1
```

### Option 2: Steam Game Search Service
**Try it:**
```bash
./main.sh
# Choose option 2
```

---

## Common First-Time Issues

### "GOOGLE_API_KEY not found"

You forgot step 2!

```bash
# Create config file
cp env_setup.sh.example env_setup.sh

# Edit it
nano env_setup.sh  # Add your API key

# Load it
source env_setup.sh
```

### "Docker not available" (Game Search only)

1. Install Docker Desktop
2. Start Docker Desktop  
3. Windows: Enable WSL2 integration
4. Restart terminal

### "ModuleNotFoundError"

You forgot step 1!

```bash
uv sync
```

---

## What to Expect

### First Run - AI Basics RAG
```
 RAG System
First Time Setup Detected

 Downloading PDF... (30 seconds)
 Generating embeddings... (5-10 minutes)
 Done!

 Interactive Chat Mode
 Your question: What is AI?
 Answer: Systems that mimic human intelligence...

 Your question: quit
 Goodbye!
```

### First Run - Steam Game Search
```
 SIMILARITY SEARCH SYSTEM
 Checking Docker... 
 Checking database... Starting...
  No games in database
 Load sample data? yes

 Loading 200 games... (2-3 minutes)
 Done!

 What game are you looking for? RPG
 Max price: 20
 Found 5 games...
```

## Need Help?

### Check Documentation
1. **This file** – First-time setup
2. **README.md** – Architecture overview + doc roadmap
3. **QUICKSTART.md** – Detailed quick start
4. **CONSOLE_GUIDE.md** – All commands

### Common Questions

**Q: Which system should I try first?**
A: AI Basics RAG - it's easier (no Docker needed)

**Q: How much does it cost?**
A: Free! Gemini API has generous free tier

**Q: Do I need a GPU?**
A: No, works fine on CPU

**Q: Can I use my own documents/data?**
A: Yes! Check the respective README files for instructions

---

## Checklist

Before running, make sure you have:

- [ ] Cloned the repository
- [ ] Ran `uv sync`
- [ ] Created `env_setup.sh` from example
- [ ] Added your Google API key
- [ ] Ran `source env_setup.sh`
- [ ] (Optional) Installed Docker Desktop

All done? Run:
```bash
./main.sh
```

---

**Enjoy exploring vector search and RAG systems!** 

*If you get stuck, open `QUICKSTART.md` for the full walkthrough or `CONSOLE_GUIDE.md` for command-by-command help.*

