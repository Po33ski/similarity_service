from sentence_transformers import SentenceTransformer
import torch

# Change to "cuda" if you have a GPU
device = "cpu"
model = SentenceTransformer(
    "distiluse-base-multilingual-cased-v2",
    device=device
)
print(f"Using device for embeddings: {device}")

# This function generates a 512-dim embedding for a given text
def generate_embedding(text: str) -> list[float]:
    """Generate 512-dim embedding for game descriptions"""
    if not text.strip():
        return [0.0] * 512  # Handle empty descriptions
    return model.encode(text, convert_to_numpy=True).tolist()