#Storage module for the Habit Tracking App.
#This module handles all interactions with the SQLite database.
#This module does NOT contain business logic — only database operations.

# Import built-in modules for database operations and date handling
import sqlite3
from datetime import datetime
from typing import List, 
# Import the Habit class from the habit module
from habit import Habit


class DatabaseHandler:
    """
    The DatabaseHandler class acts as the bridge between your Habit objects and the database.
    It creates required tables, saves new habits, loads habits, and stores completion events.
    """

    def __init__(self, db_path: str = "habits.db"):
        """
        Create a database connection and ensure all tables exist.
        """
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_tables()

    
    def _create_tables(self):
        """
        Creates required tables for storing habits and their completion logs.
        """
        # Create the habits table
        self.cursor.execute("""                          
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                frequency TEXT NOT NULL,
                start_date TEXT NOT NULL
            )    
        """)   
        # Create the habit_history table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habit_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completion_time TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(id)
            )
        """)
        # Apply the changes to the database
        self.connection.commit()


    def save_habit(self, habit: Habit) -> bool:
        """
        Save a new habit into the database.
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO habits (title, frequency, start_date)
                VALUES (?, ?, ?)
                """,
                (habit.title, habit.frequency, habit.start_date.isoformat())
            )
            self.connection.commit()
            return True
            
        except sqlite3.IntegrityError:
            # Handle case where habit with same title already exists
            return False
        

    def load_habits(self) -> List[Habit]:
        """
        Load all habits along with their stored completion history.
        """
        self.cursor.execute("SELECT habit_id, title, frequency, start_date FROM habits")
        rows = self.cursor.fetchall()

        habits: List[Habit] = []

        for habit_id, title, frequency, start_date_str in rows:
            # Create Habit instance
            habit = Habit(title=title, frequency=frequency)
            habit.start_date = datetime.fromisoformat(start_date_str)

            # Load completion history for this habit
            self.cursor.execute(
                "SELECT completion_time FROM habit_history WHERE habit_id = ?",
                (habit_id,)
            )
            completion_rows = self.cursor.fetchall()

            for (time_str,) in completion_rows:
                habit.history.append(datetime.fromisoformat(time_str))
            habits.append(habit)

        return habits

    
    def record_completion(self, habit_title: str, time: Optional[datetime] = None) -> bool:
        """
        Record a completion event for a habit.     
        If no time is provided, uses current time.
        """
        if time is None:
            time = datetime.now()

        try:
            # Find habit ID by title
            self.cursor.execute("SELECT id FROM habits WHERE title = ?", (habit_title,))
            result = self.cursor.fetchone()
    
            if result:
                habit_id = result[0]   # Habit not found
                self.cursor.execute(
                    """
                    INSERT INTO habit_history (habit_id, completion_time)
                    VALUES (?, ?)
                    """,
                    (habit_id, time.isoformat())
                )
                self.connection.commit()
                return True
            return False
        except sqlite3.Error:
            return False

    
    def delete_habit(self, habit_title: str) -> bool:
        """
        Remove a habit and all of its completion logs.
        """
        try:
        # Find ID first
            self.cursor.execute("SELECT id FROM habits WHERE title = ?", (habit_title,))
            row = self.cursor.fetchone()
    
            if  row:
                habit_id = row[0]
                # Delete completion records
                self.cursor.execute("DELETE FROM habit_history WHERE habit_id = ?", (habit_id,))
                 # Delete the habit itself
                self.cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
                self.connection.commit()
                return True
            return False
        except sqlite3.Error:
            return False

    
    def close(self):
        """Close the database connection."""
        self.connection.close()
