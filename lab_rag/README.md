# RAG System - Documentation

RAG (Retrieval-Augmented Generation) system using Milvus vector database and Google Gemini API to answer questions based on PDF documents.

## File Structure

```
lab_rag/
├── ex6.ipynb                    # Original Jupyter notebook (preserved unchanged)
├── milvus_rag_interface.py      # RAG interface class
├── main.py                      # Main demonstration script
├── milvus_db/                   # Milvus configuration and data
│   ├── docker-compose.yml       # Docker Compose for Milvus database
│   ├── data/                    # Storage for PDFs, JSONs and embeddings
│   └── volumes/                 # Milvus database data
└── README.md                    # This documentation
```

## Prerequisites

### 1. Start Milvus Database

```bash
cd /home/jarek/AGH/IPUM/IPUM_Lab02/lab_rag/milvus_db
docker compose up -d
```

Check if containers are running:
```bash
docker ps
```

You should see:
- `milvus-standalone` (port 19530)
- `milvus-minio` (ports 9000, 9001)
- `milvus-etcd` (port 2379)

### 2. Set Google Gemini API Key and Model

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

**Option A: Use the provided env_setup.sh file (Recommended)**

The project includes an `env_setup.sh` file in the main directory. Edit it with your API key:

```bash
# Edit the file with your API key
nano ../env_setup.sh

# Then source it to load environment variables
source ../env_setup.sh
```

**Option B: Export manually**

```bash
export GOOGLE_API_KEY="your_api_key_here"
export GEMINI_MODEL="gemini-2.0-flash-exp"
```

**Note:** The `env_setup.sh` file is already in `.gitignore` to prevent accidentally committing your API key.

### 3. Install Dependencies

```bash
cd /home/jarek/AGH/IPUM/IPUM_Lab02
uv sync
```

## Usage

### Method 1: Run main.py Script

```bash
# From project root directory
cd /home/jarek/AGH/IPUM/IPUM_Lab02

# Load environment variables
source env_setup.sh

# Run the RAG system
cd lab_rag
python main.py
```

The script will automatically:
1. Connect to Milvus database
2. Create collection (if it doesn't exist)
3. Download and process PDF document
4. Generate embeddings
5. Execute example RAG queries
6. Offer interactive mode for custom questions

### Method 2: Use as Library in Your Own Code

```python
from milvus_rag_interface import MilvusRAGInterface

# Initialize
rag = MilvusRAGInterface(
    host="localhost",
    port="19530",
    embedding_model_name="ipipan/silver-retriever-base-v1.1",
    gemini_model_name="gemini-2.0-flash"
)

# Create collection
rag.create_collection("my_collection")

# Process document
rag.process_document(
    pdf_url="https://example.com/document.pdf",
    file_name="document.pdf",
    file_json="document.json",
    embeddings_json="document-embeddings.json",
    collection_name="my_collection"
)

# Ask a question (Polish document example)
response = rag.rag("Czym jest sztuczna inteligencja?", collection_name="my_collection", language="pl")
print(response)

# For English documents, use language="en"
# response = rag.rag("What is artificial intelligence?", collection_name="my_collection", language="en")
```

## Available Methods of MilvusRAGInterface Class

### Collection Management
- `create_collection(collection_name, schema_description)` - Create a new collection
- `drop_collection(collection_name)` - Delete a collection

### Document Processing
- `download_pdf(pdf_url, file_name)` - Download PDF
- `extract_pdf_text(file_name, file_json)` - Extract text from PDF
- `generate_embeddings(file_json, embeddings_json)` - Generate embeddings
- `insert_embeddings(file_json, embeddings_json, collection_name)` - Insert into database
- `process_document(...)` - Execute complete pipeline in one step

### Search and RAG
- `search(query, collection_name, limit)` - Search for similar texts
- `generate_response(prompt)` - Generate response via Gemini
- `build_prompt(context, question, language)` - Build prompt for Gemini (supports "pl" and "en")
- `rag(query, collection_name, language)` - Main RAG method (retrieve + generate)

## Example Use Cases

### 1. Search Only (Without Response Generation)

```python
rag = MilvusRAGInterface()
results = rag.search("artificial intelligence", limit=3)

for hit in results[0]:
    print(f"Distance: {hit['distance']}")
    print(f"Text: {hit['entity']['text'][:200]}...")
```

### 2. Processing Multiple Documents

```python
rag = MilvusRAGInterface()
rag.create_collection("documents_collection")

documents = [
    ("https://example.com/doc1.pdf", "doc1.pdf"),
    ("https://example.com/doc2.pdf", "doc2.pdf"),
]

for url, filename in documents:
    json_name = filename.replace(".pdf", ".json")
    emb_name = filename.replace(".pdf", "-embeddings.json")
    
    rag.process_document(url, filename, json_name, emb_name, "documents_collection")
```

### 3. Resetting Collection

```python
rag = MilvusRAGInterface()
rag.drop_collection("rag_texts_and_embeddings")
rag.create_collection("rag_texts_and_embeddings")
# Then reprocess documents
```

## Troubleshooting

### Problem: "Connection refused" when connecting to Milvus

**Solution:**
```bash
cd /home/jarek/AGH/IPUM/IPUM_Lab02/lab_rag/milvus_db
docker compose up -d
docker ps  # Check if containers are running
```

### Problem: "GOOGLE_API_KEY not found"

**Solution:**
```bash
export GOOGLE_API_KEY="your_api_key_here"
# Or add to ~/.bashrc for persistence
```

### Problem: "CUDA capability sm_120 is not compatible"

**Solution:** This is normal for RTX 5070 Ti. Code automatically uses CPU.
If you want to force GPU (after updating PyTorch), change in class:
```python
DEVICE = "cuda"  # Instead of "cpu"
```

### Problem: Slow embedding generation

**Solution:** This is normal when using CPU. For 100+ pages it may take several minutes.
Consider using GPU with compatible PyTorch version or a smaller model.

## Comparison with ex6.ipynb

| Feature | ex6.ipynb | New Code (Class) |
|---------|-----------|------------------|
| **Structure** | Sequential cells | Object-oriented class |
| **Reusability** | Low | High (import and use) |
| **Testing** | Difficult | Easy (testable methods) |
| **Integration** | Manual copy-paste | Import as module |
| **Maintenance** | Everything in one place | Separated responsibilities |

Notebook `ex6.ipynb` remains as:
- Development process documentation
- Educational material showing step-by-step process
- Prototype for quick testing

## System Architecture

```
┌─────────────┐
│   main.py   │  ← User runs the script
└──────┬──────┘
       │
       v
┌──────────────────────────────┐
│ MilvusRAGInterface (class)   │
├──────────────────────────────┤
│ • Milvus Client               │ ←→ Milvus DB (localhost:19530)
│ • Sentence Transformer Model  │
│ • Gemini API Client           │ ←→ Google Gemini API
└──────────────────────────────┘
       │
       v
┌──────────────────┐
│  Milvus Storage  │
│  - Texts         │
│  - Embeddings    │
│  - HNSW Indexes  │
└──────────────────┘
```

## How It Works

### Step-by-Step Process

1. **Document Download**
   - PDF is downloaded from URL to local storage

2. **Text Extraction**
   - PyMuPDF (fitz) extracts text from each PDF page
   - Saved to JSON: `[{"page_num": 0, "text": "..."}, ...]`

3. **Embedding Generation**
   - SentenceTransformer model converts text to 768-dimensional vectors
   - Each page gets its semantic embedding
   - Saved to JSON: `[{"page_num": 0, "embedding": [0.1, 0.2, ...]}, ...]`

4. **Database Insertion**
   - Text and embeddings inserted into Milvus
   - HNSW index created for fast similarity search

5. **RAG Query Processing**
   - User question is converted to embedding
   - Milvus searches for most similar document fragments (L2 distance)
   - Retrieved context is sent to Gemini with the question
   - Gemini generates answer based on context

### Why This Works

- **Vector Embeddings**: Capture semantic meaning of text
- **Similarity Search**: Finds relevant content even with different wording
- **Context Augmentation**: Provides AI with specific knowledge
- **Response Generation**: Gemini creates natural language answers

## Advanced Configuration

### Using Different Models

```python
# For English documents
rag = MilvusRAGInterface(
    embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# For multilingual documents
rag = MilvusRAGInterface(
    embedding_model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Different Gemini model
rag = MilvusRAGInterface(
    gemini_model_name="gemini-1.5-pro"
)
```

### Custom Collection Schema

```python
# Modify in milvus_rag_interface.py if needed
VECTOR_LENGTH = 384  # For smaller models
```

### Changing Search Parameters

```python
# In search method, modify:
result = self.milvus_client.search(
    collection_name=collection_name, 
    data=[embedded_query], 
    limit=5,  # Return top 5 results instead of 1
    search_params={"metric_type": "COSINE"},  # Use cosine similarity
    output_fields=["text"]
)
```

## Performance Optimization

### Speed Improvements

1. **Use GPU** (if compatible PyTorch available):
   ```python
   DEVICE = "cuda"
   ```

2. **Batch Processing**:
   Process multiple queries at once for better throughput

3. **Index Tuning**:
   Adjust HNSW parameters in `create_collection`:
   ```python
   params={"M": 16, "efConstruction": 200}  # Higher accuracy, slower
   params={"M": 4, "efConstruction": 64}    # Faster, lower accuracy
   ```

### Memory Optimization

- Process large PDFs in chunks
- Use smaller embedding models
- Clear collection cache when not needed

## Next Steps

1. **API Integration** - Use the class in Flask/FastAPI service
2. **Caching** - Add cache for frequently asked questions
3. **Monitoring** - Add logging and metrics
4. **Multi-document** - Extend to handle multiple documents with metadata
5. **UI** - Create web interface (Gradio/Streamlit)
6. **Authentication** - Add user authentication and query logging
7. **Evaluation** - Implement RAG quality metrics (relevance, accuracy)


## Resources

- [Milvus Documentation](https://milvus.io/docs)
- [Sentence Transformers](https://www.sbert.net/)
- [Google Gemini API](https://ai.google.dev/)
- [RAG Explained](https://www.promptingguide.ai/techniques/rag)
