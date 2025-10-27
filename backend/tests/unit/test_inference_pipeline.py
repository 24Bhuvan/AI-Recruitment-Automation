# backend/tests/unit/test_inference_pipeline.py
import sys, os
import numpy as np
import pytest
from pathlib import Path

# -------- FIX: Add project root to sys.path --------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from ai_models import inference_pipeline as ip

# -------- CONFIG --------
BASE_DIR = Path(__file__).resolve().parents[2]
TEST_INPUT_FOLDER = BASE_DIR / "data/test_input"
TEST_OUTPUT_FOLDER = BASE_DIR / "ai_models/embeddings_test"
TEST_OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# -------- FIXTURE: Create sample text file --------
@pytest.fixture(scope="module")
def sample_text_file():
    TEST_INPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    test_file = TEST_INPUT_FOLDER / "sample.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("This is a test resume. Skills: Python, ML, Data Science.")
    yield test_file
    if test_file.exists():
        test_file.unlink()  # cleanup

# -------- TEST: Embedding generation --------
def test_get_embeddings(sample_text_file):
    with open(sample_text_file, "r", encoding="utf-8") as f:
        text = f.read()

    emb = ip.get_embeddings(text)

    assert isinstance(emb, np.ndarray), "Embedding should be a numpy array"
    assert emb.ndim == 1, "Embedding should be 1-dimensional"
    assert emb.size > 0, "Embedding should not be empty"

# -------- TEST: Full pipeline save --------
def test_embedding_save():
    emb = ip.get_embeddings("Sample resume content for testing.")
    out_file = TEST_OUTPUT_FOLDER / "sample_test.npy"
    np.save(out_file, emb)

    assert out_file.exists(), "Embedding file should be created"

    loaded_emb = np.load(out_file)
    assert np.allclose(emb, loaded_emb), "Saved and loaded embeddings should match"

    out_file.unlink()  # cleanup
