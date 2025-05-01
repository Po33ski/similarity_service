from milvus_setup import setup_milvus
from document_processor import process_pdf
from embeddings import EmbeddingModel
from rag_service import RAGService

def main():
    # Initialize components
    milvus = setup_milvus()
    embedder = EmbeddingModel()
    
    # Process PDF document
    pdf_url = "https://www.iab.org.pl/wp-content/uploads/2024/04/Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.pdf"
    local_pdf = "./data/document.pdf"
    json_output = "./data/pages.json"
    
    download_pdf(pdf_url, local_pdf)  # Implement download function
    process_pdf(local_pdf, json_output)
    
    # Generate and insert embeddings
    with open(json_output) as f:
        pages = json.load(f)
    
    texts = [p["text"] for p in pages]
    embeddings = embedder.embed_batch(texts)
    
    data = [
        {"page_num": p["page_num"], "text": p["text"], "embedding": emb}
        for p, emb in zip(pages, embeddings)
    ]
    
    milvus.insert("rag_docs", data)
    milvus.load_collection("rag_docs")
    
    # Initialize RAG
    rag = RAGService(milvus, embedder)
    
    # Example query
    query = "Jakie są główne zastosowania sztucznej inteligencji w marketingu?"
    print(rag.generate_response(query))

if __name__ == "__main__":
    main()