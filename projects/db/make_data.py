
from pathlib import Path
from datetime import date, timedelta
import csv
import random

random.seed(1234)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)
AS_OF = date(2026, 11, 8)
WINDOW_START = AS_OF - timedelta(days=364)


def save_csv(name, columns, rows):
    with (DATA_DIR / name).open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    print(f'{name}: {len(rows)} rows')


def pick_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Cameron', 'Quinn', 'Parker', 'Jamie', 'Drew', 'Reese', 'Skyler', 'Hayden', 'Blake', 'Emerson', 'Rowan', 'Finley', 'Dakota', 'Charlie', 'Sage', 'Logan', 'Harper', 'Elliot']
last_names = ['Chen', 'Patel', 'Rivera', 'Johnson', 'Kim', 'Williams', 'Brown', 'Garcia', 'Lee', 'Martin', 'Thompson', 'Davis', 'Wilson', 'Anderson', 'Clark', 'Lewis', 'Walker', 'Hall', 'Allen', 'Young', 'King', 'Scott', 'Green', 'Baker', 'Adams']
titles = ['AI Engineer', 'Data Analyst', 'Project Manager', 'Software Developer', 'Business Analyst', 'Data Scientist']
people = []
for i, (first, last) in enumerate(zip(first_names, last_names), start=1):
    people.append(dict(person_id=i, first_name=first, last_name=last, work_email=f'{first.lower()}.{last.lower()}@babsonailabs.example', title='Co-Founder' if i <= 2 else random.choice(titles), start_date=pick_date(date(2022, 1, 1), date(2025, 10, 1)).isoformat(), manager_id='' if i <= 2 else random.randint(1, min(i-1, 6))))
save_csv('people.csv', ['person_id', 'first_name', 'last_name', 'work_email', 'title', 'start_date', 'manager_id'], people)

project_names = ['Retail Demand Forecasting', 'Customer Support AI', 'Inventory Optimization', 'Sales Prediction Engine', 'Healthcare Scheduling AI', 'Marketing Analytics Platform', 'Automated Invoice Processing', 'Customer Churn Prediction', 'Supply Chain Dashboard', 'Document Intelligence', 'Internal AI Training', 'AI Product Research']
clients = ['Northstar Retail', 'Beacon Health', 'Harbor Logistics', 'Summit Foods', 'BrightPath Consulting', 'Evergreen Markets']
projects = []
for i, name in enumerate(project_names, 1):
    category = 'Internal' if i in (11, 12) else random.choice(['Client Delivery', 'Research'])
    projects.append(dict(project_id=i, name=name, client_name='' if category == 'Internal' else random.choice(clients), category=category, budget=random.randrange(30000, 125001, 5000), start_date=pick_date(WINDOW_START, AS_OF - timedelta(days=120)).isoformat(), status=random.choice(['planned', 'active', 'paused', 'done'])))
save_csv('projects.csv', ['project_id', 'name', 'client_name', 'category', 'budget', 'start_date', 'status'], projects)

assignments = []
for project in projects:
    for person in random.sample(people, random.randint(4, 8)):
        joined = max(date.fromisoformat(project['start_date']), date.fromisoformat(person['start_date']))
        assignments.append(dict(project_id=project['project_id'], person_id=person['person_id'], project_role=random.choice(['Project Lead', 'Analyst', 'Developer', 'Technical Advisor']), hours_per_week=random.randint(1, 40), joined_date=joined.isoformat()))
save_csv('project_assignments.csv', ['project_id', 'person_id', 'project_role', 'hours_per_week', 'joined_date'], assignments)

staffed = {p['project_id']: [a for a in assignments if a['project_id'] == p['project_id']] for p in projects}
task_descriptions = ['Gather business requirements', 'Clean and validate data', 'Develop predictive model', 'Test AI application', 'Prepare client presentation', 'Build reporting dashboard', 'Review model performance', 'Document project findings', 'Conduct stakeholder interview', 'Deploy prototype']
tasks = []
for i in range(1, 276):
    project = projects[(i - 1) % len(projects)] if i <= 12 else random.choice(projects)
    pid = project['project_id']
    if i in (1, 2):
        # Exactly two deliberate staffing violations, for a later detection query.
        valid_ids = {a['person_id'] for a in staffed[pid]}
        assigned_id = random.choice([p['person_id'] for p in people if p['person_id'] not in valid_ids])
        earliest = max(date.fromisoformat(project['start_date']), date.fromisoformat(people[assigned_id - 1]['start_date']))
    elif random.random() < 0.15:
        assigned_id = ''
        earliest = date.fromisoformat(project['start_date'])
    else:
        assignment = random.choice(staffed[pid])
        assigned_id = assignment['person_id']
        earliest = date.fromisoformat(assignment['joined_date'])
    latest = min(AS_OF, earliest + timedelta(days=75))
    created = pick_date(earliest, latest)
    due = created + timedelta(days=random.randint(7, 35))
    completed = ''
    if created < AS_OF - timedelta(days=2) and random.random() < 0.60:
        completed = pick_date(created + timedelta(days=1), min(AS_OF, created + timedelta(days=50))).isoformat()
    tasks.append(dict(task_id=i, project_id=pid, assigned_person_id=assigned_id, description=random.choice(task_descriptions), created_date=created.isoformat(), due_date=due.isoformat(), completed_date=completed))
save_csv('tasks.csv', ['task_id', 'project_id', 'assigned_person_id', 'description', 'created_date', 'due_date', 'completed_date'], tasks)

expenses = []
for i in range(1, 176):
    project = projects[(i - 1) % len(projects)] if i <= 12 else random.choice(projects)
    start = date.fromisoformat(project['start_date'])
    expenses.append(dict(expense_id=i, project_id=project['project_id'], expense_date=pick_date(start, AS_OF).isoformat(), amount=round(random.uniform(50, 2500), 2), category=random.choice(['GPU cloud', 'Data labeling', 'Software', 'Travel']), note='Synthetic project expense'))
save_csv('expenses.csv', ['expense_id', 'project_id', 'expense_date', 'amount', 'category', 'note'], expenses)

assignment_keys = {(a['project_id'], a['person_id']) for a in assignments}
invalid_tasks = [t['task_id'] for t in tasks if t['assigned_person_id'] != '' and (t['project_id'], t['assigned_person_id']) not in assignment_keys]
assert invalid_tasks == [1, 2], invalid_tasks
assert len(people) == 25 and len(projects) >= 12 and len(tasks) >= 250 and len(expenses) >= 150
assert all(1 <= a['hours_per_week'] <= 40 for a in assignments)
assert all(date.fromisoformat(t['created_date']) <= AS_OF for t in tasks)
assert all(date.fromisoformat(e['expense_date']) <= AS_OF for e in expenses)
print(f'As-of date: {AS_OF}; 12-month window begins: {WINDOW_START}')
print(f'Intentional staffing violations (task IDs): {invalid_tasks}')
print('All generator checks passed.')