# Test functions for the Habit class.
# import necessary built in modules
import unittest
from datetime import datetime, timedelta
# import custom modules
from habit import Habit


class TestHabit(unittest.TestCase):
    """
    These tests check that the Habit object behaves correctly:
    """  

    def setUp(self):
        """
        Create a sample habit before each test runs.
        """
        self.habit = Habit("Exercise", "daily")

    # Habit creation tests
    def test_habit_creation(self):
        """
        Test that a new habit is created with correct attributes.
        """
        self.assertEqual(self.habit.title, "Exercise")
        self.assertEqual(self.habit.frequency, "daily")
        self.assertIsNotNone(self.habit.start_date)
        self.assertEqual(len(self.habit.history), 0)

    # Completion marking tests
    def test_mark_complete(self):
        """
        Test that marking a habit as complete adds a timestamp.
        """
        now = datetime.now()
        self.habit.mark_complete(now)

        self.assertEqual(len(self.habit.history), 1)
        self.assertIn(now, self.habit.history)

    # Latest completion date tests
    def test_get_last_completion_date(self):
        """
        Test that the habit correctly returns the last completion timestamp.
        """
        t1 = datetime(2025, 1, 1)
        t2 = datetime(2025, 2, 1)

        self.habit.mark_complete(t1)
        self.habit.mark_complete(t2)

        self.assertEqual(self.habit.get_last_completion_date(), t2)

    # Completion rate tests
    def test_completion_rate_daily(self):
        """
        Test the daily completion rate calculation.
        """
        self.habit.start_date = datetime.now() - timedelta(days=3)

        self.habit.mark_complete(datetime.now() - timedelta(days=2))
        self.habit.mark_complete(datetime.now() - timedelta(days=1))

        rate = self.habit.completion_rate()
        self.assertTrue(0 < rate <= 1)


if __name__ == "__main__":
    unittest.main()
