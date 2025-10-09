import os
import requests
import fitz
import json
import torch
from pymilvus import MilvusClient, FieldSchema, DataType, CollectionSchema
from sentence_transformers import SentenceTransformer
from google import genai


class MilvusRAGInterface:
    """
    Interface for RAG (Retrieval-Augmented Generation) system using Milvus vector database
    and Google Gemini API for response generation.
    """
    
    VECTOR_LENGTH = 768
    DATA_DIR = "./milvus_db/data"
    DEVICE = "cpu"  # Change to "cuda" if GPU is available and compatible
    DEFAULT_COLLECTION_NAME = "rag_texts_and_embeddings"
    
    def __init__(
        self, 
        host="localhost", 
        port="19530", 
        embedding_model_name="ipipan/silver-retriever-base-v1.1",
        gemini_model_name=None
    ):
        """
        Initialize the RAG interface with Milvus client and embedding model.
        
        Args:
            host: Milvus server host or path to Milvus Lite database file
            port: Milvus server port (use None for Milvus Lite)
            embedding_model_name: Name of the sentence transformer model for embeddings
            gemini_model_name: Name of the Gemini model for response generation 
                              (defaults to GEMINI_MODEL env var or "gemini-2.0-flash-exp")
        """
        # Get Gemini model name from environment variable or use default
        if gemini_model_name is None:
            gemini_model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        # Initialize Milvus client
        if port is None or host.endswith('.db'):
            # Use Milvus Lite (embedded, file-based)
            self.milvus_client = MilvusClient(uri=host)
            self.is_lite = True
            print(f"Using Milvus Lite (embedded mode) at: {host}")
        else:
            # Use Milvus server
            self.milvus_client = MilvusClient(host=host, port=port)
            self.is_lite = False
            print(f"Connecting to Milvus server at {host}:{port}")
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(
            embedding_model_name, 
            device=MilvusRAGInterface.DEVICE
        )
        
        # Initialize Gemini API
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if google_api_key:
            self.genai_client = genai.Client(api_key=google_api_key)
            self.gemini_model_name = gemini_model_name
            print(f"Using Gemini model: {gemini_model_name}")
        else:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
            print("RAG functionality will not work without it.")
            self.genai_client = None
            self.gemini_model_name = None
    
    def create_collection(
        self, 
        collection_name=None,
        schema_description="RAG Texts collection"
    ):
        """
        Create a new Milvus collection for RAG texts and embeddings.
        
        Args:
            collection_name: Name of the collection (default: rag_texts_and_embeddings)
            schema_description: Description of the collection schema
        """
        if collection_name is None:
            collection_name = MilvusRAGInterface.DEFAULT_COLLECTION_NAME
            
        if self.milvus_client.has_collection(collection_name):
            print(f"Collection '{collection_name}' already exists.")
            return
        
        # Define schema fields
        id_field = FieldSchema(
            name="id", 
            dtype=DataType.INT64, 
            is_primary=True, 
            description="Primary id"
        )
        text_field = FieldSchema(
            name="text", 
            dtype=DataType.VARCHAR, 
            max_length=4096, 
            description="Page text"
        )
        embedding_field = FieldSchema(
            name="embedding", 
            dtype=DataType.FLOAT_VECTOR, 
            dim=MilvusRAGInterface.VECTOR_LENGTH, 
            description="Embedded text"
        )
        
        fields = [id_field, text_field, embedding_field]
        schema = CollectionSchema(
            fields=fields, 
            auto_id=True, 
            enable_dynamic_field=True, 
            description=schema_description
        )
        
        # Create collection
        self.milvus_client.create_collection(
            collection_name=collection_name,
            schema=schema
        )
        
        # Create index for fast similarity search
        index_params = self.milvus_client.prepare_index_params()
        
        if self.is_lite:
            # Milvus Lite only supports FLAT, IVF_FLAT, and AUTOINDEX
            index_params.add_index(
                field_name="embedding", 
                index_type="AUTOINDEX",
                metric_type="L2"
            )
            print("Using AUTOINDEX (Milvus Lite mode)")
        else:
            # Milvus server supports HNSW for better performance
            index_params.add_index(
                field_name="embedding", 
                index_type="HNSW",
                metric_type="L2",
                params={"M": 4, "efConstruction": 64}
            )
            print("Using HNSW index")
        
        self.milvus_client.create_index(
            collection_name=collection_name,
            index_params=index_params
        )
        
        print(f"Collection '{collection_name}' created successfully!")
        print(f"Available collections: {self.milvus_client.list_collections()}")
    
    def drop_collection(self, collection_name=None):
        """
        Drop (delete) a Milvus collection.
        
        Args:
            collection_name: Name of the collection to drop
        """
        if collection_name is None:
            collection_name = MilvusRAGInterface.DEFAULT_COLLECTION_NAME
            
        if self.milvus_client.has_collection(collection_name):
            print(f"Dropping collection: {collection_name}")
            self.milvus_client.drop_collection(collection_name)
            print("Collection dropped successfully")
        else:
            print(f"Collection '{collection_name}' doesn't exist")
    
    def clear_collection(self, collection_name=None):
        """
        Clear all data from a Milvus collection by dropping and recreating it.
        
        Args:
            collection_name: Name of the collection to clear
        """
        if collection_name is None:
            collection_name = MilvusRAGInterface.DEFAULT_COLLECTION_NAME
        
        print(f"Clearing collection: {collection_name}")
        self.drop_collection(collection_name)
        self.create_collection(collection_name)
        print(f"Collection '{collection_name}' cleared and recreated")
    
    def count_entries(self, collection_name=None):
        """
        Count the number of entries in a collection.
        
        Args:
            collection_name: Name of the collection to count
            
        Returns:
            Number of entries in the collection
        """
        if collection_name is None:
            collection_name = MilvusRAGInterface.DEFAULT_COLLECTION_NAME
        
        if not self.milvus_client.has_collection(collection_name):
            return 0
        
        try:
            stats = self.milvus_client.get_collection_stats(collection_name)
            return stats.get('row_count', 0)
        except:
            return 0
    
    def download_pdf(self, pdf_url, file_name):
        """
        Download a PDF file from a URL.
        
        Args:
            pdf_url: URL of the PDF file
            file_name: Local filename to save the PDF
        """
        print(f"Downloading PDF from {pdf_url}...")
        response = requests.get(pdf_url, stream=True)
        
        # Create data directory if it doesn't exist
        os.makedirs(MilvusRAGInterface.DATA_DIR, exist_ok=True)
        
        file_path = os.path.join(MilvusRAGInterface.DATA_DIR, file_name)
        with open(file_path, "wb") as file:
            for block in response.iter_content(chunk_size=1024):
                if block:
                    file.write(block)
        
        print(f"PDF downloaded successfully: {file_path}")
    
    def extract_pdf_text(self, file_name, file_json):
        """
        Extract text from PDF file and save to JSON.
        
        Args:
            file_name: Name of the PDF file
            file_json: Name of the output JSON file
        """
        print(f"Extracting text from {file_name}...")
        pdf_path = os.path.join(MilvusRAGInterface.DATA_DIR, file_name)
        document = fitz.open(pdf_path)
        pages = []
        
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            page_text = page.get_text()
            pages.append({"page_num": page_num, "text": page_text})
        
        json_path = os.path.join(MilvusRAGInterface.DATA_DIR, file_json)
        with open(json_path, "w") as file:
            json.dump(pages, file, indent=4, ensure_ascii=False)
        
        print(f"Text extracted to {json_path} ({len(pages)} pages)")
    
    def generate_embeddings(self, file_json, embeddings_json):
        """
        Generate embeddings for text pages and save to JSON.
        
        Args:
            file_json: Name of the JSON file with extracted text
            embeddings_json: Name of the output JSON file for embeddings
        """
        print(f"Generating embeddings from {file_json}...")
        json_path = os.path.join(MilvusRAGInterface.DATA_DIR, file_json)
        
        with open(json_path, "r") as file:
            data = json.load(file)
        
        pages = [page["text"] for page in data]
        embeddings = self.embedding_model.encode(pages)
        
        embeddings_paginated = []
        for page_num in range(len(embeddings)):
            embeddings_paginated.append({
                "page_num": page_num, 
                "embedding": embeddings[page_num].tolist()
            })
        
        embeddings_path = os.path.join(MilvusRAGInterface.DATA_DIR, embeddings_json)
        with open(embeddings_path, "w") as file:
            json.dump(embeddings_paginated, file, indent=4, ensure_ascii=False)
        
        print(f"Embeddings generated and saved to {embeddings_path}")
    
    def insert_embeddings(self, file_json, embeddings_json, collection_name=None):
        """
        Insert text and embeddings into Milvus collection.
        
        Args:
            file_json: Name of the JSON file with extracted text
            embeddings_json: Name of the JSON file with embeddings
            collection_name: Name of the collection to insert into
        """
        if collection_name is None:
            collection_name = MilvusRAGInterface.DEFAULT_COLLECTION_NAME
            
        print(f"Inserting embeddings into collection '{collection_name}'...")
        
        text_path = os.path.join(MilvusRAGInterface.DATA_DIR, file_json)
        embeddings_path = os.path.join(MilvusRAGInterface.DATA_DIR, embeddings_json)
        
        with open(text_path, "r") as t_f, open(embeddings_path, "r") as e_f:
            text_data = json.load(t_f)
            embedding_data = json.load(e_f)
            
            text_list = [d["text"] for d in text_data]
            embedding_list = [d["embedding"] for d in embedding_data]
            
            rows = []
            for text, embedding in zip(text_list, embedding_list):
                rows.append({"text": text, "embedding": embedding})
        
        self.milvus_client.insert(collection_name=collection_name, data=rows)
        
        # Load collection into memory for faster search
        self.milvus_client.load_collection(collection_name)
        
        print(f"Inserted {len(rows)} entries into collection '{collection_name}'")
    
    def process_document(
        self, 
        pdf_url, 
        file_name, 
        file_json, 
        embeddings_json,
        collection_name=None
    ):
        """
        Complete pipeline: download PDF, extract text, generate embeddings, and insert into Milvus.
        
        Args:
            pdf_url: URL of the PDF to download
            file_name: Name for the downloaded PDF file
            file_json: Name for the extracted text JSON file
            embeddings_json: Name for the embeddings JSON file
            collection_name: Name of the collection to insert into
        """
        self.download_pdf(pdf_url, file_name)
        self.extract_pdf_text(file_name, file_json)
        self.generate_embeddings(file_json, embeddings_json)
        self.insert_embeddings(file_json, embeddings_json, collection_name)
        print("Document processing complete!")
    
    def search(self, query, collection_name=None, limit=1):
        """
        Search for the most similar text in the collection.
        
        Args:
            query: Search query string
            collection_name: Name of the collection to search
            limit: Number of results to return
            
        Returns:
            Search results from Milvus
        """
        if collection_name is None:
            collection_name = MilvusRAGInterface.DEFAULT_COLLECTION_NAME
        
        embedded_query = self.embedding_model.encode(query).tolist()
        
        result = self.milvus_client.search(
            collection_name=collection_name, 
            data=[embedded_query], 
            limit=limit,
            search_params={"metric_type": "L2"},
            output_fields=["text"]
        )
        
        return result
    
    def generate_response(self, prompt):
        """
        Generate a response using Google Gemini API.
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Generated response text or None if error occurs
        """
        if self.genai_client is None:
            print("Error: Gemini client not initialized. Set GOOGLE_API_KEY environment variable.")
            return None
        
        try:
            response = self.genai_client.models.generate_content(
                model=self.gemini_model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def build_prompt(self, context, question, language="pl"):
        """
        Build a prompt for Gemini with context and question.
        
        Args:
            context: Retrieved context from the document
            question: User's question
            language: Language for the prompt ("pl" for Polish, "en" for English)
            
        Returns:
            Formatted prompt string
        """
        if language == "pl":
            return f"""Na podstawie poniższych fragmentów dokumentu odpowiedz na pytanie.
    
Kontekst:
{context}

Pytanie: {question}
Odpowiedź:"""
        else:
            return f"""Based on the following document fragments, answer the question.
    
Context:
{context}

Question: {question}
Answer:"""
    
    def rag(self, query, collection_name=None, language="pl"):
        """
        RAG (Retrieval-Augmented Generation): Retrieve context and generate response.
        
        Args:
            query: User's question
            collection_name: Name of the collection to search
            language: Language for the prompt ("pl" for Polish, "en" for English)
            
        Returns:
            Generated response based on retrieved context
        """
        # Retrieve relevant context
        results = self.search(query, collection_name)
        context = "\n".join(hit["entity"]["text"] for hit in results[0])
        
        # Generate response using Gemini
        prompt = self.build_prompt(context, query, language=language)
        response = self.generate_response(prompt)
        
        return response
