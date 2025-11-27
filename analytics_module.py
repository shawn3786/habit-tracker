#Analytics Module for Habit Tracking
#This module provides analytical functions using functional programming principles.
#Functional programming emphasizes pure functions that don't modify input data and have no side effects.
#Each function takes habit objects or lists and returns computed results without altering original state.

# typing module helps with type hints for better code documentation
from typing import List, Optional, Dict
# Import the Habit class from habit module
from habit import Habit

# Basic habit information 

def list_habit_title(habits: List[Habit]) -> List[str]:
    """
    Return the names of all habits.
    """
    return [habit.title for habit in habits]


def filter_by_frequency(habits: List[Habit], target_frequency: str) -> List[Habit]:
    """
    Select habits matching a certain frequency ("daily", "weekly").
    """
    normalized_frequency = target_frequency.lower()
    return [habit for habit in habits if habit.frequency == normalized_frequency]

# Streak related calculations

def largest_streak(habits: List[Habit]) -> int:
    """
    Return the largest streak value across all habits.
    """
    if not habits:
        return 0
    return max(habit.calculate_current_streak() for habit in habits)


def streak_for_single_habit(habit: Habit) -> int:
    """
    Return the current streak for a single habit.
    """
    return habit.calculate_current_streak()

# Completion rate calculations


def completion_rates(habits: List[Habit]) -> Dict[str, float]:
    """
    Return a dictionary mapping habit names -> completion rate (0.0 to 1.0).
    """
    return {habit.title: habit.completion_rate() for habit in habits}


def average_completion_rate(habits: List[Habit]) -> float:
    """
    Compute the mean completion rate for all habits.
    """
    if not habits:
        return 0.0
    rates = [habit.completion_rate() for habit in habits]
    return sum(rates) / len(rates) if rates else 0.0


# Ranking & comparison

def rank_by_streak(habits: List[Habit]) -> List[Habit]:
    """
    Return habits sorted from highest streak to lowest streak.
    """
    return sorted(habits, key=lambda habit: habit.calculate_current_streak(), reverse=True)


def rank_by_consistency(habits: List[Habit]) -> List[Habit]:
    """
    Sort habits by completion rate (best → worst).
    """
    return sorted(habits, key=lambda habit: habit.completion_rate(), reverse=True)

# Broken habit analytics

def broken_habits(habits: List[Habit]) -> List[Habit]:
    """
    Return a list of habits that were ever broken.
    """
    return [habit for habit in habits if habit.broken()]


def unbroken_habits(habits: List[Habit]) -> List[Habit]:
    """
    Return a list of habits that were never broken.
    """
    return [habit for habit in habits if not habit.broken()]


# Summary

def overall_summary(habits: List[Habit]) -> Dict[str, Optional[float]]:
    """
    Provide a global analytical summary of the entire habit list.
    """
    return {
        "total_habits": len(habits),
        "strongest_streak": largest_streak(habits),
        "average_completion_rate": average_completion_rate(habits),
        "broken_habits": len(broken_habits(habits)),
        "unbroken_habits": len(unbroken_habits(habits)),
    }









