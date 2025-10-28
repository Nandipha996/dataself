from collections import Counter
import random
import os
# Dependencies for Predictive System (Gap 1b)
# Note: scikit-learn is required for the predictive system [3, 4]
from sklearn.linear_model import LogisticRegression 
# Dependencies for Secure Configuration (Gap 3 setup)
from dotenv import load_dotenv 

# --- Configuration Loading (Essential for Automate Search) ---
load_dotenv()
EXTERNAL_SEARCH_API_KEY = os.getenv("EXTERNAL_SEARCH_API_KEY") # API Key for external calls [7]

# --- Predictive Model Setup Placeholder (Gap 1b) ---
PREDICTIVE_MODEL = None 
MODEL_LOADED = False
# In a full system, model loading logic would be here:
# try:
#     PREDICTIVE_MODEL = load_trained_model("model_v1.pkl")
#     MODEL_LOADED = True
# except FileNotFoundError:
#     pass
    
# --- Automate Search Helper (Gap 2) ---
def run_automate_search(recent_tags):
    """
    Placeholder for the logic that performs external API calls to suggest 
    opportunities, training, and relevant roles [2, 7].
    """
    # Trigger search if API key exists and a relevant tag (e.g., 'career' or 'job hunt') is present
    if EXTERNAL_SEARCH_API_KEY and any(tag in recent_tags for tag in ["career", "job search", "upskilling"]):
        return True, "Relevant Career Opportunity Match"
    return False, None


def journey_check(entries, user_state=None):
    """
    Personalized recommender for your learning journey (Predictive/Rule Hybrid).
    entries: list[dict]
    user_state: dict {energy: int}
    """
    user_state = user_state or {}
    if not entries:
        return {"action": "Start", "reason": "No data yet", "task": "Add your first entry", "confidence": 0.6}

    # Analyze patterns
    recent = entries[-30:]
    energy = user_state.get("energy", 6)
    tags = [tag for e in recent for tag in e.get("topic_tags", [])]
    questions = [e.get("question") for e in recent if e.get("question")]
    
    # 1. NEW: Check for Automate Search Opportunity (Highest Priority)
    search_needed, search_reason = run_automate_search(tags)
    if search_needed:
        # Automate Search streamlines job hunting and upskilling [8]
        return {"action": "Automate Search", 
                "reason": search_reason, 
                "task": "Review tailored job/upskilling recommendations", 
                "confidence": 0.9}

    # 2. Transition to Predictive Logic (Gap 1b)
    if MODEL_LOADED and energy > 5: 
        # In a complete system, this would use embeddings and energy to predict the action
        # Example Placeholder:
        if random.random() > 0.6:
            return {"action": "Strategy", 
                    "reason": "AI Predicted Optimal Next Step", 
                    "task": "Define the next 3 steps for your current learning project", 
                    "confidence": 0.8}
            
    # 3. Existing Rule-Based Logic (Fallback)
    
    # Recurring question [9]
    q_counts = Counter(q for q in questions if q)
    for q, cnt in q_counts.items():
        if cnt >= 2:
            return {"action": "Deep Dive", "reason": f"Recurring question: {q}", "task": f"Reflect deeper on '{q}'", "confidence": 0.85}

    # Low energy ⇒ micro learning [9]
    if energy <= 4:
        return {"action": "Micro", "reason": "Low energy", "task": "Do a 15-min light review", "confidence": 0.75}

    # Trending tag [10]
    if tags:
        top = Counter(tags).most_common(1)
        return {"action": "Practice", "reason": "Recurring theme", "task": f"Do one exercise on {top}", "confidence": 0.7}

    # Default
    return {"action": "Explore", "reason": "No clear pattern", "task": "Explore a new topic briefly", "confidence": 0.5}
