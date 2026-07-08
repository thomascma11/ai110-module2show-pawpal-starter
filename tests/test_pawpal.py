"""Tests for PawPal+ core scheduler behavior."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_changes_status():
    task = Task("Feed breakfast", "07:00")
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet("Mochi", "cat")
    pet.add_task(Task("Medication", "08:00"))
    assert len(pet.tasks) == 1


def test_scheduler_sorts_tasks_chronologically_across_pets():
    owner = Owner("Jordan")
    dog = Pet("Biscuit", "dog")
    cat = Pet("Mochi", "cat")
    dog.add_task(Task("Walk", "09:00"))
    cat.add_task(Task("Feed", "07:30"))
    owner.add_pet(dog)
    owner.add_pet(cat)

    sorted_pairs = Scheduler(owner).sort_by_time()

    assert [task.description for _, task in sorted_pairs] == ["Feed", "Walk"]


def test_daily_recurring_task_creates_next_day_task():
    owner = Owner("Jordan")
    dog = Pet("Biscuit", "dog")
    today = date.today()
    dog.add_task(Task("Morning walk", "08:00", today, 30, "high", "daily"))
    owner.add_pet(dog)

    Scheduler(owner).mark_task_complete("Biscuit", "Morning walk")

    assert dog.tasks[0].completed is True
    assert len(dog.tasks) == 2
    assert dog.tasks[1].due_date == today + timedelta(days=1)
    assert dog.tasks[1].completed is False


def test_scheduler_detects_conflicts_across_pets():
    owner = Owner("Jordan")
    dog = Pet("Biscuit", "dog")
    cat = Pet("Mochi", "cat")
    dog.add_task(Task("Walk", "08:00"))
    cat.add_task(Task("Medication", "08:00"))
    owner.add_pet(dog)
    owner.add_pet(cat)

    conflicts = Scheduler(owner).detect_conflicts()

    assert len(conflicts) == 1
    assert "Conflict at 08:00" in conflicts[0]
