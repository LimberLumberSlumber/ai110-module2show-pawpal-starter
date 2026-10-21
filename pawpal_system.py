from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    description: str
    time: str
    frequency: str
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return self.tasks


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every pet's tasks combined in one list."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks across the owner's pets."""
        return self.owner.get_all_tasks()

    def get_todays_schedule(self) -> list[Task]:
        """Return today's tasks across all pets."""
        return self.get_all_tasks()

    def sort_by_time(self) -> list[Task]:
        """Return all tasks across all pets sorted by their time."""
        return sorted(self.get_all_tasks(), key=lambda task: task.time)

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for open tasks scheduled at the same date and time."""
        slots: dict[tuple[date, str], list[str]] = {}
        for pet in self.owner.pets:
            for task in pet.get_tasks():
                if not task.completed:
                    slots.setdefault((task.due_date, task.time), []).append(
                        f"{task.description} ({pet.name})"
                    )
        return [
            f"Warning: {len(entries)} tasks at {time} on {due}: {', '.join(entries)}"
            for (due, time), entries in slots.items()
            if len(entries) > 1
        ]

    def mark_task_complete(self, task: Task) -> Task | None:
        """Mark a task complete and, if it is daily or weekly, add the next occurrence to its pet."""
        task.mark_complete()
        days = {"daily": 1, "weekly": 7}.get(task.frequency)
        if days is None:
            return None
        for pet in self.owner.pets:
            if any(t is task for t in pet.get_tasks()):
                next_task = Task(
                    task.description,
                    task.time,
                    task.frequency,
                    due_date=task.due_date + timedelta(days=days),
                )
                pet.add_task(next_task)
                return next_task
        return None

    def filter_tasks(self, pet_name: str | None = None, completed: bool | None = None) -> list[Task]:
        """Return tasks across all pets, optionally filtered by pet name and/or completion status."""
        tasks = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.get_tasks():
                if completed is None or task.completed == completed:
                    tasks.append(task)
        return tasks
