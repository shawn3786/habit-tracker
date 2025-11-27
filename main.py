# Main Streamlit Module for Habit Tracking Application
# Provides web interface for users to interact with the system

import streamlit as st
import sys
from datetime import datetime
from manager import HabitManager

# Initialize session state for habit manager
if 'manager' not in st.session_state:
    st.session_state.manager = HabitManager()

def display_menu():
    """
    Shows the main menu options to the user in Streamlit.
    """
    st.sidebar.title("🍃 Habit Tracking Application")
    st.sidebar.markdown("---")
    
    menu_options = [
        "Create New Habit",
        "Mark Habit as Completed", 
        "View All Habits",
        "View Habit Details",
        "Delete Habit",
        "View Overall Summary",
        "View Analytics",
        "Exit"
    ]
    
    choice = st.sidebar.selectbox("Navigate to:", menu_options)
    return menu_options.index(choice) + 1

def show_habit_list(titles):
    """
    Display habit list in Streamlit format.
    """
    for i, title in enumerate(titles, 1):
        st.write(f"{i}. {title}")

def main():
    """
    Entry point for the Streamlit application.
    """
    st.title("🍃 Habit Tracking Application")
    
    manager = st.session_state.manager
    choice = display_menu()
    
    # Handle habit creation
    if choice == 1:
        st.header("Create New Habit")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Enter habit name:").strip()
        
        with col2:
            frequency = st.selectbox("Enter frequency:", ["daily", "weekly"])
        
        if st.button("Create Habit"):
            if not title:
                st.error("Habit name cannot be empty.")
            else:
                if manager.create_habit(title, frequency):
                    st.success(f"✅ Habit '{title}' created successfully!")
                else:
                    st.error(f"❌ Failed to create habit. Maybe '{title}' already exists?")

    # MARK COMPLETE
    elif choice == 2:
        st.header("Mark Habit as Completed")
        titles = manager.get_habit_titles()

        if not titles:
            st.warning("No habits found. Please create a habit first.")
        else:
            selected_title = st.selectbox("Select habit to mark complete:", titles)
            
            if st.button("Mark as Completed"):
                if selected_title not in titles:
                    st.error(f"Habit '{selected_title}' not found.")
                else:
                    if manager.mark_habit_complete(selected_title):
                        st.success(f"✅ Habit '{selected_title}' marked as completed!")
                    else:
                        st.error("❌ Failed to mark habit as completed.")

    # All HABITS
    elif choice == 3:
        st.header("All Habits")
        habits = manager.list_habits()

        if not habits:
            st.info("No habits found.")
        else:
            for i, habit in enumerate(habits, 1):
                last_completion = habit.get_last_completion_date()
                last_str = last_completion.strftime("%Y-%m-%d") if last_completion else "Never"
                streak = habit.calculate_current_streak()
                st.write(f"{i}. **{habit.title}** ({habit.frequency}) - Streak: {streak} - Last: {last_str}")

    # HABIT DETAILS
    elif choice == 4:
        st.header("Habit Details")
        titles = manager.get_habit_titles()

        if not titles:
            st.info("No habits found.")
        else:
            selected_title = st.selectbox("Select habit to view details:", titles)
            
            if st.button("View Details"):
                habit = manager.get_habit_by_title(selected_title)
                if habit:
                    st.subheader(f"Details for: {habit.title}")
                    st.text(habit.summary())
                else:
                    st.error(f"Habit '{selected_title}' not found.")

    # DELETE HABIT
    elif choice == 5:
        st.header("Delete Habit")
        titles = manager.get_habit_titles()

        if not titles:
            st.info("No habits found.")
        else:
            selected_title = st.selectbox("Select habit to delete:", titles)
            
            if st.button("Delete Habit", type="primary"):
                if selected_title not in titles:
                    st.error(f"Habit '{selected_title}' not found.")
                else:
                    st.warning(f"Are you sure you want to delete '{selected_title}'?")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("Yes, Delete", type="secondary"):
                            if manager.delete_habit(selected_title):
                                st.success(f"✅ Habit '{selected_title}' deleted successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete habit.")
                    
                    with col2:
                        if st.button("Cancel", type="secondary"):
                            st.info("Deletion cancelled.")

    # Overall Summary
    elif choice == 6:
        st.header("Overall Summary")
        summary = manager.summary()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Habits", summary['total_habits'])
            st.metric("Longest Streak", summary['strongest_streak'])
        
        with col2:
            rate = summary.get('average_completion_rate')
            if isinstance(rate, (int, float)):
                st.metric("Average Completion Rate", f"{rate * 100:.1f}%")
            else:
                st.metric("Average Completion Rate", "N/A")
            
            st.metric("Broken Habits", summary['broken_habits'])
            st.metric("Unbroken Habits", summary['unbroken_habits'])

    # Analytics
    elif choice == 7:
        st.header("Analytics Dashboard")
        
        analytics_options = [
            "View Completion Rates",
            "View Habits by Streak Ranking", 
            "View Habits by Consistency",
            "View Broken Habits",
            "View Unbroken Habits",
            "View Daily Habits",
            "View Weekly Habits"
        ]
        
        sub_choice = st.selectbox("Select Analytics View:", analytics_options)
        
        # Displays completion rates
        if sub_choice == "View Completion Rates":
            st.subheader("Completion Rates")
            rates = manager.get_completion_rates()
            avg_rate = manager.get_average_completion_rate()

            for habit_name, rate in rates.items():
                percentage = rate * 100
                st.write(f"**{habit_name}**: {percentage:.1f}%")

            st.metric("Average Completion Rate", f"{avg_rate * 100:.1f}%")
                       
        # Shows habits ranked
        elif sub_choice == "View Habits by Streak Ranking":
            st.subheader("Habits Ranked by Current Streak")
            ranked = manager.get_habits_ranked_by_streak()

            for i, habit in enumerate(ranked, 1):
                streak = habit.calculate_current_streak()
                st.write(f"{i}. **{habit.title}**: {streak} days")

         # Shows habits ranked by consistency
        elif sub_choice == "View Habits by Consistency":
            st.subheader("Habits Ranked by Consistency")
            ranked = manager.get_habits_ranked_by_consistency()

            for i, habit in enumerate(ranked, 1):
                percentage = habit.completion_rate() * 100
                st.write(f"{i}. **{habit.title}**: {percentage:.1f}%")

        # Shows habits that have been broken
        elif sub_choice == "View Broken Habits":
            st.subheader("Broken Habits")
            broken = manager.broken_habits()

            if not broken:
                st.success("No broken habits! Great job! 🎉")
            else:
                for habit in broken:
                    st.write(f"• **{habit.title}** ({habit.frequency})")

        # Shows habits that have never been broken
        elif sub_choice == "View Unbroken Habits":
            st.subheader("Unbroken Habits")
            unbroken = manager.get_unbroken_habits()

            if not unbroken:
                st.info("No unbroken habits found.")
            else:
                for habit in unbroken:
                    streak = habit.calculate_current_streak()
                    st.write(f"• **{habit.title}** ({habit.frequency}) - Streak: {streak}")

        # Shows daily habits
        elif sub_choice == "View Daily Habits":
            st.subheader("Daily Habits")
            daily_habits = manager.filter_by_frequency("daily")
            if not daily_habits:
                st.info("No daily habits found.")    
            else:
                for habit in daily_habits:
                    streak = habit.calculate_current_streak()
                    st.write(f"• **{habit.title}** - Current Streak: {streak} days")

        # Shows weekly habits
        elif sub_choice == "View Weekly Habits":
            st.subheader("Weekly Habits")
            weekly_habits = manager.filter_by_frequency("weekly")
            if not weekly_habits:
                st.info("No weekly habits found.")
            else:                                                
                for habit in weekly_habits:
                    streak = habit.calculate_current_streak()
                    st.write(f"• **{habit.title}** - Current Streak: {streak} weeks")

    # EXIT
    elif choice == 8:
        st.header("Thank You!")
        st.success("Thank you for using the Habit Tracking Application!")
        st.info("Goodbye! 👋")
        manager.close()
        
        if st.button("Restart Application"):
            st.rerun()

if __name__ == "__main__":
    main()
