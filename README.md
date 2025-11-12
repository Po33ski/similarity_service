# Retrieval-Augmented Generation Sample Project

This repository showcases two complementary Retrieval-Augmented Generation (RAG) implementations: one powered by Milvus Lite and Google Gemini, the other backed by PostgreSQL with the VectorScale extension. The goal is to demonstrate how vector databases, embeddings, and large language models can be combined to answer questions or search semantically through domain data. Convenience launchers are provided for both Bash and PowerShell so that Linux, macOS, and Windows users can start the demos with a single command. PowerShell scripts mirror the Bash wrappers—simply run them from a `pwsh` session (for example, `pwsh -File main.ps1`, `run_rag.ps1`, or `run_search.ps1`) to select and execute the same workflows without relying on WSL.

The repository is organised around three core folders:
- `lab_rag/` – Milvus-based RAG service ingesting PDFs and answering questions.
- `similarity_service/` – PostgreSQL-based semantic search service for video games.
- `vectorscale_db/` – Docker Compose setup that provisions TimescaleDB with the VectorScale extension and initialises the vector-ready database used by the search service.

## Documentation Roadmap

Follow these files in order to prepare your environment and run the demos:
1. `API_KEY_SETUP.md` – request a Gemini API key and configure environment variables.
2. `FIRST_TIME_USER.md` – complete first-run checklist and launch the main menu.
3. `QUICKSTART.md` – review detailed usage tips and alternative launch paths.
4. `CONSOLE_GUIDE.md` – keep this handy for command-by-command references once you are comfortable with the basics.

## Milvus RAG System (`lab_rag/`)

The Milvus pipeline focuses on document-driven Q&A:
- **Document ingestion** – `main.py` downloads the reference PDF (an AI guide) into `milvus_db/data` and keeps JSON artefacts for text and embeddings so repeated runs are faster.
- **Text extraction** – `MilvusRAGInterface.extract_pdf_text` uses PyMuPDF to split the PDF into page-level JSON records.
- **Embedding generation** – `MilvusRAGInterface.generate_embeddings` encodes each page with the Polish-friendly model `ipipan/silver-retriever-base-v1.1` on CPU, storing 768‑dimensional vectors.
- **Vector storage** – `MilvusRAGInterface.create_collection` prepares a Milvus Lite collection with a float vector field and an AUTOINDEX configuration. `insert_embeddings` batches `{text, embedding}` rows and loads the collection for fast search.
- **Query workflow** – `MilvusRAGInterface.rag` embeds the user question, retrieves the closest pages via Milvus, builds a language-aware prompt, and calls Google Gemini through the official SDK to stream the final answer.
- **Interactive CLI** – `main.py` includes an intelligent menu: the first run performs the full pipeline automatically, later runs let you refresh embeddings or jump straight into the chat loop backed by the cached vectors.

**Workflow schematic**
```
User question
    │
    ▼
Interactive menu (main.py)
    │
    ├─ if first run → download & embed PDF → insert into Milvus
    │
    ▼
MilvusRAGInterface.rag()
    │
    ├─ embed query with SentenceTransformer
    ├─ search Milvus Lite collection
    ├─ build language-aware prompt
    └─ call Gemini for the final answer
```
The CLI orchestrates ingestion on demand and funnels every query through Milvus for context retrieval before delegating answer generation to Gemini.

Together these steps illustrate an end-to-end RAG workflow built around a PDF knowledge base, Milvus Lite as the semantic store, and Gemini as the language model.

## Similarity Search Service (`similarity_service/`)

The second system highlights semantic search on a structured dataset:
- **Database provisioning** – `main_search.py` checks Docker availability and starts the container defined in `vectorscale_db/docker-compose.yml`. The initialisation script creates `similarity_search_service_db` and enables the `vectorscale` extension so the `vector` type and cosine operators are ready to use.
- **Schema definition** – `models.Games` stores game metadata plus a 512‑dimension `pgvector` column. SQLAlchemy maps this field directly, allowing `.cosine_distance()` ordering inside ORM queries.
- **Embedding pipeline** – `embeddings.generate_embedding` relies on `distiluse-base-multilingual-cased-v2` to produce description embeddings on CPU, returning zero vectors for missing text to keep inserts fault-tolerant.
- **Data loading** – `game_queries.insert_games` downloads a sample from the HuggingFace Steam dataset, skips incomplete entries, embeds each description, and persists rows one by one with a progress bar. Larger batches can be loaded via `tests/test_games.py`.
- **Search experience** – `game_queries.find_similar_games` encodes the query, sorts by cosine distance in SQL, and applies optional filters (price ceiling, Windows/Linux/macOS flags, minimum similarity). `interactive_search` in `main_search.py` wraps this in a conversational CLI.
- **Supporting folder** – `vectorscale_db/` keeps everything PostgreSQL-related in one place: Docker Compose, initial SQL scripts, and persistent volumes if you choose to mount them. Stopping the service is as simple as `docker compose down` inside that folder.

**Workflow schematic**
```
User search prompt
    │
    ▼
interactive_search() (main_search.py)
    │
    ├─ ensure Docker & vectorscaledb container are running
    ├─ optionally load sample games with embeddings
    │
    ▼
find_similar_games()
    │
    ├─ embed prompt (SentenceTransformer)
    ├─ SQL ORDER BY cosine_distance on pgvector column
    ├─ apply price/platform filters
    └─ return top matches with metadata
```
The console flow guarantees the database is available, optionally seeds it with demo data, and then issues cosine-ranked SQL queries that surface the closest-matching games together with actionable filters.

This service demonstrates how a relational database equipped with VectorScale can function as a high-performance vector store, driving semantic discovery in a catalogue-like scenario such as video game recommendations.


