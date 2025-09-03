import os
import requests
import fitz
import json
import torch
import numpy as np
from pymilvus import MilvusClient, FieldSchema, DataType, CollectionSchema
from sentence_transformers import SentenceTransformer

class MilvusInterface():
    VECTOR_LENGTH = 768  # Silver Retriever Base v1.1 dimension
    DATA_DIR = "./milvus_db/data"  # Simplified path structure like in ex6.ipynb
    DEVICE = "cpu"  # Default to CPU for WSL compatibility
    
    def __init__(self, host="localhost", port="19530", embedding_model_name="ipipan/silver-retriever-base-v1.1"):
        self.milvus_client = MilvusClient(host=host, port=port)
        self.model = SentenceTransformer(embedding_model_name, device=self.DEVICE)

    def create_rag_collection(self, collection_name="rag_texts_and_embeddings", schema_description="RAG Texts collection"):
        """Create collection matching ex6.ipynb structure"""
        if self.milvus_client.has_collection(collection_name):
            print(f"Collection {collection_name} already exists")
            return
            
        # Schema matching ex6.ipynb: id, text, embedding
        id_field = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, description="Primary id")
        text = FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=4096, description="Page text")
        embedding_text = FieldSchema("embedding", dtype=DataType.FLOAT_VECTOR, dim=self.VECTOR_LENGTH, description="Embedded text")

        fields = [id_field, text, embedding_text]
        schema = CollectionSchema(fields=fields, auto_id=True, enable_dynamic_field=True, description=schema_description)

        self.milvus_client.create_collection(collection_name=collection_name, schema=schema)

        # Create HNSW index like in ex6.ipynb
        index_params = self.milvus_client.prepare_index_params()
        index_params.add_index(
            field_name="embedding", 
            index_type="HNSW",
            metric_type="L2",
            params={"M": 4, "efConstruction": 64}
        )
        
        self.milvus_client.create_index(collection_name=collection_name, index_params=index_params)
        print(f"Collection {collection_name} created successfully")
        print(f"Available collections: {self.milvus_client.list_collections()}")

    def remove_collection(self, collection_name):
        """Remove collection if it exists"""
        if self.milvus_client.has_collection(collection_name):
            print(f"Dropping collection: {collection_name}")
            self.milvus_client.drop_collection(collection_name)
            print("Collection dropped successfully")
        else:
            print("Collection doesn't exist")

    def download_pdf_data(self, pdf_url: str, file_name: str) -> None:
        """Download PDF from URL to data directory"""
        os.makedirs(self.DATA_DIR, exist_ok=True)
        response = requests.get(pdf_url, stream=True)
        with open(os.path.join(self.DATA_DIR, file_name), "wb") as file:
            for block in response.iter_content(chunk_size=1024):
                if block:
                    file.write(block)
        print(f"PDF downloaded to {os.path.join(self.DATA_DIR, file_name)}")

    def extract_pdf_text(self, file_name: str, file_json: str):
        """Extract text from PDF pages to JSON format matching ex6.ipynb structure"""
        os.makedirs(self.DATA_DIR, exist_ok=True)
        document = fitz.open(os.path.join(self.DATA_DIR, file_name))
        pages = []

        for page_num in range(len(document)):
            page = document.load_page(page_num)
            page_text = page.get_text()
            pages.append({"page_num": page_num, "text": page_text})

        with open(os.path.join(self.DATA_DIR, file_json), "w") as file:
            json.dump(pages, file, indent=4, ensure_ascii=False)
        print(f"Text extracted to {os.path.join(self.DATA_DIR, file_json)}")

    def generate_embeddings(self, file_json: str, embeddings_json: str):
        """Generate embeddings from extracted text, matching ex6.ipynb structure"""
        with open(os.path.join(self.DATA_DIR, file_json), "r") as file:
            data = json.load(file)

        pages = [page["text"] for page in data]
        embeddings = self.model.encode(pages)

        embeddings_paginated = []
        for page_num in range(len(embeddings)):
            embeddings_paginated.append({"page_num": page_num, "embedding": embeddings[page_num].tolist()})

        with open(os.path.join(self.DATA_DIR, embeddings_json), "w") as file:
            json.dump(embeddings_paginated, file, indent=4, ensure_ascii=False)
        print(f"Embeddings generated to {os.path.join(self.DATA_DIR, embeddings_json)}")

    def insert_embeddings(self, file_json: str, embeddings_json: str, collection_name="rag_texts_and_embeddings"):
        """Insert embeddings into Milvus collection, matching ex6.ipynb structure"""
        rows = []
        with open(os.path.join(self.DATA_DIR, file_json), "r") as t_f, open(os.path.join(self.DATA_DIR, embeddings_json), "r") as e_f:
            text_data, embedding_data = json.load(t_f), json.load(e_f)
            text_data = [d["text"] for d in text_data]
            embedding_data = [d["embedding"] for d in embedding_data]
            
            for page, (text, embedding) in enumerate(zip(text_data, embedding_data)):
                rows.append({"text": text, "embedding": embedding})

        self.milvus_client.insert(collection_name=collection_name, data=rows)
        print(f"Inserted {len(rows)} embeddings into {collection_name}")
        
        # Load collection for search
        self.milvus_client.load_collection(collection_name)

    def search(self, query: str, collection_name="rag_texts_and_embeddings", limit=1):
        """Search for similar texts, matching ex6.ipynb search function"""
        embedded_query = self.model.encode(query).tolist()
        results = self.milvus_client.search(
            collection_name=collection_name, 
            data=[embedded_query], 
            limit=limit,
            search_params={"metric_type": "L2"},
            output_fields=["text"]
        )
        return results

    def create_rag_pipeline(self, pdf_url: str, file_name: str, file_json: str, embeddings_json: str, collection_name="rag_texts_and_embeddings"):
        """Complete RAG pipeline: download PDF, extract text, generate embeddings, insert into Milvus"""
        print("Starting RAG pipeline...")
        
        # Create collection if it doesn't exist
        self.create_rag_collection(collection_name)
        
        # Download and process PDF
        self.download_pdf_data(pdf_url, file_name)
        self.extract_pdf_text(file_name, file_json)
        self.generate_embeddings(file_json, embeddings_json)
        self.insert_embeddings(file_json, embeddings_json, collection_name)
        
        print("RAG pipeline completed successfully!")
