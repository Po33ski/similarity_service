from pymilvus import MilvusClient, FieldSchema, DataType, CollectionSchema

def setup_milvus():
    client = MilvusClient(host="localhost", port="19530")
    
    VECTOR_LENGTH = 768  # Silver Retriever dimension
    
    schema = CollectionSchema(
        fields=[
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="page_num", dtype=DataType.INT32),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=4096),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=VECTOR_LENGTH)
        ],
        description="RAG document chunks"
    )
    
    client.create_collection(
        collection_name="rag_docs",
        schema=schema
    )
    
    # Create HNSW index
    client.create_index(
        collection_name="rag_docs",
        field_name="embedding",
        index_type="HNSW",
        metric_type="L2",
        params={"M": 8, "efConstruction": 64}
    )
    
    return client