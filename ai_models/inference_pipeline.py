import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel

# Load model and tokenizer (you can change to any embedding model you prefer)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def get_embeddings(text: str) -> np.ndarray:
    """
    Generate embeddings for a given text input using a transformer model.
    Returns a 1D numpy array.
    """
    try:
        # Tokenize text
        inputs = tokenizer([text], padding=True, truncation=True, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Get model output
        with torch.no_grad():
            outputs = model(**inputs)
            # Take mean pooling over token embeddings
            embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()

        # Flatten from shape (1, n) -> (n,)
        return embeddings.squeeze()

    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return np.zeros((384,), dtype=np.float32)


def save_embedding(embedding: np.ndarray, path: str):
    """
    Save embedding vector as .npy file.
    """
    np.save(path, embedding)


def load_embedding(path: str) -> np.ndarray:
    """
    Load embedding vector from .npy file.
    """
    return np.load(path)
