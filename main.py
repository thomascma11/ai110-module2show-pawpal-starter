"""CLI demo for PawPal+ backend behavior."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
    """Create demo data for the PawPal+ CLI walkthrough."""
    owner = Owner("Jordan")
    biscuit = Pet("Biscuit", "dog", age=4)
    mochi = Pet("Mochi", "cat", age=2)

    biscuit.add_task(Task("Morning walk", "08:00", date.today(), 30, "high", "daily"))
    biscuit.add_task(Task("Grooming brush", "17:30", date.today(), 15, "low", "weekly"))
    mochi.add_task(Task("Breakfast feeding", "07:30", date.today(), 10, "high", "daily"))
    mochi.add_task(Task("Medication", "08:00", date.today(), 5, "high", "once"))

    owner.add_pet(biscuit)
    owner.add_pet(mochi)
    return owner


def main() -> None:
    """Run an end-to-end PawPal+ scheduler demonstration."""
    owner = build_demo_owner()
    scheduler = Scheduler(owner)

    print(f"Today's Schedule for {owner.name}")
    print("=" * 32)
    for pet, task in scheduler.sort_by_time():
        print(f"{pet.name}: {task.display()}")

    print("\nHigh Priority Tasks")
    print("=" * 32)
    for pet, task in scheduler.filter_tasks(priority="high", completed=False):
        print(f"{pet.name}: {task.display()}")

    print("\nConflict Warnings")
    print("=" * 32)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"WARNING: {warning}")
    else:
        print("No conflicts found.")

    scheduler.mark_task_complete("Biscuit", "Morning walk")
    print("\nAfter completing Biscuit's daily Morning walk:")
    for pet, task in scheduler.filter_tasks(pet_name="Biscuit"):
        print(f"{pet.name}: {task.display()} due {task.due_date}")


if __name__ == "__main__":
    main()
