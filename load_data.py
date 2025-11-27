"""
load_data.py
Load habits from JSON into database and verify entries.
Usage:
    python load_data.py example_data.json
"""

import sys
from habit_db import HabitDB, DATETIME_FMT

def main(json_path: str):
    db = HabitDB("habits.db")
    print(f"Loading data from {json_path} into {db.db_path} ...")
    db.load_from_json(json_path)
    print("Done. Verifying entries:")

    habits = db.load_habits()
    for h in habits:
        last = h.get_last_completion_date()
        last_str = last.strftime(DATETIME_FMT) if last else "Never"
        print(f"- Habit {h.title} ({h.frequency}) created {h.start_date.strftime(DATETIME_FMT)}")
        print(f"  Current streak: {h.calculate_current_streak()} | Broken: {h.broken()} | Last done: {last_str}")
    db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python load_data.py example_data.json")
        sys.exit(1)
    main(sys.argv[1])
    print("Data loaded successfully!")
