# PawPal+ Smart Pet Care Scheduler

PawPal+ is a Python and Streamlit app that helps a busy pet owner organize daily care routines across multiple pets. It uses object-oriented programming to model owners, pets, tasks, and a scheduler that can sort, filter, detect conflicts, and handle recurring care tasks.

## Features

- Add an owner and multiple pets.
- Add pet care tasks with a description, due time, duration, priority, frequency, date, and completion status.
- View a daily schedule sorted by time across all pets.
- Filter tasks by pet, completion status, or priority.
- Detect exact-time conflicts across pets and show readable warnings.
- Mark recurring tasks complete and automatically create the next daily or weekly occurrence.
- Run a CLI demo through `main.py` before using the Streamlit UI.
- Verify behavior with a pytest suite.

## System Design

The core design uses four required classes:

| Class | Responsibility |
|------|----------------|
| `Owner` | Stores the owner's name and manages a list of pets. |
| `Pet` | Stores pet information and manages that pet's tasks. |
| `Task` | Represents one care task with time, date, duration, priority, frequency, and completion status. |
| `Scheduler` | Organizes tasks across all pets and provides sorting, filtering, conflict detection, recurrence, and plan-building logic. |

The final UML diagram is saved as Mermaid source in:

```text
diagrams/uml_final.mmd
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the CLI Demo

```bash
python main.py
```

## Sample CLI Output

```text
Today's Schedule for Jordan
================================
Mochi: 07:30 — Breakfast feeding (10 min) [priority: high, open]
Biscuit: 08:00 — Morning walk (30 min) [priority: high, open]
Mochi: 08:00 — Medication (5 min) [priority: high, open]
Biscuit: 17:30 — Grooming brush (15 min) [priority: low, open]

High Priority Tasks
================================
Biscuit: 08:00 — Morning walk (30 min) [priority: high, open]
Mochi: 07:30 — Breakfast feeding (10 min) [priority: high, open]
Mochi: 08:00 — Medication (5 min) [priority: high, open]

Conflict Warnings
================================
WARNING: Conflict at 08:00 on 2026-07-08: Biscuit's Morning walk and Mochi's Medication.

After completing Biscuit's daily Morning walk:
Biscuit: 08:00 — Morning walk (30 min) [priority: high, done] due 2026-07-08
Biscuit: 17:30 — Grooming brush (15 min) [priority: low, open] due 2026-07-08
Biscuit: 08:00 — Morning walk (30 min) [priority: high, open] due 2026-07-09
```

## Run the Streamlit App

```bash
streamlit run app.py
```

The app lets the user add pets, schedule tasks, view a sorted task table, see conflict warnings, and view high-priority open tasks.

## Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by due date and `HH:MM` time across all pets. |
| Priority scheduling | `Scheduler.sort_by_priority_then_time()` | Sorts high-priority tasks before medium and low tasks, then sorts by time. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name, completion status, and/or priority. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warning strings when two tasks share the same date and exact time. |
| Recurring tasks | `Task.next_occurrence()` and `Scheduler.mark_task_complete()` | Daily tasks recreate for the next day; weekly tasks recreate seven days later. |
| Daily plan text | `Scheduler.build_daily_plan()` | Produces readable schedule lines for a selected date. |

## Testing PawPal+

Run the full test suite:

```bash
python -m pytest
```

The tests cover task completion, adding tasks to pets, chronological sorting across pets, daily recurrence, and conflict detection.

Sample passing output:

```text
.....                                                                    [100%]
5 passed in 0.13s
```

Confidence level: ⭐⭐⭐⭐⭐ / 5. The scheduler is reliable for the current scope because the main object interactions and scheduling algorithms are verified with automated tests.

## Demo Walkthrough

1. The user starts in the Streamlit app and enters an owner name.
2. The user adds one or more pets with name, species, and age.
3. The user creates care tasks for each pet with due time, duration, priority, and frequency.
4. The app stores the owner object in `st.session_state`, so pets and tasks remain available during the session.
5. The app displays a sorted schedule table using `Scheduler.sort_by_time()`.
6. If two tasks are scheduled at the same exact date and time, the app displays a warning from `Scheduler.detect_conflicts()`.
7. The user can separately view high-priority open tasks using `Scheduler.filter_tasks()`.

## Project Files

```text
pawpal_system.py          # backend OOP classes and scheduler logic
main.py                   # CLI demo script
tests/test_pawpal.py      # pytest suite
app.py                    # Streamlit UI connected to backend classes
diagrams/uml_final.mmd    # final Mermaid UML source
reflection.md             # design and AI collaboration reflection
requirements.txt          # dependencies
```
