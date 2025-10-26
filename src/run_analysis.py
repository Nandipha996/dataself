import json
import pandas as pd

#from src.recommender.journey_check import journey_check
#from recommender.journey_check import check_journey
from src.recommender.journey_check import journey_check


def load_entries(path="data/journal_entries.jsonl"):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def main():
    entries = load_entries()
    df = pd.DataFrame(entries)
    print("📊 Total Entries:", len(df))
    print("Recent Moods:", df["mood"].value_counts().to_dict())

    suggestion = journey_check(entries, user_state={"energy": 6})
    print("\n🧭 Journey Check Suggestion:")
    for k, v in suggestion.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
