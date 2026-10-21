from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Jordan")

mochi = Pet("Mochi", "dog")
luna = Pet("Luna", "cat")
owner.add_pet(mochi)
owner.add_pet(luna)

# Tasks are added out of time order on purpose
mochi.add_task(Task("Evening walk", "18:00", "daily"))
luna.add_task(Task("Feeding", "09:30", "daily"))
morning_walk = Task("Morning walk", "08:00", "daily")
mochi.add_task(morning_walk)
luna.add_task(Task("Medication", "12:00", "daily"))
mochi.add_task(Task("Grooming", "09:30", "once"))  # same time as Luna's feeding

scheduler = Scheduler(owner)
morning_walk.mark_complete()


def pet_name_for(task):
    for pet in owner.pets:
        if any(t is task for t in pet.get_tasks()):
            return pet.name


def print_tasks(title, tasks):
    print(title)
    print("-" * 40)
    if not tasks:
        print("  (none)")
    for task in tasks:
        status = "done" if task.completed else "to do"
        print(f"  {task.time}  {task.description} ({pet_name_for(task)}) [{task.frequency}] - {status}")
    print()


print(f"Today's Schedule for {owner.name}")
print("=" * 40)
print_tasks("All tasks, sorted by time", scheduler.sort_by_time())
print_tasks("Tasks still to do", scheduler.filter_tasks(completed=False))
print_tasks("Mochi's tasks", scheduler.filter_tasks(pet_name="Mochi"))

print("Conflict check")
print("-" * 40)
conflicts = scheduler.detect_conflicts()
for warning in conflicts:
    print(f"  {warning}")
if not conflicts:
    print("  No conflicts found")
print()

# Completing a daily task creates the same task for the next day
evening_walk = scheduler.filter_tasks(pet_name="Mochi", completed=False)[0]
next_task = scheduler.mark_task_complete(evening_walk)
print(f"Completed '{evening_walk.description}' due {evening_walk.due_date}")
print(f"New task created: '{next_task.description}' due {next_task.due_date}")
