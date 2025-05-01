from sentence_transformers import SentenceTransformer
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(
    "distiluse-base-multilingual-cased-v2",
    device=device
)

def generate_embedding(text: str) -> list[float]:
    """Generate 512-dim embedding for game descriptions"""
    if not text.strip():
        return [0.0] * 512  # Handle empty descriptions
    return model.encode(text, convert_to_numpy=True).tolist()