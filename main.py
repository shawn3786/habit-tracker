import streamlit as st
from manager import HabitManager

# Initialize manager only once
if "manager" not in st.session_state:
    st.session_state.manager = HabitManager()

manager = st.session_state.manager

st.title("Habit Tracking Application")

menu = st.sidebar.selectbox(
    "Menu",
    ["Create Habit", "Mark Complete", "View All Habits", "Habit Details", "Delete Habit", "Summary", "Analytics"]
)

# CREATE HABIT
if menu == "Create Habit":
    st.subheader("Create New Habit")

    title = st.text_input("Habit name")
    frequency = st.selectbox("Frequency", ["daily", "weekly"])

    if st.button("Create"):
        if manager.create_habit(title, frequency):
            st.success(f"Habit '{title}' created!")
        else:
            st.error("Habit already exists.")

# MARK COMPLETE
elif menu == "Mark Complete":
    st.subheader("Mark Habit as Completed")
    titles = manager.get_habit_titles()

    if titles:
        choice = st.selectbox("Select habit", titles)
        if st.button("Mark as completed"):
            manager.mark_habit_complete(choice)
            st.success(f"'{choice}' marked complete!")
    else:
        st.info("No habits found.")

# VIEW ALL HABITS
elif menu == "View All Habits":
    st.subheader("All Habits")
    habits = manager.list_habits()
    for h in habits:
        st.write(h.summary())

# SUMMARY
elif menu == "Summary":
    st.subheader("Overall Summary")
    summary = manager.summary()
    st.write(summary)

# ANALYTICS
elif menu == "Analytics":
    st.subheader("Analytics")
    st.write(manager.get_completion_rates())
