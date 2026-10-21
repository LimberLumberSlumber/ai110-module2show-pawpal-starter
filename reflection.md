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
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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

I checked the AI's work by running `python main.py` and comparing the printed schedule with what I expected, and by running `python -m pytest` (2 tests passed). I also compared each step against the assignment instructions.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
