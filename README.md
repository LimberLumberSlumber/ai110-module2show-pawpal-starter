# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Implementation summary

The logic layer lives in `pawpal_system.py` and has four classes:

- `Task`: one care activity with a description, time, frequency (once, daily, or weekly), due date, and whether it is done. It can mark itself complete.
- `Pet`: a name, species, and a list of its tasks. Tasks can be added to it.
- `Owner`: a name and a list of pets. `get_all_tasks()` collects every pet's tasks into one list.
- `Scheduler`: takes an Owner and works on tasks across all of that owner's pets by calling `Owner.get_all_tasks()`. It sorts, filters, detects conflicts, and handles recurring tasks.

The classes work together like this: an Owner has Pets, each Pet has Tasks, and the Scheduler reads from the Owner so it sees tasks from every pet, not just one. The UML is in `diagrams/uml_final.mmd` (the original draft is in `diagrams/uml_draft.mmd`).

### Features

- Sorting by time across all pets (`Scheduler.sort_by_time()`)
- Filtering by pet name and/or completion status (`Scheduler.filter_tasks()`)
- Conflict warnings when two open tasks are at the same time (`Scheduler.detect_conflicts()`)
- Daily and weekly recurrence: completing a recurring task creates the next one (`Scheduler.mark_task_complete()`)
- A Streamlit app (`app.py`) that shows the sorted schedule, filters, conflict warnings, and a mark-complete button

### Running the demo, app, and tests

```bash
python main.py            # CLI demo
streamlit run app.py      # Streamlit app
python -m pytest          # tests
```

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule for Jordan
========================================
All tasks, sorted by time
----------------------------------------
  08:00  Morning walk (Mochi) [daily] - done
  09:30  Grooming (Mochi) [once] - to do
  09:30  Feeding (Luna) [daily] - to do
  12:00  Medication (Luna) [daily] - to do
  18:00  Evening walk (Mochi) [daily] - to do

Tasks still to do
----------------------------------------
  18:00  Evening walk (Mochi) [daily] - to do
  09:30  Grooming (Mochi) [once] - to do
  09:30  Feeding (Luna) [daily] - to do
  12:00  Medication (Luna) [daily] - to do

Mochi's tasks
----------------------------------------
  18:00  Evening walk (Mochi) [daily] - to do
  08:00  Morning walk (Mochi) [daily] - done
  09:30  Grooming (Mochi) [once] - to do

Conflict check
----------------------------------------
  Warning: 2 tasks at 09:30 on 2026-10-21: Grooming (Mochi), Feeding (Luna)

Completed 'Evening walk' due 2026-10-21
New task created: 'Evening walk' due 2026-10-22
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Optional: run with coverage (requires `pip install pytest-cov` first):
pytest --cov
```

The tests in `tests/test_pawpal.py` cover:

- Marking a task complete and adding a task to a pet
- Sorting tasks by time across multiple pets
- Daily and weekly recurrence (a new task is created for the next occurrence) and one-off tasks creating nothing
- Conflict detection for same-time tasks across pets, with no false warnings for different times or completed tasks
- Edge cases: an owner with no pets, a pet with no tasks, and filtering by pet, by status, and by an unknown pet

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\CodePathFall2026\CodePathAI110Fall2026\CodePathAIFall2026Projects\Unit5Project2\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 10 items

tests\test_pawpal.py ..........                                          [100%]

============================== 10 passed in 0.05s ==============================
```

Confidence level: ⭐⭐⭐⭐ (4/5). All 10 tests pass and cover the main scheduling behaviors and edge cases. I did not test overlapping durations, invalid time strings, or the Streamlit UI.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Returns all tasks from every pet sorted by their time. |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks across all pets by pet name, completion status, or both. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns a warning message for each time that has more than one open task, for the same pet or different pets. Only exact matching times are flagged, not overlapping durations. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Marks a task complete. If it is daily or weekly, a new task is added to the same pet due 1 day or 7 days later, using `timedelta`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

Run the app with `streamlit run app.py`. In the app a user can add pets, add tasks for a pet (with a time and a frequency), view the schedule, filter it, and mark tasks complete.

1. Enter a pet name and species and click **Add pet**. The pet appears in the "Current pets" table and stays in memory (the Owner is kept in `st.session_state`).
2. Pick the pet, enter a task title, a time such as `08:00`, and a frequency, then click **Add task**. Add a few tasks, including two at the same time.
3. Look at **Today's Schedule**. Tasks from all pets appear sorted by time (`Scheduler.sort_by_time()`).
4. Check the conflict warning. If two open tasks share a time, a `st.warning` names both tasks and their pets (`Scheduler.detect_conflicts()`). If not, a success message says there are no conflicts.
5. Use **Show pet** and **Show status** to filter the table (`Scheduler.filter_tasks()`).
6. Pick a task and click **Mark complete**. If it is daily or weekly, a new task is created for the next date and a success message says so (`Scheduler.mark_task_complete()`).

Key Scheduler behaviors shown: sorting across pets, filtering, conflict warnings, and recurring tasks. The CLI demo (`python main.py`) shows the same behaviors in the terminal:

```
Today's Schedule for Jordan
========================================
All tasks, sorted by time
----------------------------------------
  08:00  Morning walk (Mochi) [daily] - done
  09:30  Grooming (Mochi) [once] - to do
  09:30  Feeding (Luna) [daily] - to do
  12:00  Medication (Luna) [daily] - to do
  18:00  Evening walk (Mochi) [daily] - to do

Tasks still to do
----------------------------------------
  18:00  Evening walk (Mochi) [daily] - to do
  09:30  Grooming (Mochi) [once] - to do
  09:30  Feeding (Luna) [daily] - to do
  12:00  Medication (Luna) [daily] - to do

Mochi's tasks
----------------------------------------
  18:00  Evening walk (Mochi) [daily] - to do
  08:00  Morning walk (Mochi) [daily] - done
  09:30  Grooming (Mochi) [once] - to do

Conflict check
----------------------------------------
  Warning: 2 tasks at 09:30 on 2026-10-21: Grooming (Mochi), Feeding (Luna)

Completed 'Evening walk' due 2026-10-21
New task created: 'Evening walk' due 2026-10-22
```

**Screenshot or video** *(optional)*: none included.
