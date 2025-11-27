# Main CLI Module for Habit Tracking Application
# Provides command-line interface for users to interact with the system

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

# Helper function to display habit list with numbers
def show_habit_list(titles):
    for i, title in enumerate(titles, 1):
        print(f"{i}. {title}")


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
            title = input("Enter habit name: ")

            if not title:
                print("Habit name cannot be empty.")
                continue

            frequency = input("Enter frequency (daily/weekly): ").strip().lower()

            if frequency not in ['daily', 'weekly']:
                print("Frequency must be 'daily' or 'weekly'.")
                continue

            if manager.create_habit(title, frequency):
                print(f"✅ Habit '{title}' created successfully!")
            else:
                print(f"❌ Failed to create habit. Maybe '{title}' already exists?")

        # MARK COMPLETE
        elif choice == "2":
            print("\n--- Mark Habit as Completed ---")
            titles = manager.get_habit_titles()

            if not titles:
                print("No habits found. Please create a habit first.")
                continue

            show_habit_list(titles)
            title = input("Enter habit name to mark complete: ").strip()

            if title not in titles:
                print(f"Habit '{title}' not found.")
                continue

            if manager.mark_habit_complete(title):
                print(f"✅ Habit '{title}' marked as completed!")
            else:
                print("❌ Failed to mark habit as completed.")


        # All HABITS
        elif choice == "3":
            print("\n--- All Habits ---")
            habits = manager.list_habits()

            if not habits:
                print("No habits found.")
                continue

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
                continue

            show_habit_list(titles)

            title = input("Enter habit name to view details: ")
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
                continue

            show_habit_list(titles)
            title = input("Enter habit name to delete: ")

            if title not in titles:
                print(f"Habit '{title}' not found.")
                continue

            confirm = input(f"Are you sure you want to delete '{title}'? (y/N): ").strip().lower()
            if confirm == 'y':
                if manager.delete_habit(title):
                    print(f"✅ Habit '{title}' deleted successfully!")
                else:
                    print("❌ Failed to delete habit.")
            else:
                print("Deletion cancelled.")

       
        #Overall Summary
        elif choice == "6":
            print("\n--- Overall Summary ---")
            summary = manager.summary()
            print(f"Total Habits: {summary['total_habits']}")
            print(f"Longest Streak: {summary['strongest_streak']}")
            rate = summary.get('average_completion_rate')
            if isinstance(rate, (int, float)):
                print(f"average Completion Rate: {rate * 100:.1f}%")
            else:
                print("average Completion Rate: N/A")
            print(f"Broken Habits: {summary['broken_habits']}")
            print(f"Unbroken Habits: {summary['unbroken_habits']}")
        
        # Analytics
        elif choice == "7":

            while True:
                print("\n--- Analytics Menu ---")
                print("1. View Completion Rates")
                print("2. View Longest overall Streak")
                print("3. View longest Streak of current Habit")
                print("4. View Broken Habits")
                print("5. View Unbroken Habits")
                print("6. View Daily Habits")
                print("7. View Weekly Habits")
                print("8. View Habits Ranked by Current Streak")
                print("9. Back to Main Menu")

                sub_choice = input("Enter your choice (1-8): ").strip()
    
                #Displays completion rates
                if sub_choice == '1':
                    print("\n--- Completion Rates ---")
                    rates = manager.get_completion_rates()
                    avg_rate = manager.get_average_completion_rate()
    
                    for habit_name, rate in rates.items():
                        percentage = rate * 100
                        print(f"{habit_name}: {percentage:.1f}%")

                    print(f"\nAverage Completion Rate: {avg_rate * 100:.1f}%")
                           
                #Shows longest streak overall
                elif sub_choice == '2':
                    print("\n--- Longest Overall Streak ---")
                    longest_streak = manager.largest_streak()

                    for habit in manager.habits:
                        if habit.calculate_current_streak() == longest_streak:
                            print(f"Habit: {habit.title} - Streak: {longest_streak} days")
                            break
                        
                        
                #Shows longest streak for a specific habit
                elif sub_choice == '3':
                    print("\n--- Longest Streak of Current Habit ---")
                    title = input("Enter habit name: ")

                    if not title:
                        print("Habit name cannot be empty.")
                        continue
                    streak = manager.largest_streak_for_habit(title)
                    if streak is not None:
                        print(f"The longest streak for '{title}' is {streak} days.")
                    else:
                        print(f"Habit '{title}' not found.")
    
                #Shows habits that have been broken
                elif sub_choice == '4':
                    print("\n--- Broken Habits ---")
                    broken = manager.broken_habits()
    
                    if not broken:
                        print("No broken habits! Great job! 🎉")
                        continue
    
                    for habit in broken:
                        print(f"• {habit.title} ({habit.frequency})")
    
                #Shows habits that have never been broken
                elif sub_choice == '5':
                    print("\n--- Unbroken Habits ---")
                    unbroken = manager.get_unbroken_habits()
    
                    if not unbroken:
                        print("No unbroken habits found.")
                        continue
    
                    for habit in unbroken:
                        print(f"• {habit.title} ({habit.frequency}) - Streak: {habit.calculate_current_streak()}")
    
                #Shows daily habits
                elif sub_choice == '6':
                    print("\n--- Daily Habits ---")
                    daily_habits = manager.filter_by_frequency("daily")
                    if not daily_habits:
                        print("No daily habits found.")    
                    else:
                        for habit in daily_habits:
                            streak = habit.calculate_current_streak()
                            print(f"• {habit.title} - Current Streak: {streak} days")
    
                #Shows weekly habits
                elif sub_choice == '7':
                    print("\n--- Weekly Habits ---")
                    weekly_habits = manager.filter_by_frequency("weekly")
                    if not weekly_habits:
                        print("No weekly habits found.")
                    else:                                                
                        for habit in weekly_habits:
                            streak = habit.calculate_current_streak()
                            print(f"• {habit.title} - Current Streak: {streak} weeks")

                #Shows habits ranked by current streak
                elif sub_choice == '8':
                    print("\n--- Habits Ranked by Current Streak ---")
                    ranked = manager.get_habits_ranked_by_streak()

                    for i, habit in enumerate(ranked, 1):
                        streak = habit.calculate_current_streak()
                        print(f"{i}. {habit.title}: {streak} days")
    
                #Back to main menu
                elif sub_choice == '9':
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
if __name__ == "__main__":
    main()
            












