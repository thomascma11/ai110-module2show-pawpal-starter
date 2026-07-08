"""Core object-oriented logic for the PawPal+ pet care scheduler."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Optional


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """Represents one pet care task such as feeding, walking, medication, or grooming."""

    description: str
    due_time: str
    due_date: date = field(default_factory=date.today)
    duration_minutes: int = 15
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate and normalize task values after creation."""
        self.priority = self.priority.lower().strip()
        self.frequency = self.frequency.lower().strip()
        if self.priority not in PRIORITY_ORDER:
            raise ValueError("priority must be low, medium, or high")
        datetime.strptime(self.due_time, "%H:%M")
        if self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be positive")

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Create the next task if this task is recurring."""
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            description=self.description,
            due_time=self.due_time,
            due_date=next_date,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            completed=False,
        )

    def display(self) -> str:
        """Return a readable one-line description for CLI or UI output."""
        status = "done" if self.completed else "open"
        return (
            f"{self.due_time} — {self.description} "
            f"({self.duration_minutes} min) [priority: {self.priority}, {status}]"
        )


@dataclass
class Pet:
    """Stores identifying information and care tasks for a pet."""

    name: str
    species: str
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def list_tasks(self) -> List[Task]:
        """Return this pet's tasks."""
        return list(self.tasks)

    def get_task(self, description: str) -> Optional[Task]:
        """Find a task by description."""
        for task in self.tasks:
            if task.description.lower() == description.lower():
                return task
        return None


@dataclass
class Owner:
    """Represents a pet owner who can manage multiple pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def list_pets(self) -> List[Pet]:
        """Return all pets owned by this owner."""
        return list(self.pets)

    def get_all_tasks(self) -> List[tuple[Pet, Task]]:
        """Return all tasks across all pets as pet-task pairs."""
        pairs: List[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.tasks:
                pairs.append((pet, task))
        return pairs


class Scheduler:
    """Retrieves, organizes, and manages tasks across an owner's pets."""

    def __init__(self, owner: Owner):
        """Create a scheduler connected to one owner."""
        self.owner = owner

    def all_tasks(self) -> List[tuple[Pet, Task]]:
        """Return all tasks across all pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: Optional[List[tuple[Pet, Task]]] = None) -> List[tuple[Pet, Task]]:
        """Sort pet-task pairs chronologically by date and time."""
        task_pairs = tasks if tasks is not None else self.all_tasks()
        return sorted(task_pairs, key=lambda item: (item[1].due_date, item[1].due_time))

    def sort_by_priority_then_time(self) -> List[tuple[Pet, Task]]:
        """Sort tasks by priority first, then by date and time."""
        return sorted(
            self.all_tasks(),
            key=lambda item: (PRIORITY_ORDER[item[1].priority], item[1].due_date, item[1].due_time),
        )

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
    ) -> List[tuple[Pet, Task]]:
        """Filter tasks by pet name, completion status, or priority."""
        results = self.all_tasks()
        if pet_name is not None:
            results = [pair for pair in results if pair[0].name.lower() == pet_name.lower()]
        if completed is not None:
            results = [pair for pair in results if pair[1].completed == completed]
        if priority is not None:
            results = [pair for pair in results if pair[1].priority == priority.lower()]
        return results

    def detect_conflicts(self) -> List[str]:
        """Return warnings for tasks scheduled at the same date and time."""
        seen: dict[tuple[date, str], tuple[Pet, Task]] = {}
        warnings: List[str] = []
        for pet, task in self.sort_by_time():
            key = (task.due_date, task.due_time)
            if key in seen:
                other_pet, other_task = seen[key]
                warnings.append(
                    f"Conflict at {task.due_time} on {task.due_date}: "
                    f"{other_pet.name}'s {other_task.description} and "
                    f"{pet.name}'s {task.description}."
                )
            else:
                seen[key] = (pet, task)
        return warnings

    def mark_task_complete(self, pet_name: str, description: str) -> Optional[Task]:
        """Mark a task complete and add the next occurrence if it recurs."""
        for pet, task in self.all_tasks():
            if pet.name.lower() == pet_name.lower() and task.description.lower() == description.lower():
                task.mark_complete()
                new_task = task.next_occurrence()
                if new_task is not None:
                    pet.add_task(new_task)
                return task
        return None

    def build_daily_plan(self, target_date: Optional[date] = None) -> List[str]:
        """Create readable schedule lines for one day across all pets."""
        selected_date = target_date or date.today()
        todays_tasks = [pair for pair in self.all_tasks() if pair[1].due_date == selected_date]
        sorted_tasks = self.sort_by_time(todays_tasks)
        lines: List[str] = []
        for pet, task in sorted_tasks:
            reason = f"scheduled by time and marked {task.priority} priority"
            lines.append(f"{task.due_time} — {pet.name}: {task.description} ({reason})")
        return lines
