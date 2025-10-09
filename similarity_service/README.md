# Similarity Search Service

Semantic similarity search system for games and images using PostgreSQL with pgvectorscale extension.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│  Steam Games Dataset (40,000 games)             │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│  SentenceTransformer Model                      │
│  (distiluse-base-multilingual-cased-v2)        │
│  → Generates 512-dim embeddings                 │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│  PostgreSQL + pgvectorscale                     │
│  - Tables: games, images                        │
│  - Vector operations: cosine_distance           │
│  - SQL filters: price, platform, etc.           │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│  Query API (game_queries.py)                    │
│  - Semantic search                              │
│  - Filter by price, platform, similarity score  │
└─────────────────────────────────────────────────┘
```

## 📋 Prerequisites

1. **Docker Desktop** with WSL2 integration enabled
2. **Python 3.11+** with `uv` package manager
3. **Dependencies** installed: `cd /home/jarek/AGH/IPUM/IPUM_Lab02 && uv sync`

## 🚀 Quick Start

### Method 1: Using the automated script

```bash
# From project root
cd /home/jarek/AGH/IPUM/IPUM_Lab02
./run_similarity_service.sh
```

### Method 2: Manual step-by-step

#### Step 1: Start PostgreSQL database

```bash
cd vectorscale_db
docker compose up -d
```

Check if running:
```bash
docker ps | grep vectorscaledb
```

#### Step 2: Initialize database tables

```bash
cd ../similarity_service
uv run python main.py
```

You should see:
```
Database tables created successfully!
```

#### Step 3: Load game data (optional, takes ~30 minutes)

```bash
uv run python tests/test_games.py
```

This will:
- Download 40,000 games from Steam dataset
- Generate embeddings for each game description
- Insert into PostgreSQL

**Note:** This step takes significant time. You can:
- Reduce the number: Edit `test_games.py` and change `40000` to `1000`
- Skip and just test the search functionality

#### Step 4: Run demo searches

```bash
uv run python demo_search.py
```

## 📁 File Structure

```
similarity_service/
├── database.py          # Database connection configuration
├── models.py            # SQLAlchemy ORM models (Games, Images)
├── embeddings.py        # Embedding generation using SentenceTransformer
├── queries.py           # Image similarity queries
├── game_queries.py      # Game similarity queries with filters
├── main.py              # Database initialization script
├── demo_search.py       # Interactive demo (NEW)
└── tests/
    ├── test_queries.py  # Test image similarity
    └── test_games.py    # Load and test game data
```

## 🔍 Usage Examples

### Example 1: Find cheap RPG games

```python
from game_queries import find_similar_games

games = find_similar_games(
    "epic fantasy RPG with dragons and magic",
    max_price=10.0,
    limit=5
)

for game in games:
    print(f"{game.name} - ${game.price}")
```

### Example 2: Find Linux strategy games

```python
games = find_similar_games(
    "real-time strategy game with base building",
    linux=True,
    min_score=0.4,  # Minimum similarity score
    limit=5
)
```

### Example 3: Find free puzzle games

```python
games = find_similar_games(
    "relaxing puzzle game",
    max_price=0.0,  # Free games only
    limit=10
)
```

### Example 4: Platform-specific search

```python
# Windows games only
games = find_similar_games(
    "first-person shooter",
    windows=True,
    max_price=30.0
)

# Mac games only
games = find_similar_games(
    "indie platformer",
    mac=True
)
```

## 🎮 Interactive Demo

Run the interactive search demo:

```bash
cd /home/jarek/AGH/IPUM/IPUM_Lab02/similarity_service
uv run python demo_search.py
```

The demo will:
1. Show 4 example searches with different filters
2. Enter interactive mode where you can:
   - Describe the game you're looking for
   - Set optional filters (price, platform)
   - See top 5 similar games

## 🧪 Testing

### Test image similarity search

```bash
uv run python tests/test_queries.py
```

This will:
- Insert 100 test images with random embeddings
- Find 5 most similar images to the first one
- Demonstrate cosine similarity search

### Test game similarity search

```bash
uv run python tests/test_games.py
```

This will:
- Load games from Steam dataset
- Test searches with various filters
- Display results

## 🔧 Configuration

### Database connection

Edit `database.py` to change connection settings:

```python
def get_db_url():
    return URL.create(
        drivername="postgresql+psycopg",
        username="postgres",
        password="password",
        host="localhost",
        port=5556,
        database="similarity_search_service_db"
    )
```

### Embedding model

Edit `embeddings.py` to use a different model:

```python
model = SentenceTransformer(
    "distiluse-base-multilingual-cased-v2",  # Change this
    device=device
)
```

Other good models:
- `all-MiniLM-L6-v2` - Faster, English only
- `paraphrase-multilingual-MiniLM-L12-v2` - Multilingual
- `all-mpnet-base-v2` - Higher quality, slower

## 🛑 Stopping the Service

```bash
cd /home/jarek/AGH/IPUM/IPUM_Lab02/vectorscale_db
docker compose down
```

To also remove data:
```bash
docker compose down -v
```

## 🐛 Troubleshooting

### Database connection failed

**Problem:** `Connection refused` or `could not connect to server`

**Solution:**
1. Check if Docker Desktop is running
2. Verify WSL2 integration is enabled
3. Check if container is running: `docker ps`
4. Check logs: `docker logs vectorscaledb`

### No games found in search

**Problem:** Search returns empty results

**Solution:**
1. Check if data is loaded: Run `demo_search.py` - it shows game count
2. Load data: `uv run python tests/test_games.py`
3. Check database: 
   ```bash
   docker exec vectorscaledb psql -U postgres -d similarity_search_service_db -c "SELECT COUNT(*) FROM games;"
   ```

### Slow embedding generation

**Problem:** Loading games takes very long

**Solution:**
1. Reduce dataset size in `test_games.py`: Change `40000` to `1000`
2. Use GPU if available: Model automatically uses CUDA if available
3. Use smaller model in `embeddings.py`

### Import errors

**Problem:** `ModuleNotFoundError`

**Solution:**
```bash
cd /home/jarek/AGH/IPUM/IPUM_Lab02
uv sync  # Reinstall dependencies
```

## 📊 Performance Tips

1. **Create indexes** on frequently filtered columns:
   ```sql
   CREATE INDEX idx_games_price ON games(price);
   CREATE INDEX idx_games_platforms ON games(windows, linux, mac);
   ```

2. **Batch inserts** for large datasets (already implemented in `game_queries.py`)

3. **Use appropriate similarity metric**:
   - `cosine_distance` - Best for semantic similarity (current)
   - `l2_distance` - Euclidean distance
   - `inner_product` - Dot product similarity

## 🔗 Related Components

- **vectorscale_db/**: PostgreSQL + pgvectorscale database setup
- **lab_rag/**: RAG system using Milvus (alternative vector database)

## 📚 Learn More

- [pgvector documentation](https://github.com/pgvector/pgvector)
- [pgvectorscale documentation](https://github.com/timescale/pgvectorscale)
- [Sentence Transformers](https://www.sbert.net/)
- [Steam Games Dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset)

