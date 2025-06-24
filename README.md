# Vector Search and RAG Applications in MLOps
This project dives into vector search, vector databases (Milvus), and vector indexes (Postgres with pgvectorscale), demonstrating their real-world applications in similarity search and Retrieval-Augmented Generation (RAG) within an MLOps context.

I've implemented two distinct approaches: leveraging PostgreSQL with TimescaleDB and the pgvectorscale/pgvector extensions for scalable vector indexing, and a dedicated Milvus vector database. Both setups use SQLAlchemy for database interaction. For text embedding, I employed Sentence Transformers' distiluse-base-multilingual-cased-v2 for general vector search (e.g., on game descriptions) and ipipan/silver-retriever-base-v1.1 (a Polish-specific model) for the Milvus-based RAG system.

Crucially, the Milvus RAG implementation integrates the Gemini API to generate context-aware responses. This project emphasizes practical deployment, requiring Docker for environment setup.

**Necessary software**
- [Docker and Docker Compose](https://docs.docker.com/engine/install/), 
  also [see those post-installation notes](https://docs.docker.com/engine/install/linux-postinstall/)
- Postgres client, e.g. `sudo apt install postgresql-client`
  ([more details](https://askubuntu.com/questions/1040765/how-to-install-psql-without-postgres))
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.11

Note that you should also activate `uv` project and install dependencies with `uv sync`.

**Lab**

See [lab instruction](LAB_INSTRUCTION.md).

**Homework**

See [homework instruction](HOMEWORK.md).

**Data**

We will be using [Steam Games Dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset)
about games published on Steam, as well as
[Amazon Berkeley Objects (ABO) Dataset](https://amazon-berkeley-objects.s3.amazonaws.com/index.html)
with data about objects available in the Amazon store.
