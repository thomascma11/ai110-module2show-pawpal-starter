"""Streamlit UI for PawPal+."""

from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A smart pet care scheduler using object-oriented Python logic.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name

st.subheader("Add a Pet")
with st.form("pet_form"):
    pet_name = st.text_input("Pet name", value="Biscuit")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=30, value=3)
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    if pet_name and pet_name not in [pet.name for pet in st.session_state.owner.pets]:
        st.session_state.owner.add_pet(Pet(pet_name, species, int(age)))
        st.success(f"Added {pet_name}.")
    else:
        st.warning("Please enter a new pet name.")

if not st.session_state.owner.pets:
    st.info("Add at least one pet to begin scheduling.")

st.subheader("Schedule a Task")
pet_options = [pet.name for pet in st.session_state.owner.pets]
with st.form("task_form"):
    selected_pet = st.selectbox("Pet", pet_options) if pet_options else None
    description = st.text_input("Task description", value="Morning walk")
    due_time = st.text_input("Due time (HH:MM)", value="08:00")
    duration = st.number_input("Duration minutes", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["high", "medium", "low"])
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    add_task = st.form_submit_button("Add task")

if add_task and selected_pet:
    try:
        task = Task(description, due_time, date.today(), int(duration), priority, frequency)
        for pet in st.session_state.owner.pets:
            if pet.name == selected_pet:
                pet.add_task(task)
                st.success(f"Added {description} for {selected_pet}.")
                break
    except ValueError as error:
        st.error(str(error))

st.subheader("Today's Smart Schedule")
scheduler = Scheduler(st.session_state.owner)
rows = []
for pet, task in scheduler.sort_by_time():
    rows.append(
        {
            "Pet": pet.name,
            "Time": task.due_time,
            "Task": task.description,
            "Duration": task.duration_minutes,
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Completed": task.completed,
        }
    )

if rows:
    st.table(rows)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No exact-time conflicts detected.")

    st.markdown("### High Priority Open Tasks")
    high_rows = [
        {"Pet": pet.name, "Time": task.due_time, "Task": task.description}
        for pet, task in scheduler.filter_tasks(priority="high", completed=False)
    ]
    st.table(high_rows if high_rows else [{"Status": "No high priority open tasks."}])
else:
    st.info("No tasks yet. Add tasks above to generate a schedule.")
