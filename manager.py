#This module connects CLI actions with database and analytics functions.

# Import necessary built in modules
from typing import Dict, List, Optional
# Import custom modules
from habit import Habit
from storage import DatabaseHandler
from analytics_module import (
    filter_by_frequency,
    largest_streak,
    largest_streak_for_habit,
    broken_habits,
    unbroken_habits,
    completion_rates,
    average_completion_rate,
    rank_by_streak,
    overall_summary
)


class HabitManager:
    """
    Manages all habit operations and coordinates between different modules.
    Acts as the central controller for the habit tracking application.
    """

    def __init__(self, database_path: str = "habits.db"):
        """
        Initializes the manager with storage and loads existing habits.
        """
        self.storage = DatabaseHandler(database_path)
        self.habits = self.storage.load_habits()


    def create_habit(self, title: str, frequency: str) -> bool:
        """
        Create a new habit and save it into database.
        """
        habit = Habit(title, frequency)
        saved = self.storage.save_habit(habit)

        if saved:
            self.habits.append(habit)

        return saved


    def list_habits(self) -> List[Habit]:
        """
        Returns all habits in the system.
        """
        return self.habits
        

    def get_habit_titles(self) -> List[str]:
        """
        Returns titles of all habits.
        """
        return [habit.title for habit in self.habits]

    
    def get_habit_by_title(self, title: str) -> Optional[Habit]:
        """
        Finds a habit by its title.
        """
        for habit in self.habits:
            if habit.title == title:
                return habit
        return None

    
    def mark_habit_complete(self, title: str) -> bool:
        """
        Mark a habit complete and update the database.
        """
        success = self.storage.record_completion(title)

        if not success:
            return False

        # update in-memory object
        for habit in self.habits:
            if habit.title == title:
                habit.mark_complete()
                break

        return True

    
    def delete_habit(self, title: str) -> bool:
        """
        Delete a habit from database and memory.
        """
        success = self.storage.delete_habit(title)

        if success:
            self.habits = [h for h in self.habits if h.title != title]

        return success

    
    def filter_by_frequency(self, frequency: str) -> List[Habit]:
        """
        Filters habits by their frequency.
        """
        return filter_by_frequency(self.habits, frequency)

    
    def largest_streak(self) -> int:
        """
        Gets the longest streak across all habits.
        """
        return largest_streak(self.habits)

    
    def largest_streak_for_habit(self, title: str) -> Optional[int]:
        """
        Gets the current streak for a specific habit.
        """
        habit = self.get_habit_by_title(title)
        return largest_streak_for_habit(habit) if habit else None

    
    def broken_habits(self) -> List[Habit]:
        """
        Gets habits that have been broken at least once.
        """
        return broken_habits(self.habits)

    
    def get_unbroken_habits(self) -> List[Habit]:
        """
        Gets habits that have never been broken.
        """
        return unbroken_habits(self.habits)

    
    def get_completion_rates(self) -> Dict[str, float]:
        """
        Gets completion rates for all habits.
        """
        return completion_rates(self.habits)

    
    def get_average_completion_rate(self) -> float:
        """
        Calculates average completion rate across all habits.
        """
        return average_completion_rate(self.habits)

    

    def get_habits_ranked_by_streak(self) -> List[Habit]:
        """
        Returns habits sorted by current streak (highest first).
        """
        return rank_by_streak(self.habits)

    
    def summary(self):
        """
        Provides comprehensive summary of all habits.
        """
        return overall_summary(self.habits)

    
    def refresh(self):
        """
        Reload all habits from database.
        """
        self.habits = self.storage.load_habits()

    def close(self):
        """
        Closes the storage connection properly.
        """
        self.storage.close()
