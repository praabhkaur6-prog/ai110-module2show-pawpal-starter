# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I designed four classes for PawPal+:
- **Task**: Holds one care activity with a description, time, frequency,
  and completion status. It is responsible for knowing whether it recurs.
- **Pet**: Stores a pet's name, species, and list of tasks. It is
  responsible for adding and returning its own tasks.
- **Owner**: Manages a list of pets and can retrieve all tasks across
  every pet in one combined list.
- **Scheduler**: The "brain" of the system. It is responsible for
  sorting tasks by time, filtering them by pet or status, and detecting
  scheduling conflicts.

**b. Design changes**

Yes, my design changed during implementation. I added a `due_date`
field to the `Task` class that was not in my original skeleton. I needed
it so that when a recurring task is marked complete, the next occurrence
could be calculated using Python's `timedelta`. Without `due_date`,
the recurrence logic had no way to know what date to schedule next.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers:
- **Time**: Tasks are sorted chronologically by their HH:MM time string
- **Pet**: Tasks can be filtered to show only one pet's tasks
- **Completion status**: Tasks can be filtered to show only incomplete
  or complete tasks

I prioritized time as the main constraint because a pet owner's most
important need is knowing what to do and when throughout the day.

**b. Tradeoffs**

My conflict detection only flags tasks at the **exact same time**
(e.g. both at "08:00"). It does not detect overlapping durations —
for example, a 30-minute task at 08:00 and a task at 08:15 would not
be flagged as a conflict even though they overlap in real life.

This tradeoff is reasonable because tasks in PawPal+ don't currently
track duration. Keeping conflict detection simple means it runs fast
and never crashes, which is better than a complex system that might
break or give confusing results.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI tools throughout the project in several ways:
- **Design**: Asked AI to help brainstorm what attributes and methods
  each class should have before writing any code
- **Debugging**: When I got an IndentationError in pawpal_system.py,
  I used AI to identify where the spacing was wrong
- **Code generation**: Used AI to scaffold the initial class skeletons
  and generate the test suite in test_pawpal.py
- **Explaining concepts**: Asked AI to explain what `st.session_state`
  does in Streamlit so I understood why it was needed

The most helpful prompts were specific ones like "how do I sort a list
of tuples by a field inside the second element using a lambda."

**b. Judgment and verification**

When AI suggested using a list of tuples to track seen time slots in
`detect_conflicts()`, I changed it to use a dictionary instead. A
dictionary lets me look up whether a time slot is already taken in
constant time (O(1)) rather than looping through a list every time.
I verified this by thinking through the logic manually and confirming
the conflict warning appeared correctly when I ran `python main.py`.

---

## 4. Testing and Verification

**a. What you tested**

I tested six behaviors:
1. Marking a task complete changes `is_complete` to True
2. Adding a task to a pet increases its task count by 1
3. Tasks added out of order come back sorted chronologically
4. Two tasks at the same time trigger a conflict warning
5. Completing a daily task returns a new task for the next day
6. Completing a one-time task returns None (no recurrence)

These tests were important because they cover the core logic that the
entire app depends on. If sorting or conflict detection broke, the UI
would show wrong information to the user.

**b. Confidence**

I am confident (4 out of 5 stars) that the core scheduler works
correctly — all 6 tests pass. If I had more time, I would test these
edge cases:
- A pet with zero tasks (empty schedule)
- Two tasks at the same time for the same pet (not different pets)
- A weekly task completing near the end of the month (date rollover)
- Invalid time formats like "8:00" instead of "08:00"

---

## 5. Reflection

**a. What went well**

I am most satisfied with the conflict detection and recurring task
logic. These felt like real algorithms — not just storing data, but
actually reasoning about it. Seeing the conflict warning appear in
the Streamlit UI after I added two tasks at the same time was very
satisfying.

**b. What you would improve**

If I had another iteration, I would add task duration as a field so
that conflict detection could flag overlapping time ranges instead of
only exact matches. I would also add a way to mark tasks complete
directly in the Streamlit UI and have the next recurrence appear
automatically in the schedule.

**c. Key takeaway**

The most important thing I learned is that AI is a powerful tool but
you still need to understand your own code. When errors came up — like
the IndentationError or the task appearing twice in the schedule — AI
could suggest fixes, but I had to understand the problem to know
whether the fix was correct. The human architect still has to be in
charge of the design decisions.