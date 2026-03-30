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
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def get_all_tasks(self):
        result = []
        for pet in self.pets:
            for task in pet.get_tasks():
                result.append((pet.name, task))
        return result


class Scheduler:

    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self):
        return sorted(self.owner.get_all_tasks(), key=lambda pair: pair[1].time)

    def filter_tasks(self, pet_name=None, status=None):
        tasks = self.owner.get_all_tasks()
        if pet_name:
            tasks = [(p, t) for p, t in tasks if p == pet_name]
        if status == "complete":
            tasks = [(p, t) for p, t in tasks if t.is_complete]
        elif status == "incomplete":
            tasks = [(p, t) for p, t in tasks if not t.is_complete]
        return tasks

    def detect_conflicts(self):
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