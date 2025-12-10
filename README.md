# Overview
This is a command line based Habit Tracking Application built in Python. It allows users to create daily and weekly habits, record completions, calculate total completed days and remove old habits from list. This app helps users maintain routines and analyze habit performance over time.

## Features
* Create and track daily and weekly habits.
* Record habit completions with timestamps.
* Return a list of all habits.
* Delete any habit from list.
* Return average completion rate.
* Return the longest run streak of all defined habits.
* Return the longest run streak for a given habit.
* Return the list of broken habits.
* Return the list of unbroken habits.
* Return a list of all habits with the same periodicity.
* Return a list of habits ranked by their streak
* Calculate total completion days for each habit.
* View overall summary of all the analytics calculations.
* Store habit data in SQLite database.
* Works via simple command line interface.

## Requirements
* Python 3.8+ installed on your system.
* Optional: pip for installing any dependencies.
* Basic terminal for macOS/Linux and command prompt for window for running the app.

## Installation
* Download the repository to your system.
* Make sure you have Python 3 installed:python --version
* Navigate to the project directory in terminal or command prompt:
* cd path_to_project
* python main.py
* Note:
   * Optional: Create a virtual environment
   * python -m venv venv
   * source venv/bin/activate   # macOS/Linux
   * venv\Scripts\activate      # Windows

## How to Use
* Create new habits
* Record completions
* Delete any habit
* View total completed days or streaks
* Example Commands
  * Run the app:
     python main.py
  * CLI options:
     * Create New Habit   → Add new habit
     * Mark Habit as Completed  → Complete the already define habit
     * View All Habits   → List of all store habit
     * View Habit Details  → Habit decription with completed day, and creation date. 
     * Delete Habit  → Delete any habit from database
     * View Analytics  → View all the analytics calcualtions
     * Exit
  
## File Structure
* habit.py → Defines the Habit class and methods for managing habits.
* manager.py → This module connects user actions with database and analytics functions.
* storage.py → Loads habit data from SQLite database into the application.
* analytics_module.py → Hnalde the analytics calculation like calculating the streaks.
* main.py → Main CLI interface to interact with the app.
* habits.db → SQLite database file with example data.

## Notes
* This app is case-sensitive.
* The app tracks total completed days without skipping gaps.
* You can use it for both daily and weekly habits.
* All data is saved in Sqlite database, making it easy to back up or edit manually.

# Author
Muhammad Zeeshan – Habit Tracking Application for personal productivity and assignment purposes.



