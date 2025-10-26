from collections import Counter
import random

def journey_check(entries, user_state=None):
    """
    Personalized recommender for your learning journey.
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

    # Recurring question
    q_counts = Counter(q for q in questions if q)
    for q, cnt in q_counts.items():
        if cnt >= 2:
            return {"action": "Deep Dive", "reason": f"Recurring question: {q}", "task": f"Reflect deeper on '{q}'", "confidence": 0.85}

    # Low energy ⇒ micro learning
    if energy <= 4:
        return {"action": "Micro", "reason": "Low energy", "task": "Do a 15-min light review", "confidence": 0.75}

    # Trending tag
    if tags:
        top = Counter(tags).most_common(1)[0][0]
        return {"action": "Practice", "reason": "Recurring theme", "task": f"Do one exercise on {top}", "confidence": 0.7}

    # Default
    return {"action": "Explore", "reason": "No clear pattern", "task": "Explore a new topic briefly", "confidence": 0.5}
