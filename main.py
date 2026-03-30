from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Alex")

dog = Pet(name="Buddy", species="Dog")
cat = Pet(name="Luna",  species="Cat")

dog.add_task(Task("Morning walk",   "07:00", "daily"))
dog.add_task(Task("Heartworm pill", "08:00", "weekly"))
dog.add_task(Task("Evening walk",   "18:00", "daily"))

cat.add_task(Task("Breakfast",       "07:00", "daily"))
cat.add_task(Task("Vet appointment", "14:00", "once"))

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner)

print("=" * 45)
print("        🐾 TODAY'S SCHEDULE")
print("=" * 45)
for pet_name, task in scheduler.sort_by_time():
    icon = "✅" if task.is_complete else "⬜"
    print(f"  {icon}  [{task.time}]  {pet_name:8} → {task.description}  ({task.frequency})")

print("\n" + "=" * 45)
print("        ⚠️  CONFLICT WARNINGS")
print("=" * 45)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for w in conflicts:
        print(f"  {w}")
else:
    print("  ✅ No conflicts!")