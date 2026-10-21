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

So far I built the logic layer in `pawpal_system.py` with four classes:

- `Task`: one care activity with a description, time, frequency, and whether it is done. It can mark itself complete.
- `Pet`: a name, species, and a list of its tasks. Tasks can be added to it.
- `Owner`: a name and a list of pets. `get_all_tasks()` collects every pet's tasks into one list.
- `Scheduler`: takes an Owner and gets tasks across all of that owner's pets by calling `Owner.get_all_tasks()`.

The classes work together like this: an Owner has Pets, each Pet has Tasks, and the Scheduler reads from the Owner so it sees tasks from every pet, not just one.

`main.py` is a demo script that creates an owner, two pets, and three tasks and prints today's schedule. Run it with `python main.py`. `tests/test_pawpal.py` has two basic tests, run with `python -m pytest`.

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
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Returns all tasks from every pet sorted by their time. |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks across all pets by pet name, completion status, or both. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns a warning message for each time that has more than one open task, for the same pet or different pets. Only exact matching times are flagged, not overlapping durations. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Marks a task complete. If it is daily or weekly, a new task is added to the same pet due 1 day or 7 days later, using `timedelta`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
