#This module connects CLI actions with database and analytics functions.

# Import necessary built in modules
from typing import List, Optional
# Import custom modules
from habit import Habit
from storage import DatabaseHandler
import analytics_module as analytics


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
        

    def get_habit_title(self, title: str) -> Optional[Habit]:
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
        return analytics.filter_by_frequency(self.habits, frequency)

    
    def largest_streak(self) -> int:
        """
        Gets the longest streak across all habits.
        """
        return analytics.largest_streak(self.habits)

    
    def get_habit_streak(self, title: str) -> Optional[int]:
        """
        Gets the current streak for a specific habit.
        """
        habit = self.get_habit_by_title(title)
        return streak_for(habit) if habit else None

    
    def broken_habits(self) -> List[Habit]:
        """
        Gets habits that have been broken at least once.
        """
        return analytics.broken_habits(self.habits)
    def get_unbroken_habits(self) -> List[Habit]:
        """
        Gets habits that have never been broken.
        """
        return unbroken_habits(self.habits)

    
    def get_completion_rates(self) -> Dict[str, float]:
        """
        Gets completion rates for all habits.

        :return: Dictionary mapping habit names to completion rates
        """
        return completion_rates(self.habits)

    
    def get_average_completion_rate(self) -> float:
        """
        Calculates average completion rate across all habits.

        :return: Average completion rate (0.0 to 1.0)
        """
        return average_completion_rate(self.habits)

    

    def get_habits_ranked_by_streak(self) -> List[Habit]:
        """
        Returns habits sorted by current streak (highest first).
        """
        return rank_by_streak(self.habits)

    

    def get_habits_ranked_by_consistency(self) -> List[Habit]:
        """
        Returns habits sorted by completion rate (highest first).
        """
        return rank_by_consistency(self.habits)

    
    def summary(self):
        """
        Provides comprehensive summary of all habits.
        """
        return analytics.overall_summary(self.habits)

    
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
