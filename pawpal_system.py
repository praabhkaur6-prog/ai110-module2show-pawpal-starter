from dataclasses import dataclass, field
from typing import List
from datetime import date, timedelta


@dataclass
class Task:
    description: str
    time: str
    frequency: str
    is_complete: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark task done. Returns next Task if recurring, else None."""
        self.is_complete = True
        if self.frequency == "daily":
            return Task(self.description, self.time, self.frequency,
                        due_date=self.due_date + timedelta(days=1))
        elif self.frequency == "weekly":
            return Task(self.description, self.time, self.frequency,
                        due_date=self.due_date + timedelta(weeks=1))
        return None


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's list."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's family."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return all tasks across all pets as (pet_name, task) pairs."""
        result = []
        for pet in self.pets:
            for task in pet.get_tasks():
                result.append((pet.name, task))
        return result


class Scheduler:

    def __init__(self, owner: Owner):
        """Needs an Owner to access all pets and tasks."""
        self.owner = owner

    def sort_by_time(self):
        """Return all tasks sorted earliest to latest."""
        return sorted(self.owner.get_all_tasks(), key=lambda pair: pair[1].time)

    def filter_tasks(self, pet_name=None, status=None):
        """Filter tasks by pet name and/or completion status."""
        tasks = self.owner.get_all_tasks()
        if pet_name:
            tasks = [(p, t) for p, t in tasks if p == pet_name]
        if status == "complete":
            tasks = [(p, t) for p, t in tasks if t.is_complete]
        elif status == "incomplete":
            tasks = [(p, t) for p, t in tasks if not t.is_complete]
        return tasks

    def detect_conflicts(self):
        """Return warnings when two tasks are scheduled at the exact same time."""
        seen = {}
        warnings = []
        for pet_name, task in self.owner.get_all_tasks():
            if task.time in seen:
                other_pet, other_task = seen[task.time]
                warnings.append(
                    f"⚠️ Conflict at {task.time}: "
                    f"'{task.description}' ({pet_name}) clashes with "
                    f"'{other_task.description}' ({other_pet})"
                )
            else:
                seen[task.time] = (pet_name, task)
        return warnings