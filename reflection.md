# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial design used the four required classes: `Owner`, `Pet`, `Task`, and `Scheduler`. `Owner` stores the pet owner's name and a list of pets. `Pet` stores identifying information such as name, species, age, and a list of tasks. `Task` represents one care activity with a description, due time, due date, duration, priority, frequency, and completion status. `Scheduler` acts as the brain of the system by collecting tasks across all pets and organizing them into a useful schedule.

**b. Design changes**

The design became more specific during implementation. At first, I only thought about simple task storage, but I added `due_date`, `frequency`, and `duration_minutes` to make the scheduler more realistic. I also kept the conflict detection lightweight by checking for exact same date and time instead of building a full overlapping time-block system. This kept the project understandable while still meeting the scheduling requirements.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers task time, task date, priority, completion status, pet name, and recurrence frequency. Time matters most for building a daily plan because a pet owner needs to know what to do first. Priority is also important because medication, feeding, and walks may matter more than low-priority grooming or enrichment tasks.

**b. Tradeoffs**

One tradeoff is that conflict detection only checks for exact same date and time. For example, it will flag two tasks at 08:00, but it does not yet detect that a 30-minute task at 08:00 overlaps with a task at 08:15. This is reasonable for this project because the rubric asks for basic conflict detection, and exact-time conflict warnings are clear, reproducible, and easy for a user to understand.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI for design brainstorming, class responsibility planning, method naming, and thinking through scheduler algorithms. The most helpful prompts were specific prompts such as asking how the `Scheduler` should retrieve tasks from an `Owner`, how to sort tasks by `HH:MM` time strings, and what tests would verify a pet scheduler.

**b. Judgment and verification**

I did not accept every AI idea as-is. One suggestion was to make the scheduler more complex by tracking full overlapping time blocks and availability windows. I chose not to use that version because it was harder to read and beyond the required scope. I verified the final version by running `python main.py` to inspect the CLI output and `python -m pytest` to confirm that the automated tests passed.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, adding a task to a pet, sorting tasks across multiple pets, recurring daily task creation, and conflict detection. These tests are important because they verify the most central behaviors of the system: tasks can be changed, pets can hold tasks, the scheduler can organize tasks across pets, recurrence works, and schedule conflicts are visible.

**b. Confidence**

My confidence level is 5 out of 5 stars for the current project scope. The scheduler works correctly for the required features and the tests pass. If I had more time, I would test overlapping tasks with duration, invalid time formats in the UI, pets with no tasks, and weekly recurrence over multiple completions.

---

## 5. Reflection

**a. What went well**

I am most satisfied with connecting the OOP design to real scheduling behavior. The classes are separate but work together: `Owner` has pets, pets have tasks, and `Scheduler` organizes everything across pets.

**b. What you would improve**

In another iteration, I would add persistent storage with JSON so tasks remain after restarting the app. I would also improve the Streamlit UI with edit and delete buttons and a more advanced overlap detector that considers duration.

**c. Key takeaway**

The biggest takeaway is that AI can help brainstorm and scaffold a system, but the human still needs to act as the lead architect. I had to decide what was realistic, readable, and appropriate for the rubric, then verify the system with demo output and tests.
