import os
#from src.etl.utils import create_entry_template, append_entry
#from etl.utils import create_entry_template, append_entry
from src.etl.utils import create_entry_template, append_entry

def main():
    data_path = "data/journal_entries.jsonl"
    entry = create_entry_template()
    if not os.path.exists("data"):
        os.makedirs("data")
    append_entry(data_path, entry)
    print("✅ New entry template appended to data/journal_entries.jsonl")

if __name__ == "__main__":
    main()
