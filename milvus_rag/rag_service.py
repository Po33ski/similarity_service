from typing import List
import google.generativeai as genai
from pymilvus import MilvusClient

class RAGService:
    def __init__(self, milvus_client: MilvusClient, embedding_model):
        self.milvus = milvus_client
        self.embedding_model = embedding_model
        genai.configure(api_key="YOUR_API_KEY")  # Set in config.py
        self.llm = genai.GenerativeModel('gemini-pro')
    
    def retrieve(self, query: str, k: int = 3) -> List[dict]:
        query_embedding = self.embedding_model.embed_text(query)
        results = self.milvus.search(
            collection_name="rag_docs",
            data=[query_embedding],
            limit=k,
            output_fields=["text", "page_num"]
        )
        return [hit["entity"] for hit in results[0]]
    
    def generate_response(self, query: str) -> str:
        context_chunks = self.retrieve(query)
        context = "\n\n".join(
            f"Fragment ze strony {chunk['page_num']}:\n{chunk['text']}"
            for chunk in context_chunks
        )
        
        prompt = f"""Na podstawie poniższych fragmentów dokumentu odpowiedz na pytanie.
        
        Kontekst:
        {context}
        
        Pytanie: {query}
        Odpowiedź:"""
        
        response = self.llm.generate_content(prompt)
        return response.text