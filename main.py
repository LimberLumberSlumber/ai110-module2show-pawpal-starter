from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Jordan")

mochi = Pet("Mochi", "dog")
luna = Pet("Luna", "cat")
owner.add_pet(mochi)
owner.add_pet(luna)

mochi.add_task(Task("Morning walk", "08:00", "daily"))
mochi.add_task(Task("Evening walk", "18:00", "daily"))
luna.add_task(Task("Feeding", "09:30", "daily"))

scheduler = Scheduler(owner)
all_tasks = scheduler.get_todays_schedule()

print(f"Today's Schedule for {owner.name} ({len(all_tasks)} tasks)")
print("=" * 40)
for pet in owner.pets:
    print(f"{pet.name} ({pet.species})")
    for task in pet.get_tasks():
        status = "done" if task.completed else "to do"
        print(f"  {task.time}  {task.description} [{task.frequency}] - {status}")
