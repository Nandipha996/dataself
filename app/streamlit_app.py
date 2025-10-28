import sys
import os

# Fix the ModuleNotFoundError by adding the project root to the Python path
# Assumes the script is run from the project root or one directory deep (e.g., in 'app/')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import json
import pandas as pd
# ... rest of the original code ...

from datetime import datetime
from src.recommender.journey_check import journey_check
# Import new utility functions
from src.etl.utils import calculate_embedding, append_entry # Inferred necessary for data saving

# Import python-dotenv for secure configuration loading (Addressing Gap 3)
from dotenv import load_dotenv
load_dotenv() 

DATA_PATH = "data/journal_entries.jsonl"

st.set_page_config(page_title="DataSelf — Personal Intelligence System", layout="wide")
st.title("🧠 DataSelf — Personal Intelligence System")
st.caption("Track reflections • Discover trends • Navigate your next best move")

# Load entries
def load_entries():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f] # [11, 13]
    except FileNotFoundError:
        return []

entries = load_entries()
df = pd.DataFrame(entries)

# Section: Add new entry
st.header("Add New Entry")
title = st.text_input("Title")
reflection = st.text_area("Reflection")
tags = st.text_input("Tags (comma separated)")
question = st.text_input("Question")
mood = st.selectbox("Mood", ["", "happy", "neutral", "sad", "curious", "tired"])
energy = st.slider("Energy (1-10)", 1, 10, 6)

if st.button("Save Entry"):
    
    # 🌟 NEW: Calculate Embedding before saving (Integration for Gap 1a)
    entry_embedding = calculate_embedding(reflection)
    
    entry = {
        "id": datetime.utcnow().isoformat(), # [5]
        "date": datetime.utcnow().isoformat(), # [5]
        "title": title, # [5]
        "topic_tags": [t.strip() for t in tags.split(",") if t.strip()], # [5]
        "reflection": reflection, # [5]
        "question": question, # [5]
        "time_minutes": 10, # [5]
        "mood": mood, # [5]
        "energy": energy, # [5]
        "source": "app", # [5]
        "embedding": entry_embedding # Updated from None [5]
    }

    # Using the ETL helper function for appending
    append_entry(DATA_PATH, entry)
    st.success("Entry saved.")

# Section: Analytics
st.header("Analytics")
if not df.empty:
    st.bar_chart(df["energy"]) # [12]
else:
    st.info("No entries yet.") # [12]

# Section: Journey Check
st.header("🧭 Journey Check")
suggestion = journey_check(entries, user_state={"energy": energy}) # [12]
st.json(suggestion)