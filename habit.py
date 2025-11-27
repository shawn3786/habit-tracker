# Import necessary built-in modules
# datetime module provides classes for manipulating dates and times
# We'll use it to track when habits are created and marked as completed
from datetime import datetime, timedelta
# typing module helps with type hints for better code documentation
from typing import List, Optional



# Define the Habit class to represent individual habits
class Habit:
    """
    The Habit class represents a personal habit that users want to establish and monitor.

    This class track a habit with flexible frequency, completion history,
    and helpful analysis like streaks, completion rate, last done date, etc.
    """

    def __init__(self, title: str, frequency: str):
        """
        Initializes a new Habit instance with basic information.

        :param title: Name for the habit like read, run and meditate etc.
        :param frequency: The repetition pattern, either 'daily' or 'weekly'.
        """
        # Store the habit name
        self.title = title

        # Normalize frequency to lowercase for consistent processing
        self.frequency = frequency.lower()

        # Record when this habit was first created
        self.start_date = datetime.now()

        # Initialize storage for tracking history
        self.history: List[datetime] = []

    

    def mark_complete(self, completion_time: Optional[datetime] = None):
        """
        Records the habit as completed at a specific time.

        :param completion_time: Optional datetime for completion. Uses current time if not provided.
        """
        # Default to current moment if no specific time given
        if completion_time is None:
            completion_time = datetime.now()

        # Add this completion to our tracking history
        self.history.append(completion_time)

    

    def calculate_current_streak(self) -> int:
        """
        Determines the number of consecutive periods the habit has been maintained, 
        counting backwards from the most recent completion.
        """
        # No completions means no streak
        if len(self.history) == 0:
            return 0

        # Sort completions from most recent to oldest
        sorted_completions = sorted(self.history, reverse=True)

        # Initialize streak counter
        streak = 0

        # Set the period length based on habit frequency
        period_length = timedelta(days=1) if self.frequency == 'daily' else timedelta(weeks=1)

        # Reference point for streak calculation starts with most recent completion
        streak_reference = sorted_completions[0]

        # Check each completion against our streak window
        for completion in sorted_completions:
            if streak_reference - completion <= period_length:
                streak += 1
                streak_reference = completion
            else:
                break
        return streak
        

    def broken(self) -> bool:
        """
        Checks if there was any period where the habit was not completed as required.
        """
        # No completions means the habit was broken from the start
        if not self.history:
            return True

        # Sort completions chronologically
        ordered_completions = sorted(self.history)

        # Define the maximum allowed gap between completions
        allowed_gap = timedelta(days=1) if self.frequency == 'daily' else timedelta(weeks=1)

        # Start checking from habit creation date
        last_checkpoint = self.start_date

        # Examine each completion for gaps
        for completion in ordered_completions:
            if completion - last_checkpoint > allowed_gap:
                return True
            last_checkpoint = completion
        return False
        

    def completed_today(self) -> bool:
        """
        Checks if the habit has been completed during the current day.
        """
        today = datetime.now().date()

        # Check if any completion occurred today
        for completion in self.history:
            if completion.date() == today:
                return True

        return False
        

    def get_last_completion_date(self) -> Optional[datetime]:
        """
        Retrieves the most recent date when this habit was completed.
        """
        if not self.history:
            return None
        return max(self.history)


    def completion_rate(self) -> float:
        """Calculates completion rate as actual completions divided by expected periods."""
        now = datetime.now()
        days = (now.date() - self.start_date.date()).days
        if self.frequency == 'daily':
            expected_periods = max(days + 1, 1)
        else:
            expected_periods = max(((days // 7) + 1), 1)
        if expected_periods == 0:
            return 0.0
        return min(len(self.history) / expected_periods, 1.0)
        

    def clear_completion_history(self):
        """
        Resets the completion tracking while keeping the habit definition intact.
        Useful for starting fresh while maintaining the same habit.
        """
        self.history.clear()
        

    def summary(self) -> str:
        """
        Generates a concise summary of the habit's current status.
        """
        last = self.get_last_completion_date()
        return (
             f"Habit: {self.title}\n"
             f"Frequency: {self.frequency}\n"
             f"Current Streak: {self.calculate_current_streak()}\n"
             f"Was ever broken: {'Yes' if self.broken() else 'No'}\n"
             f"Last completed: {last.strftime('%Y-%m-%d') if last else 'Never'}\n"
        )
