# Helper test module used only for tests.
# import necessary built in modules
import unittest
from datetime import timedelta
# import custom modules
from habit import Habit
import analytics_module as analytics


def create_habit(title, freq, days_completed=0, broken=False):
    """
    This function creates a Habit object with a given number of completed days.
    It is used to avoid repeating the same setup code inside each test.
    """
    habit = Habit(title, freq)

    # Add fake completion history for testing
    for i in range(days_completed):
        completion_time = habit.start_date + timedelta(days=i)
        habit.mark_complete(completion_time)

    if broken:
        habit.history.append(habit.start_date + timedelta(days=50))

    return habit


class TestAnalyticsModule(unittest.TestCase):
    """
    This test suite checks the most important functions inside analytics_module.
    """

    # Basic functionality tests
    def test_list_habit_title(self):
        """
        Test that the function returns only habit titles in the correct order.
        """
        h1 = Habit("Reading", "daily")
        h2 = Habit("Workout", "weekly")
        result = analytics.list_habit_title([h1, h2])
        self.assertEqual(result, ["Reading", "Workout"])

    def test_filter_by_frequency(self):
        """
        Test filtering habits by their frequency.
        """
        h1 = Habit("Read", "daily")
        h2 = Habit("Run", "weekly")
        daily = analytics.filter_by_frequency([h1, h2], "DAILY")
        self.assertEqual(daily, [h1])

    # Streak tests
    def test_largest_streak(self):
        """
        Test that the system correctly finds the largest streak across all habits.
        """
        h1 = create_habit("A", "daily", days_completed=3)
        h2 = create_habit("B", "daily", days_completed=5)
        result = analytics.largest_streak([h1, h2])
        self.assertEqual(result, 5)

    def test_largest_streak_for_habit(self):
        """
        Test streak calculation for a single habit.
        """
        h = create_habit("Meditation", "daily", days_completed=4)
        result = analytics.largest_streak_for_habit(h)
        self.assertEqual(result, 4)

    # Average completion rate tests
    def test_average_completion_rate(self):
        """
        Test that average completion rate returns the right value.
        """
        h1 = create_habit("A", "daily", days_completed=2)
        h2 = create_habit("B", "daily", days_completed=2)
        avg = analytics.average_completion_rate([h1, h2])
        self.assertIsInstance(avg, float)

    # Ranking tests
    def test_rank_by_streak(self):
        """
        Test that ranking the habits from highest streak to lowest streak.
        """
        h1 = create_habit("A", "daily", days_completed=1)
        h2 = create_habit("B", "daily", days_completed=3)
        ranked = analytics.rank_by_streak([h1, h2])
        self.assertEqual(ranked[0], h2)
        self.assertEqual(ranked[1], h1)

    # Broken vs unbroken habits tests
    def test_broken_habits(self):
        """
        Test thst function correctly identifies broken habit.
        """
        h1 = create_habit("Good", "daily", days_completed=3)
        h2 = create_habit("Bad", "daily", days_completed=1, broken=True)
        result = analytics.broken_habits([h1, h2])
        self.assertEqual(result, [h2])

    def test_unbroken_habits(self):
        """
        Test that function returns the habits that are unbroken.
        """
        h1 = create_habit("Good", "daily", days_completed=3)
        h2 = create_habit("Bad", "daily", days_completed=1, broken=True)
        result = analytics.unbroken_habits([h1, h2])
        self.assertEqual(result, [h1])

    # Summary test
    def test_overall_summary(self):
        """
        Test that the summary returns correct statistics about the habits.
        """
        h1 = create_habit("A", "daily", days_completed=2)
        h2 = create_habit("B", "daily", days_completed=0, broken=True)

        summary = analytics.overall_summary([h1, h2])

        self.assertEqual(summary["total_habits"], 2)
        self.assertIn("strongest_streak", summary)
        self.assertIn("average_completion_rate", summary)
        self.assertEqual(summary["broken_habits"], 1)
        self.assertEqual(summary["unbroken_habits"], 1)


if __name__ == "__main__":
    unittest.main()
