from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_owner_with_two_pets():
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)
    return owner, mochi, luna


def test_mark_complete_changes_status():
    task = Task("Morning walk", "08:00", "daily")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task("Feeding", "09:30", "daily"))

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_orders_tasks_across_pets():
    owner, mochi, luna = make_owner_with_two_pets()
    mochi.add_task(Task("Evening walk", "18:00", "daily"))
    luna.add_task(Task("Feeding", "09:30", "daily"))
    mochi.add_task(Task("Morning walk", "08:00", "daily"))

    sorted_times = [task.time for task in Scheduler(owner).sort_by_time()]

    assert sorted_times == ["08:00", "09:30", "18:00"]


def test_completing_daily_task_creates_next_day_task():
    owner, mochi, _ = make_owner_with_two_pets()
    walk = Task("Morning walk", "08:00", "daily")
    mochi.add_task(walk)

    new_task = Scheduler(owner).mark_task_complete(walk)

    assert walk.completed is True
    assert new_task.due_date == walk.due_date + timedelta(days=1)
    assert len(mochi.get_tasks()) == 2


def test_completing_weekly_task_creates_task_seven_days_later():
    owner, mochi, _ = make_owner_with_two_pets()
    bath = Task("Bath", "10:00", "weekly", due_date=date(2026, 1, 1))
    mochi.add_task(bath)

    new_task = Scheduler(owner).mark_task_complete(bath)

    assert new_task.due_date == date(2026, 1, 8)


def test_completing_one_off_task_creates_no_new_task():
    owner, mochi, _ = make_owner_with_two_pets()
    vet = Task("Vet visit", "14:00", "once")
    mochi.add_task(vet)

    result = Scheduler(owner).mark_task_complete(vet)

    assert result is None
    assert len(mochi.get_tasks()) == 1


def test_detect_conflicts_flags_same_time_across_pets():
    owner, mochi, luna = make_owner_with_two_pets()
    mochi.add_task(Task("Grooming", "09:30", "once"))
    luna.add_task(Task("Feeding", "09:30", "daily"))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "Grooming (Mochi)" in warnings[0]
    assert "Feeding (Luna)" in warnings[0]


def test_detect_conflicts_ignores_different_times_and_completed_tasks():
    owner, mochi, luna = make_owner_with_two_pets()
    mochi.add_task(Task("Walk", "08:00", "daily"))
    luna.add_task(Task("Feeding", "09:30", "daily"))
    done = Task("Old task", "08:00", "once")
    done.mark_complete()
    mochi.add_task(done)

    assert Scheduler(owner).detect_conflicts() == []


def test_empty_owner_and_pet_without_tasks_return_empty_lists():
    scheduler = Scheduler(Owner("Jordan"))
    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []

    owner, _, _ = make_owner_with_two_pets()
    assert Scheduler(owner).sort_by_time() == []


def test_filter_tasks_by_pet_status_and_unknown_pet():
    owner, mochi, luna = make_owner_with_two_pets()
    walk = Task("Walk", "08:00", "daily")
    mochi.add_task(walk)
    luna.add_task(Task("Feeding", "09:30", "daily"))
    walk.mark_complete()
    scheduler = Scheduler(owner)

    assert [t.description for t in scheduler.filter_tasks(pet_name="Luna")] == ["Feeding"]
    assert [t.description for t in scheduler.filter_tasks(completed=True)] == ["Walk"]
    assert scheduler.filter_tasks(pet_name="Nobody") == []
