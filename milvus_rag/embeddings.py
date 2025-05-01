from sentence_transformers import SentenceTransformer
import torch

class EmbeddingModel:
    def __init__(self, model_name="ipipan/silver-retriever-base-v1.1"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device=self.device)
    
    def embed_text(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts).tolist()