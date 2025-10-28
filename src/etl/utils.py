import json
from datetime import datetime
from uuid import uuid4
# --- ADDED IMPORTS FOR AI INTEGRATION ---
import numpy as np # Generally useful for array manipulation
from sentence_transformers import SentenceTransformer
import os 

# Initialize the model globally (or lazily loaded)
# Model choice may be subject to future refinement
# The architecture requires the use of 'sentence-transformers' [5]
try:
    # Use a small, efficient model for embedding calculation
    EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2') 
except ImportError:
    # Fallback if sentence-transformers is not installed, though it is a requirement [5]
    EMBEDDING_MODEL = None 


def create_entry_template():
    # Defines the standardized structure for journal entries [3]
    return {
        "id": str(uuid4()),
        "date": datetime.utcnow().isoformat(),
        "title": "",
        "topic_tags": [],
        "reflection": "",
        "question": "",
        "time_minutes": 0,
        "mood": "",
        "energy": 0,
        "source": "manual",
        "embedding": None # Will be filled if reflection text is present [6]
    }

def calculate_embedding(text):
    """Calculates the sentence embedding for the reflection text."""
    if not text or not EMBEDDING_MODEL:
        return None
    
    # Encode the text into an embedding vector
    embedding = EMBEDDING_MODEL.encode(text)
    # Convert numpy array to list for JSON serialization
    return embedding.tolist()

def append_entry(file_path, entry):
    # Appends the entry as a JSONL line to the data file [3]
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")