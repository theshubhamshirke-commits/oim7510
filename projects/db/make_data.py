"""Create fictional CSV data for Scenario A: BabsonAI Labs.

Save this file as projects/db/make_data.py in your course repository.
Run from the repository root: uv run python projects/db/make_data.py
Only Python's standard library is needed.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path


# Keep these dates and the seed fixed so the results can be reproduced.
SEED = 42
DATA_START = date(2025, 11, 1)
AS_OF = date(2026, 10, 31)
DATA_FOLDER = Path(__file__).resolve().parent / "data"

random.seed(SEED)


def random_date(first_day, last_day):
    """Choose a date within the given range, including both endpoints."""
    number_of_days = (last_day - first_day).days
    return first_day + timedelta(days=random.randint(0, number_of_days))


def write_csv(filename, rows):
    """Write a header and all the rows to one CSV file."""
    with (DATA_FOLDER / filename).open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{filename}: {len(rows)} rows")


# 1. PEOPLE: names, emails, and all other details are fictional.
names = [
    ("Aarav", "Shah"), ("Maya", "Chen"), ("Rohan", "Patel"),
    ("Sofia", "Garcia"), ("Ethan", "Brooks"), ("Anika", "Rao"),
    ("Liam", "Wilson"), ("Zara", "Khan"), ("Noah", "Kim"),
    ("Priya", "Mehta"), ("Lucas", "Reed"), ("Aisha", "Ali"),
    ("Oliver", "Park"), ("Nina", "Das"), ("Mateo", "Rivera"),
    ("Leah", "Morgan"), ("Arjun", "Nair"), ("Chloe", "Bennett"),
    ("Daniel", "Wong"), ("Isha", "Kapoor"), ("Amir", "Hassan"),
    ("Emma", "Clarke"), ("Kabir", "Joshi"), ("Grace", "Turner"),
    ("Omar", "Said"),
]

people = []
for person_id, name in enumerate(names, start=1):
    first_name, last_name = name

    if person_id <= 2:
        title = "Co-founder"
        manager_id = None
        start_date = DATA_START
    elif person_id <= 5:
        title = "Team Lead"
        manager_id = 1 if person_id <= 4 else 2
        start_date = DATA_START
    else:
        title = random.choice(["AI Engineer", "Data Analyst", "Product Manager"])
        manager_id = random.choice([3, 4, 5])
        start_date = random_date(DATA_START, date(2025, 11, 20))

    people.append({
        "person_id": person_id,
        "first_name": first_name,
        "last_name": last_name,
        "work_email": f"{first_name.lower()}.{last_name.lower()}@babsonai.example.test",
        "title": title,
        "start_date": start_date,
        "manager_id": manager_id,
    })

people_by_id = {person["person_id"]: person for person in people}


# 2. PROJECTS: two projects intentionally have no expenses.
project_details = [
    ("Customer Support Copilot", "Maple Retail", "LLM app", 12000, date(2025, 11, 1), "active"),
    ("Invoice Data Pipeline", "Harbor Services", "data pipeline", 18000, date(2025, 11, 1), "active"),
    ("Internal Knowledge Search", None, "internal tool", 20000, date(2025, 11, 1), "active"),
    ("Retail FAQ Assistant", "Cedar Market", "LLM app", 25000, date(2025, 12, 1), "active"),
    ("Lead Scoring Pipeline", "Oak Sales", "data pipeline", 22000, date(2026, 1, 1), "active"),
    ("Document Review Assistant", "Pine Consulting", "LLM app", 28000, date(2026, 2, 1), "active"),
    ("Sales Analytics Pipeline", "Birch Stores", "data pipeline", 24000, date(2026, 3, 1), "active"),
    ("Meeting Notes Assistant", None, "internal tool", 15000, date(2026, 4, 1), "active"),
    ("Restaurant Booking Assistant", "Elm Dining", "LLM app", 16000, date(2025, 12, 1), "done"),
    ("Inventory Data Pipeline", "Willow Supply", "data pipeline", 21000, date(2026, 1, 15), "paused"),
    ("Customer Feedback Pilot", "Aspen Goods", "LLM app", 8000, date(2026, 10, 1), "active"),
    ("Employee Onboarding Tool", None, "internal tool", 10000, AS_OF, "planned"),
]

projects = []
for project_id, details in enumerate(project_details, start=1):
    project_name, client_name, category, budget, start_date, status = details
    projects.append({
        "project_id": project_id,
        "project_name": project_name,
        "client_name": client_name,
        "category": category,
        "budget": f"{budget:.2f}",
        "start_date": start_date,
        "status": status,
    })

projects_by_id = {project["project_id"]: project for project in projects}

# These dates stop new activity on the completed and paused projects.
last_activity = {project_id: AS_OF for project_id in range(1, 13)}
last_activity[9] = date(2026, 6, 30)
last_activity[10] = date(2026, 8, 31)


# 3. PROJECT MEMBERSHIPS: five people per project; employee 25 has none.
memberships = []
for project in projects:
    project_id = project["project_id"]

    if project_id <= 3:
        other_people = [person_id for person_id in range(1, 25) if person_id not in [1, 3]]
        member_ids = [1, 3] + random.sample(other_people, 3)
    else:
        member_ids = random.sample(list(range(1, 25)), 5)

    for member_number, person_id in enumerate(member_ids):
        # Employee 3 commits 20 hours to each of three active projects.
        if person_id == 3 and project_id <= 3:
            weekly_hours = 20
        else:
            weekly_hours = random.choice([5, 10, 15, 20])

        memberships.append({
            "person_id": person_id,
            "project_id": project_id,
            "project_role": "Project lead" if member_number == 0 else "Contributor",
            "weekly_hours": weekly_hours,
            "joined_date": max(project["start_date"], people_by_id[person_id]["start_date"]),
        })

members_by_project = {}
for project_id in range(1, 13):
    members_by_project[project_id] = [
        member for member in memberships if member["project_id"] == project_id
    ]


# 4. TASKS: 298 valid tasks followed by exactly two membership violations.
task_descriptions = [
    "Review customer requirements", "Prepare evaluation examples",
    "Test the data import", "Review model responses",
    "Update the project documentation", "Check the dashboard results",
]
active_project_ids = [1, 2, 3, 4, 5, 6, 7, 8, 11]
tasks = []

for task_id in range(1, 299):
    unassigned = task_id % 10 == 0 or task_id == 298
    if unassigned:
        project_id = random.choice(active_project_ids)
    elif task_id in [1, 2]:
        project_id = 1
    else:
        project_id = random.randint(1, 11)

    project = projects_by_id[project_id]
    end_date = last_activity[project_id]

    if task_id == 1:
        created_date = DATA_START
    elif task_id == 2:
        created_date = AS_OF
    elif unassigned:
        created_date = random_date(max(project["start_date"], AS_OF - timedelta(days=59)), AS_OF)
    else:
        created_date = random_date(project["start_date"], end_date)

    if unassigned:
        assigned_person_id = None
        assigned_date = None
        completed_date = None
        due_date = created_date + timedelta(days=random.randint(5, 21))
    else:
        # Assign only after both task creation and the person's project join date.
        member = random.choice(members_by_project[project_id])
        assigned_person_id = member["person_id"]
        assigned_date = max(created_date, member["joined_date"])
        assigned_date = min(assigned_date + timedelta(days=random.randint(0, 3)), end_date)
        due_date = assigned_date + timedelta(days=random.randint(5, 21))

        if project["status"] == "done" or random.random() < 0.70:
            completed_date = min(assigned_date + timedelta(days=random.randint(1, 14)), end_date)
        else:
            completed_date = None

    tasks.append({
        "task_id": task_id,
        "project_id": project_id,
        "description": f"{random.choice(task_descriptions)} (task {task_id})",
        "created_date": created_date,
        "assigned_person_id": assigned_person_id,
        "assigned_date": assigned_date,
        "due_date": due_date,
        "completed_date": completed_date,
    })

# Employee 25 exists, but is not a member of project 1 (or any project).
# All other rules, including employment and task dates, remain valid.
for task_id, created_date, assigned_date in [
    (299, date(2026, 10, 12), date(2026, 10, 15)),
    (300, date(2026, 10, 13), date(2026, 10, 16)),
]:
    tasks.append({
        "task_id": task_id,
        "project_id": 1,
        "description": f"Review evaluation results (task {task_id})",
        "created_date": created_date,
        "assigned_person_id": 25,
        "assigned_date": assigned_date,
        "due_date": assigned_date + timedelta(days=7),
        "completed_date": None,
    })


# 5. EXPENSES: positive amounts with different ranges for each category.
amount_ranges_in_cents = {
    "GPU cloud": (30000, 400000),
    "data labeling": (15000, 120000),
    "software": (2500, 50000),
    "travel": (10000, 90000),
}
month_starts = [date(2025, 11, 1), date(2025, 12, 1)]
month_starts += [date(2026, month, 1) for month in range(1, 11)]
expenses = []

for expense_id in range(1, 181):
    if expense_id <= 12:
        project_id = 1
        expense_date = month_starts[expense_id - 1]
    elif expense_id == 13:
        project_id = 1
        expense_date = AS_OF
    else:
        project_id = random.randint(1, 10)
        expense_date = random_date(projects_by_id[project_id]["start_date"], last_activity[project_id])

    category = random.choices(
        ["GPU cloud", "data labeling", "software", "travel"],
        weights=[45, 25, 25, 5],
    )[0]
    lowest, highest = amount_ranges_in_cents[category]
    amount_cents = random.randint(lowest, highest)

    expenses.append({
        "expense_id": expense_id,
        "project_id": project_id,
        "expense_date": expense_date,
        "amount": f"{amount_cents / 100:.2f}",
        "category": category,
        "note": f"Fictional {category} charge for project {project_id}",
    })


# CHECK THE DATA BEFORE WRITING IT.
assert [len(people), len(projects), len(memberships), len(tasks), len(expenses)] == [25, 12, 60, 300, 180]

membership_pairs = set()
for member in memberships:
    pair = (member["person_id"], member["project_id"])
    assert pair not in membership_pairs
    membership_pairs.add(pair)
    assert 1 <= member["weekly_hours"] <= 40
    assert member["joined_date"] >= people_by_id[member["person_id"]]["start_date"]
    assert member["joined_date"] >= projects_by_id[member["project_id"]]["start_date"]

violations = []
for task in tasks:
    assert DATA_START <= task["created_date"] <= AS_OF
    assert task["created_date"] >= projects_by_id[task["project_id"]]["start_date"]
    assert task["due_date"] >= task["created_date"]
    if task["completed_date"] is not None:
        assert task["created_date"] <= task["completed_date"] <= AS_OF
        assert task["completed_date"] >= task["assigned_date"]
    if task["assigned_person_id"] is None:
        assert task["assigned_date"] is None
        assert task["completed_date"] is None
    else:
        assert task["created_date"] <= task["assigned_date"] <= AS_OF
        assert task["assigned_date"] >= people_by_id[task["assigned_person_id"]]["start_date"]
        pair = (task["assigned_person_id"], task["project_id"])
        if pair not in membership_pairs:
            violations.append(task["task_id"])

assert violations == [299, 300]
assert sum(task["assigned_person_id"] is None for task in tasks) == 30
assert all(float(expense["amount"]) > 0 for expense in expenses)
assert set(expense["project_id"] for expense in expenses) == set(range(1, 11))
assert len(set((expense["expense_date"].year, expense["expense_date"].month) for expense in expenses)) == 12
for expense in expenses:
    assert projects_by_id[expense["project_id"]]["start_date"] <= expense["expense_date"] <= last_activity[expense["project_id"]]


# Write five CSV files next to this script, inside data/.
DATA_FOLDER.mkdir(parents=True, exist_ok=True)
write_csv("people.csv", people)
write_csv("projects.csv", projects)
write_csv("project_memberships.csv", memberships)
write_csv("tasks.csv", tasks)
write_csv("expenses.csv", expenses)

print(f"Data period: {DATA_START} to {AS_OF}")
print(f"Random seed: {SEED}")
print("Validation passed. Intentional membership violations: tasks 299 and 300.")
