import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+ Pet Care Manager")

# Session state = app memory between button clicks
# Without this, every click would wipe all your data
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Pet Owner")

owner = st.session_state.owner
scheduler = Scheduler(owner)

# ── ADD A PET ──────────────────────────────────────────
st.header("➕ Add a Pet")
with st.form("add_pet"):
    pet_name    = st.text_input("Pet's name")
    pet_species = st.selectbox("Species", ["Dog", "Cat", "Other"])
    submitted   = st.form_submit_button("Add Pet")

if submitted and pet_name:
    owner.add_pet(Pet(name=pet_name, species=pet_species))
    st.success(f"🎉 {pet_name} added to your family!")

# Show existing pets
if owner.pets:
    st.caption("Your pets: " + ", ".join(p.name for p in owner.pets))

st.divider()

# ── ADD A TASK ─────────────────────────────────────────
st.header("📝 Schedule a Task")
pet_names = [p.name for p in owner.pets]

if pet_names:
    with st.form("add_task"):
        selected  = st.selectbox("Which pet?", pet_names)
        desc      = st.text_input("What needs to be done?", value="Morning walk")
        time      = st.text_input("Time (HH:MM)", value="08:00")
        freq      = st.selectbox("How often?", ["once", "daily", "weekly"])
        task_btn  = st.form_submit_button("Schedule Task")

    if task_btn and desc:
        pet = next(p for p in owner.pets if p.name == selected)
        pet.add_task(Task(desc, time, freq))
        st.success(f"✅ '{desc}' scheduled for {selected} at {time}!")
else:
    st.info("👆 Add a pet first before scheduling tasks.")

st.divider()

# ── TODAY'S SCHEDULE ───────────────────────────────────
st.header("📅 Today's Schedule")
sorted_tasks = scheduler.sort_by_time()

if sorted_tasks:
    for pet_name, task in sorted_tasks:
        icon = "✅" if task.is_complete else "⬜"
        st.write(f"{icon} **[{task.time}]** {pet_name} — {task.description} *({task.frequency})*")
else:
    st.write("No tasks yet — add a pet and schedule some tasks!")

st.divider()

# ── CONFLICT WARNINGS ──────────────────────────────────
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.header("⚠️ Scheduling Conflicts")
    for warning in conflicts:
        st.warning(warning)