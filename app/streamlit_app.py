import sys
import os
# Align with "Absolute imports + sys.path management" principle [1]
# Add the project root directory (one level up from 'app') to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import json
import pandas as pd
from datetime import datetime
from src.recommender.journey_check import journey_check

DATA_PATH = "data/journal_entries.jsonl"

st.set_page_config(page_title="DataSelf — Personal Intelligence System", layout="wide")

st.title("🧠 DataSelf — Personal Intelligence System")
st.caption("Track reflections • Discover trends • Navigate your next best move")

# Load entries
def load_entries():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]
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
    entry = {
        "id": datetime.utcnow().isoformat(),
        "date": datetime.utcnow().isoformat(),
        "title": title,
        "topic_tags": [t.strip() for t in tags.split(",") if t.strip()],
        "reflection": reflection,
        "question": question,
        "time_minutes": 10,
        "mood": mood,
        "energy": energy,
        "source": "app",
        "embedding": None
    }
    with open(DATA_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    st.success("Entry saved.")

# Section: Analytics
st.header("Analytics")
if not df.empty:
    st.bar_chart(df["energy"])
else:
    st.info("No entries yet.")

# Section: Journey Check
st.header("🧭 Journey Check")
suggestion = journey_check(entries, user_state={"energy": energy})
st.json(suggestion)
