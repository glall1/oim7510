import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl
    import altair as alt
    from pathlib import Path

    database = mo.notebook_dir() / "database.duckdb"
    data_dir = mo.notebook_dir() / "data"
    as_of = "2026-11-08"

    def ask(sql):
        with duckdb.connect(str(database), read_only=True) as _con:
            return _con.sql(sql).pl()

    mo.md("# BabsonAI Labs — Database Project, Part A\nScenario A | As-of date: November 8, 2026")
    return alt, ask, data_dir, database, duckdb, mo, pl


@app.cell
def _(mo):
    mo.md("""
    ## The Tables
    Five related tables: PEOPLE, PROJECTS, PROJECT_ASSIGNMENTS, TASKS and EXPENSES. Primary and foreign keys identify records and enforce relationships. The task-staffing rule requires a separate SQL check.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## The Data
    The CSVs were generated with a fixed seed in `make_data.py` for the 12-month period ending 2026-11-08. **Exactly two deliberate staffing-rule exceptions are tasks 1 and 2.** All other task assignments are either unassigned or staffed on their project.
    """)
    return


@app.cell
def _(data_dir, database, duckdb):
    # One build cell: remove the previous database, create all tables, load all CSVs,
    # and create the reusable view. All writes use one closing context manager.
    import csv
    assert all((data_dir / name).exists() for name in (
        "people.csv", "projects.csv", "project_assignments.csv", "tasks.csv", "expenses.csv"
    )), "Missing CSV files: run make_data.py first."
    if database.exists():
        database.unlink()

    with duckdb.connect(str(database)) as _con:
        _con.execute("""
            CREATE TABLE PEOPLE (
                person_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                work_email VARCHAR NOT NULL UNIQUE,
                title VARCHAR NOT NULL,
                start_date DATE NOT NULL,
                manager_id INTEGER,
                FOREIGN KEY (manager_id) REFERENCES PEOPLE(person_id)
            )
        """)
        _con.execute("""
            CREATE TABLE PROJECTS (
                project_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL,
                client_name VARCHAR,
                category VARCHAR NOT NULL,
                budget DECIMAL(12,2) NOT NULL CHECK (budget > 0),
                start_date DATE NOT NULL,
                status VARCHAR NOT NULL CHECK (status IN ('planned','active','paused','done'))
            )
        """)
        _con.execute("""
            CREATE TABLE PROJECT_ASSIGNMENTS (
                project_id INTEGER NOT NULL,
                person_id INTEGER NOT NULL,
                project_role VARCHAR NOT NULL,
                hours_per_week INTEGER NOT NULL CHECK (hours_per_week BETWEEN 1 AND 40),
                joined_date DATE NOT NULL,
                PRIMARY KEY (project_id, person_id),
                FOREIGN KEY (project_id) REFERENCES PROJECTS(project_id),
                FOREIGN KEY (person_id) REFERENCES PEOPLE(person_id)
            )
        """)
        _con.execute("""
            CREATE TABLE TASKS (
                task_id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL,
                assigned_person_id INTEGER,
                description VARCHAR NOT NULL,
                created_date DATE NOT NULL,
                due_date DATE NOT NULL,
                completed_date DATE,
                CHECK (completed_date IS NULL OR completed_date >= created_date),
                FOREIGN KEY (project_id) REFERENCES PROJECTS(project_id),
                FOREIGN KEY (assigned_person_id) REFERENCES PEOPLE(person_id)
            )
        """)
        _con.execute("""
            CREATE TABLE EXPENSES (
                expense_id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL,
                expense_date DATE NOT NULL,
                amount DECIMAL(12,2) NOT NULL CHECK (amount > 0),
                category VARCHAR NOT NULL,
                note VARCHAR,
                FOREIGN KEY (project_id) REFERENCES PROJECTS(project_id)
            )
        """)

        def insert_csv(table, filename, columns):
            with (data_dir / filename).open(newline="", encoding="utf-8") as file:
                rows = list(csv.DictReader(file))
            sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
            for row in rows:
                _con.execute(sql, [row[column] if row[column] != "" else None for column in columns])
            return len(rows)

        # Managers precede their reports in the generated people.csv.
        inserted = {
            "PEOPLE": insert_csv("PEOPLE", "people.csv", ["person_id", "first_name", "last_name", "work_email", "title", "start_date", "manager_id"]),
            "PROJECTS": insert_csv("PROJECTS", "projects.csv", ["project_id", "name", "client_name", "category", "budget", "start_date", "status"]),
            "PROJECT_ASSIGNMENTS": insert_csv("PROJECT_ASSIGNMENTS", "project_assignments.csv", ["project_id", "person_id", "project_role", "hours_per_week", "joined_date"]),
            "TASKS": insert_csv("TASKS", "tasks.csv", ["task_id", "project_id", "assigned_person_id", "description", "created_date", "due_date", "completed_date"]),
            "EXPENSES": insert_csv("EXPENSES", "expenses.csv", ["expense_id", "project_id", "expense_date", "amount", "category", "note"]),
        }
        _con.execute("""
            CREATE VIEW project_budget_summary AS
            SELECT p.project_id, p.name AS project_name, p.status, p.budget,
                   COALESCE(SUM(e.amount), 0) AS total_expenses,
                   ROUND(100.0 * COALESCE(SUM(e.amount), 0) / p.budget, 2) AS expense_utilization_pct
            FROM PROJECTS p LEFT JOIN EXPENSES e ON p.project_id = e.project_id
            GROUP BY p.project_id, p.name, p.status, p.budget
        """)
    print("Built database from CSVs:", inserted)
    build_complete = True
    return


@app.cell
def _(alt, data_dir, mo, pl):
    mo.md("## A Look at the Data")
    # Read a CSV directly with Polars, rather than reading a SQL view.
    expenses_csv = pl.read_csv(data_dir / "expenses.csv", try_parse_dates=True)
    category_counts = expenses_csv.group_by("category").len().sort("len", descending=True)
    print(category_counts)
    category_chart = alt.Chart(category_counts).mark_bar().encode(
        x=alt.X("category:N", title="Expense category"),
        y=alt.Y("len:Q", title="Number of expenses"),
        tooltip=["category:N", "len:Q"]
    ).properties(title="Synthetic expenses by category", width=500, height=280)
    mo.md("The category totals are fairly similar because the generator chooses expense categories randomly. A real AI startup might spend more on GPU cloud and software, so this is a limitation of the synthetic data; the generator was not adjusted to model realistic category weights.")
    category_chart
    return


@app.cell
def _(ask, mo):
    mo.md("## Row Counts")
    counts = ask("""
        SELECT 'PEOPLE' AS table_name, COUNT(*) AS rows FROM PEOPLE
        UNION ALL SELECT 'PROJECTS', COUNT(*) FROM PROJECTS
        UNION ALL SELECT 'PROJECT_ASSIGNMENTS', COUNT(*) FROM PROJECT_ASSIGNMENTS
        UNION ALL SELECT 'TASKS', COUNT(*) FROM TASKS
        UNION ALL SELECT 'EXPENSES', COUNT(*) FROM EXPENSES
    """)
    print(counts)
    expected_row_count = {"PEOPLE": 25, "PROJECTS": 12, "PROJECT_ASSIGNMENTS": 68, "TASKS": 275, "EXPENSES": 175}
    assert dict(zip(counts["table_name"].to_list(), counts["rows"].to_list())) == expected_row_count
    violations = ask("""
        SELECT t.task_id FROM TASKS t
        LEFT JOIN PROJECT_ASSIGNMENTS a
          ON a.project_id = t.project_id AND a.person_id = t.assigned_person_id
        WHERE t.assigned_person_id IS NOT NULL AND a.person_id IS NULL
        ORDER BY t.task_id
    """)
    assert violations["task_id"].to_list() == [1, 2]
    print("Intentional staffing-rule violations:", violations["task_id"].to_list())
    return


@app.cell
def _(database, duckdb, mo):
    mo.md("## A Row It Refuses")
    # A negative project budget violates CHECK (budget > 0).
    try:
        with duckdb.connect(str(database)) as _con:
            _con.execute("""
                INSERT INTO PROJECTS (project_id, name, client_name, category, budget, start_date, status)
                VALUES (9999, 'Rejected project', NULL, 'Internal', -5000, '2026-11-08', 'planned')
            """)
        raise AssertionError("The invalid row was unexpectedly accepted")
    except duckdb.ConstraintException as error:
        print("DuckDB refused the invalid row:", error)
    return


@app.cell
def _(ask, mo):
    mo.md("## Answers You Already Knew")
    known_answers = [
        ("People generated", "SELECT COUNT(*) AS answer FROM PEOPLE", 25),
        ("Projects generated", "SELECT COUNT(*) AS answer FROM PROJECTS", 12),
        ("Expenses generated", "SELECT COUNT(*) AS answer FROM EXPENSES", 175),
    ]
    for label, sql, expected in known_answers:
        actual = ask(sql)["answer"][0]
        print(f"{label}: expected {expected}; SQL returned {actual}")
        assert actual == expected
    return


@app.cell
def _(alt, ask, mo, pl):
    mo.md("## A View\nThe saved `project_budget_summary` view answers a weekly management question: which projects have spent the largest share of their budgets?")
    budget_rows = ask("""
        SELECT project_name, budget, total_expenses, expense_utilization_pct
        FROM project_budget_summary ORDER BY expense_utilization_pct DESC
    """).with_columns(
        pl.col("budget").cast(pl.Float64),
        pl.col("total_expenses").cast(pl.Float64),
        pl.col("expense_utilization_pct").cast(pl.Float64)
    )
    print(budget_rows.head(5))
    budget_chart = alt.Chart(budget_rows).mark_bar().encode(
        x=alt.X("expense_utilization_pct:Q", title="Budget used (%)"),
        y=alt.Y("project_name:N", sort="-x", title="Project"),
        tooltip=["project_name:N", alt.Tooltip("budget:Q", format="$,.2f"),
                 alt.Tooltip("total_expenses:Q", format="$,.2f"),
                 alt.Tooltip("expense_utilization_pct:Q", format=".2f")]
    ).properties(title="BabsonAI Labs: Project Budget Utilization", width=550, height=350)
    budget_chart
    return


if __name__ == "__main__":
    app.run()
