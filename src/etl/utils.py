import json
from datetime import datetime
from uuid import uuid4

def create_entry_template():
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
        "embedding": None
    }

def append_entry(file_path, entry):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
