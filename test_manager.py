# Test suite for the manager module
# import necessary built in modules
import unittest
# import custom modules
from manager import HabitManager
from habit import Habit

# Fake Database for Testing
class FakeDatabaseHandler:
    """
    A simple fake database used only for testing.
    It saves habits in memory instead of writing to a real file.
    This helps us test without touching the actual database.
    """

    def __init__(self, path=None):
        self.saved_habits = []
        self.completions = []

    def load_habits(self):
        return self.saved_habits

    def save_habit(self, habit):
        self.saved_habits.append(habit)
        return True

    def record_completion(self, title):
        self.completions.append(title)
        return True

    def delete_habit(self, title):
        before = len(self.saved_habits)
        self.saved_habits = [h for h in self.saved_habits if h.title != title]
        return len(self.saved_habits) < before

    def close(self):
        pass


# Testable manager uses fake database instead of real database

class TestableHabitManager(HabitManager):
    """
    A version of manager that uses fake database for testing.
    This makes tests independent of the real database.
    """

    def __init__(self):
        self.storage = FakeDatabaseHandler()
        self.habits = self.storage.load_habits()



# Unit Tests for manager
class TestHabitManager(unittest.TestCase):
    """
    Unit tests for the manager.
    Each test checks one small behavior of the manager.
    """

    def setUp(self):
        """
        Runs before every test.
        It create a fresh Testable manager so each test is clean.
        """
        self.manager = TestableHabitManager()

        self.manager.storage.saved_habits = []
        self.manager.storage.completions = []
        self.manager.habits = []

    # Test habit creation
    def test_create_habit(self):
        """
        Test that a habit is created and added to the habit list.
        """
        result = self.manager.create_habit("Read", "daily")

        self.assertTrue(result)
        self.assertEqual(len(self.manager.habits), 1)
        self.assertEqual(self.manager.habits[0].title, "Read")

    # Test get a habit by title
    def test_get_habit_by_title(self):
        """Test that we can get any habit using its title."""
        self.manager.create_habit("Run", "daily")
        habit = self.manager.get_habit_by_title("Run")

        self.assertIsNotNone(habit)
        self.assertEqual(habit.title, "Run")
    
    # Test deleting a habit
    def test_delete_habit(self):
        """
        Test that a habit deleted properly.
        """
        self.manager.create_habit("Meditate", "daily")

        self.assertTrue(self.manager.delete_habit("Meditate"))
        self.assertEqual(len(self.manager.habits), 0)

    # Test frequency filter
    def test_filter_by_frequency(self):
        """
        Test that filtering habits by frequency returns correct habits lists.
        """
        self.manager.create_habit("Read", "daily")
        self.manager.create_habit("Run", "weekly")

        daily = self.manager.filter_by_frequency("daily")

        self.assertEqual(len(daily), 1)
        self.assertEqual(daily[0].title, "Read")



if __name__ == '__main__':
    unittest.main()
