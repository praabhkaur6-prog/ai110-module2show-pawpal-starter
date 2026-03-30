from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import timedelta

def test_mark_complete_changes_status():
    task = Task("Walk", "08:00", "once")
    task.mark_complete()
    assert task.is_complete == True

def test_add_task_increases_count():
    pet = Pet("Buddy", "Dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Walk", "08:00", "daily"))
    assert len(pet.get_tasks()) == 1

def test_sort_by_time_is_chronological():
    owner = Owner("Alex")
    pet = Pet("Buddy", "Dog")
    pet.add_task(Task("Dinner",     "18:00", "daily"))
    pet.add_task(Task("Walk",       "07:00", "daily"))
    pet.add_task(Task("Medication", "12:00", "daily"))
    owner.add_pet(pet)
    times = [t.time for _, t in Scheduler(owner).sort_by_time()]
    assert times == sorted(times)

def test_conflict_detection():
    owner = Owner("Alex")
    p1 = Pet("Buddy", "Dog")
    p2 = Pet("Luna",  "Cat")
    p1.add_task(Task("Walk",    "08:00", "daily"))
    p2.add_task(Task("Feeding", "08:00", "daily"))
    owner.add_pet(p1)
    owner.add_pet(p2)
    assert len(Scheduler(owner).detect_conflicts()) > 0

def test_daily_task_recurs_next_day():
    task = Task("Walk", "08:00", "daily")
    today = task.due_date
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)

def test_once_task_does_not_recur():
    task = Task("Vet visit", "14:00", "once")
    assert task.mark_complete() is None