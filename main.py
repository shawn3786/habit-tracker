# Main CLI Module for Habit Tracking Application
# Provides command-line interface for users to interact with the system

#Python built-in modules
import sys
from datetime import datetime
#Custom modules
from manager import HabitManager



def display_menu():
        """
        Shows the main menu options to the user.
        """
        print("\n============================================")
        print("          HABIT TRACKING APPLICATION")
        print("============================================")
        print("1.  Create New Habit")
        print("2.  Mark Habit as Completed")
        print("3.  View All Habits")
        print("4.  View Habit Details")
        print("5.  Delete Habit")
        print("6.  View Overall Summary")
        print("7.  View Analytics")
        print("8.  Exit")
        print("============================================")

# Main program loop
def main():
    """
    Entry point for the application.
    """
    manager = HabitManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ")
        
        # Handle habit creation
        if choice == "1":
            print("\n--- Create New Habit ---")
            title = input("Enter habit name: ").strip()

            if not title:
                print("Habit name cannot be empty.")
                return

            frequency = input("Enter frequency (daily/weekly): ").strip().lower()

            if frequency not in ['daily', 'weekly']:
                print("Frequency must be 'daily' or 'weekly'.")
                return

            if manager.create_habit(title, frequency):
                print(f"✅ Habit '{title}' created successfully!")
            else:
                print(f"❌ Failed to create habit. Maybe '{title}' already exists?")

        # MARK COMPLETE
        elif choice == "2":
            print("\n--- Mark Habit as Completed ---")
            titles = manager.get_habit_title()

            if not titles:
                print("No habits found. Please create a habit first.")
                return

            manager.list_habits_by_title(title)

            title = input("Enter habit name to mark complete: ").strip()

            if title not in titles:
                print(f"Habit '{title}' not found.")
                return

            if manager.complete_habit(title):
                print(f"✅ Habit '{title}' marked as completed!")
            else:
                print(f"❌ Failed to mark habit as completed.")


        # All HABITS
        elif choice == "3":
            print("\n--- All Habits ---")
            habits = manager.get_all_habits()

            if not habits:
                print("No habits found.")
                return

            for i, habit in enumerate(habits, 1):
                last_completion = habit.get_last_completion_date()
                last_str = last_completion.strftime("%Y-%m-%d") if last_completion else "Never"
                streak = habit.calculate_current_streak()
                print(f"{i}. {habit.title} ({habit.frequency}) - Streak: {streak} - Last: {last_str}")

        # HABIT DETAILS
        elif choice == "4":
            print("\n--- Habit Details ---")
            titles = manager.get_habit_titles()

            if not titles:
                print("No habits found.")
                return

            show_habit_list(titles)

            title = input("Enter habit name to view details: ").strip()
            habit = manager.get_habit_by_title(title)

            if habit:
                print(f"\n{habit.summary()}")
            else:
                print(f"Habit '{title}' not found.")


        # DELETE HABIT
        elif choice == "5":
            print("\n--- Delete Habit ---")
            titles = manager.get_habit_titles()

            if not titles:
                print("No habits found.")
                return

            show_habit_list(titles)

            title = input("Enter habit name to delete: ").strip()

            if title not in titles:
                print(f"Habit '{title}' not found.")
                return

            confirm = input(f"Are you sure you want to delete '{title}'? (y/N): ").strip().lower()
            if confirm == 'y':
                if manager.delete_habit(title):
                    print(f"✅ Habit '{title}' deleted successfully!")
                else:
                    print(f"❌ Failed to delete habit.")
            else:
                print("Deletion cancelled.")

       
        #Overall Summary
        elif choice == "6":
            print("\n--- Overall Summary ---")
            summary = manager.summary()
            print(f"Total Habits: {summary['total_habits']}")
            print(f"Longest Streak: {summary['strongest_streak']}")
            print(f"Average Completion Rate: {summary['average_completion_rate'] * 100:.1f}%")
            print(f"Broken Habits: {summary['broken_habits']}")
            print(f"Unbroken Habits: {summary['unbroken_habits']}")
        
        # Analytics
        elif choice == "7":

            def sub_menu():
                print("\n--- Analytics Menu ---")
                print("1. View Completion Rates")
                print("2. View Habits by Streak Ranking")
                print("3. View Habits by Consistency")
                print("4. View Broken Habits")
                print("5. View Unbroken Habits")
                print("6. View Daily Habits")
                print("7. View Weekly Habits")
                print("8. Back to Main Menu")

                while True:
                    sub_menu()
                    choice = input("Enter your choice (1-8): ").strip()
    
                    #Displays completion rates
                    if choice == '1':
                        print("\n--- Completion Rates ---")
                        rates = manager.get_completion_rates()
                        avg_rate = manager.get_average_completion_rate()
    
                        for habit_name, rate in rates.items():
                            percentage = rate * 100
                            print(f"{habit_name}: {percentage:.1f}%")
    
                        print(f"\nAverage Completion Rate: {avg_rate * 100:.1f}%")
                           
                    #Shows habits ranked
                    elif choice == '2':
                        print("\n--- Habits Ranked by Current Streak ---")
                        ranked = manager.get_habits_ranked_by_streak()
    
                        for i, habit in enumerate(ranked, 1):
                            streak = habit.calculate_current_streak()
                            print(f"{i}. {habit.title}: {streak} days")
    
                    #Shows habits ranked by consistency
                    elif choice == '3':
                        print("\n--- Habits Ranked by Consistency ---")
                        ranked = manager.get_habits_ranked_by_consistency()
    
                        for i, habit in enumerate(ranked, 1):
                            # Calculate completion rate for this habit
                            from analytics_module import completion_rates
                            rates = completion_rates([habit])
                            percentage = rates[habit.title] * 100
                            print(f"{i}. {habit.title}: {percentage:.1f}%")
    
                    #Shows habits that have been broken
                    elif choice == '4':
                        print("\n--- Broken Habits ---")
                        broken = manager.broken_habits()
    
                        if not broken:
                            print("No broken habits! Great job! 🎉")
                            return
    
                        for habit in broken:
                            print(f"• {habit.title} ({habit.frequency})")
    
                    #Shows habits that have never been broken
                    elif choice == '5':
                        print("\n--- Unbroken Habits ---")
                        unbroken = manager.get_unbroken_habits()
    
                        if not unbroken:
                            print("No unbroken habits found.")
                            return
    
                        for habit in unbroken:
                            print(f"• {habit.title} ({habit.frequency}) - Streak: {habit.calculate_current_streak()}")
    
                    #Shows daily habits
                    elif choice == '6':
                        print("\n--- Daily Habits ---")
                        daily_habits = manager.filter_by_frequency("daily")
                        if not daily_habits:
                            print("No daily habits found.")    
                        else:
                            for habit in daily_habits:
                                streak = habit.calculate_current_streak()
                                print(f"• {habit.title} - Current Streak: {streak} days")
    
                    #Shows weekly habits
                    elif choice == '7':
                        print("\n--- Weekly Habits ---")
                        weekly_habits = manager.filter_by_frequency("weekly")
                        if not weekly_habits:
                            print("No weekly habits found.")
                        else:
                            for habit in weekly_habits:
                                streak = habit.calculate_current_streak()
                                print(f"• {habit.title} - Current Streak: {streak} weeks")
    
                    #Back to main menu
                    elif choice == '8':
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 8. ")

        elif choice == "8": 
            print("\nThank you for using the Habit Tracking Application!")
            print("Goodbye! 👋")
            manager.close()
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
            












