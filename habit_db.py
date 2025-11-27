"""
habit_db.py
SQLite interface for Habit Tracker
"""

import sqlite3
from datetime import datetime
from typing import List
from habit import Habit

DATETIME_FMT = "%Y-%m-%d %H:%M"

class HabitDB:
    def __init__(self, db_path: str = "habits.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                frequency TEXT NOT NULL,
                start_date TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(habit_id) REFERENCES habits(id)
            )
        """)
        self.conn.commit()

    def insert_habit(self, habit: Habit) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO habits (title, frequency, start_date) VALUES (?, ?, ?)",
            (habit.title, habit.frequency, habit.start_date.isoformat())
        )
        self.conn.commit()
        return cur.lastrowid

    def insert_completion(self, habit_id: int, completion_time: datetime):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO completions (habit_id, timestamp) VALUES (?, ?)",
            (habit_id, completion_time.isoformat())
        )
        self.conn.commit()

    def load_habits(self) -> List[Habit]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, frequency, start_date FROM habits")
        rows = cur.fetchall()
        habits: List[Habit] = []

        for row in rows:
            habit = Habit(title=row["title"], frequency=row["frequency"])
            habit.start_date = datetime.fromisoformat(row["start_date"])

            cur.execute(
                "SELECT timestamp FROM completions WHERE habit_id = ? ORDER BY timestamp",
                (row["id"],)
            )
            completions = cur.fetchall()
            for c in completions:
                habit.history.append(datetime.fromisoformat(c["timestamp"]))

            habits.append(habit)
        return habits

    def load_from_json(self, json_path: str):
        import json
        with open(json_path, "r") as f:
            data = json.load(f)
        for habit_data in data["habits"]:
            habit = Habit(habit_data["name"], habit_data["period"])
            habit.start_date = datetime.fromisoformat(habit_data["created"])
            habit_id = self.insert_habit(habit)
            for c_time in habit_data["completions"]:
                self.insert_completion(habit_id, datetime.fromisoformat(c_time))

    def close(self):
        self.conn.close()
