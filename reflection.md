# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions the user should be able to do:
1. Add a pet
2. Schedule a task for a pet (like a walk or feeding)
3. See today's tasks

- Briefly describe your initial UML design.

Four classes: an Owner has Pets, each Pet has Tasks, and a Scheduler works with the Owner to organize everything.

- What classes did you include, and what responsibilities did you assign to each?

Task: one care activity (description, time, frequency, done or not).
Pet: name and species, plus its list of tasks.
Owner: name and list of pets, and can get all tasks from every pet.
Scheduler: gets all tasks from every pet through the Owner and builds today's schedule.

**b. Design changes**

- Did your design change during implementation?

Yes. The Task class gained a `due_date` field, and the Scheduler gained `sort_by_time`, `filter_tasks`, `detect_conflicts`, and `mark_task_complete`. The final UML is in `diagrams/uml_final.mmd`.

- If yes, describe at least one change and why you made it.

I added `due_date` because recurring tasks need a date to calculate the next occurrence (today + 1 day for daily, + 7 days for weekly).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers the time of each task, how often it repeats (once, daily, or weekly), its due date, whether it is done, and which pet it belongs to.

- How did you decide which constraints mattered most?

I decided time mattered most because a pet owner mainly needs to know what to do next, so sorting by time and warning about same-time tasks came first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler only flags tasks that start at exactly the same time. It does not check whether tasks overlap, because tasks don't have a duration. This is reasonable for a simple pet-care app, where a warning about two things at the same time is the most useful check, and it keeps the logic easy to read.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Claude to brainstorm the classes and their attributes and methods, draft the UML diagram, generate the class skeleton, and fill in the methods, the demo script, and the first tests. The most helpful prompts were ones that named the specific file or step I was on and asked for one small thing at a time.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

After the skeleton was written, the AI's review suggested a change to the Task class. I did not accept it right away because I wanted to keep the design simple at this point, and I decided to revisit it only if the code actually needed it.

Later, when I asked the AI how the conflict detection method could be simplified, it suggested a slightly shorter version using `defaultdict`. I kept my version because it was already efficient (one pass over the tasks) and just as easy to read.

I checked the AI's work by running `python main.py` and comparing the printed schedule with what I expected, by running `python -m pytest` (10 tests passed), and by trying the Streamlit app flow of adding a pet, adding tasks, seeing a conflict warning, and marking a task complete. I also compared each step against the assignment instructions.

Features that helped most: the assistant could edit several files at once (adding `due_date` touched the Task class, the Scheduler, and the demo script) and could run the code and tests right away to check them. I worked through the project one step at a time in a single session, approving each step before it was made, which kept the work organized without needing separate chats.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I wrote 10 tests. They cover marking a task complete, adding a task to a pet, sorting tasks by time across two pets, daily and weekly recurrence, one-off tasks creating no new task, conflict detection for same-time tasks, no false conflicts for different times or completed tasks, empty owners and pets, and filtering by pet and status.

- Why were these tests important?

The scheduler's value is in sorting, recurrence, and conflicts being right, and the edge cases (empty lists, unknown pet) are where programs usually crash.

**b. Confidence**

- How confident are you that your scheduler works correctly?

About 4 out of 5. All 10 tests pass and the demo and app behave as expected.

- What edge cases would you test next if you had more time?

Invalid time strings like "25:99" or "8am" (sorting relies on the "HH:MM" format), tasks that overlap in duration, and the Streamlit UI more thoroughly.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The scheduling features working together across pets, shown in both the CLI demo and the app.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add task durations so overlapping tasks can be detected, and validate the time input.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Making each step small and checking it by running the code worked better than building everything at once. The AI was most useful when it provided suggestions when I gave it the framework of what I wanted for a particular section.
