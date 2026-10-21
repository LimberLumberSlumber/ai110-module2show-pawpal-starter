import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    st.session_state.owner.add_pet(Pet(pet_name, species))

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table(
        [{"name": pet.name, "species": pet.species} for pet in st.session_state.owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

pets = st.session_state.owner.pets
selected_pet_name = st.selectbox("Pet", [pet.name for pet in pets]) if pets else None

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5 = st.columns(2)
with col4:
    task_time = st.text_input("Time", value="08:00")
with col5:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

if st.button("Add task", disabled=not pets):
    selected_pet = next(pet for pet in pets if pet.name == selected_pet_name)
    selected_pet.add_task(Task(task_title, task_time, frequency))

scheduler = Scheduler(st.session_state.owner)
pet_name_of = {id(task): pet.name for pet in pets for task in pet.get_tasks()}

st.markdown("### Today's Schedule")

if not pets:
    st.info("Add a pet first, then add tasks for it.")
elif not scheduler.get_all_tasks():
    st.info("No tasks yet. Add one above.")
else:
    open_tasks = scheduler.filter_tasks(completed=False)
    if open_tasks:
        to_complete = st.selectbox(
            "Mark a task complete",
            range(len(open_tasks)),
            format_func=lambda i: (
                f"{open_tasks[i].time} {open_tasks[i].description} ({pet_name_of[id(open_tasks[i])]})"
            ),
        )
        if st.button("Mark complete"):
            done = open_tasks[to_complete]
            next_task = scheduler.mark_task_complete(done)
            if next_task:
                st.success(
                    f"Completed '{done.description}'. Next {done.frequency} task created for {next_task.due_date}."
                )
            else:
                st.success(f"Completed '{done.description}'.")
            pet_name_of = {id(task): pet.name for pet in pets for task in pet.get_tasks()}

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No scheduling conflicts.")

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        pet_filter = st.selectbox("Show pet", ["All"] + [pet.name for pet in pets])
    with filter_col2:
        status_filter = st.selectbox("Show status", ["All", "To do", "Done"])

    shown = scheduler.filter_tasks(
        pet_name=None if pet_filter == "All" else pet_filter,
        completed={"All": None, "To do": False, "Done": True}[status_filter],
    )
    shown_ids = {id(task) for task in shown}
    rows = [
        {
            "time": task.time,
            "task": task.description,
            "pet": pet_name_of[id(task)],
            "frequency": task.frequency,
            "due": str(task.due_date),
            "status": "done" if task.completed else "to do",
        }
        for task in scheduler.sort_by_time()
        if id(task) in shown_ids
    ]
    if rows:
        st.table(rows)
    else:
        st.info("No tasks match these filters.")
