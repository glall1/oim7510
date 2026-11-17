import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from datetime import date

    as_of = date(2026, 11, 8)
    return (as_of,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # BabsonAI Labs — Database Project Part B
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### My Prediction

    I think joining PROJECTS, TASKS, and EXPENSES will result in a few thousand rows before grouping. This is because each task can be matched with multiple expenses within the same project, which increases the number of rows. For example, if a project has 5 tasks and 3 expenses, the join would produce 15 rows.
    """)
    return


@app.cell
def _(mo):
    import duckdb

    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell
def _(ask):
    ask("SELECT count(*) AS total_projects FROM PROJECTS")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Project Expenses vs. Budget

    Which projects have used the largest percentage of their budgets?
    """)
    return


@app.cell
def _(ask):

    ask("""
        SELECT
            project_name,
            budget,
            total_expenses,
            expense_utilization_pct AS budget_used_pct
        FROM project_budget_summary
        ORDER BY expense_utilization_pct DESC
    """)

    return


@app.cell
def _(ask):
    ask("""
        DESCRIBE TASKS
    """)
    return


@app.cell
def _(ask):
    ask("""
        DESCRIBE PEOPLE
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Retail Demand Forecasting has used the highest percentage of its budget at 64.97%, followed by Document Intelligence at 63.79% and Supply Chain Dashboard at 48.77%. These projects have used the largest shares of their budgets so far, which could be important for management to monitor.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Overdue and Unfinished Tasks

    Which tasks are overdue and unfinished, and who is responsible for them?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT t.task_id,
               p.name AS project_name,
               t.description AS task,
               t.due_date,
               pe.first_name || ' ' || pe.last_name AS assigned_person
        FROM TASKS AS t
        JOIN PROJECTS AS p
            ON t.project_id = p.project_id
        LEFT JOIN PEOPLE AS pe
            ON t.assigned_person_id = pe.person_id
        WHERE t.due_date < DATE '{as_of.isoformat()}'
          AND t.completed_date IS NULL
        ORDER BY t.due_date, p.name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As of November 8, 2026, BabsonAI Labs has **109 overdue and unfinished tasks** across its projects. The results show each task's deadline, project, and assigned employee, making it easier for managers to identify outstanding work and follow up with the appropriate team members. Some tasks are also unassigned, which may require additional attention.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Employee Workload Across Active Projects

    How many hours per week is each employee assigned across active projects, and who is assigned more than 40 hours?
    """)
    return


@app.cell
def _(ask):
    ask("""
        DESCRIBE PROJECT_ASSIGNMENTS
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT pe.person_id,
               pe.first_name || ' ' || pe.last_name AS employee_name,
               COUNT(pa.project_id) AS active_projects,
               COALESCE(SUM(pa.hours_per_week), 0) AS total_hours_per_week,
               CASE
                   WHEN COALESCE(SUM(pa.hours_per_week), 0) > 40
                   THEN 'Over 40 hours'
                   ELSE '40 hours or less'
               END AS workload_status
        FROM PEOPLE AS pe
        LEFT JOIN PROJECT_ASSIGNMENTS AS pa
            ON pe.person_id = pa.person_id
            AND pa.project_id IN (
                SELECT project_id
                FROM PROJECTS
                WHERE status = 'active'
            )
        GROUP BY pe.person_id, pe.first_name, pe.last_name
        ORDER BY total_hours_per_week DESC, employee_name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Out of 25 employees, 2 are assigned more than 40 hours per week across active projects. Riley Williams has 56 hours and Blake Lewis has 55 hours, with both working on 2 active projects. This suggests their workloads may need to be reviewed to prevent overworking.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Expense Categories Above Average

    Which expense categories had total spending above the average category total over the last 90 days?
    """)
    return


@app.cell
def _(ask):
    ask("""
        DESCRIBE EXPENSES
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        WITH category_totals AS (
            SELECT category,
                   SUM(amount) AS total_spending
            FROM EXPENSES
            WHERE expense_date BETWEEN
                  DATE '{as_of.isoformat()}' - INTERVAL 89 DAY
                  AND DATE '{as_of.isoformat()}'
            GROUP BY category
        )
        SELECT category,
               ROUND(total_spending, 2) AS total_spending,
               ROUND(
                   (SELECT AVG(total_spending)
                    FROM category_totals),
                   2
               ) AS average_category_spending
        FROM category_totals
        WHERE total_spending > (
            SELECT AVG(total_spending)
            FROM category_totals
        )
        ORDER BY total_spending DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    During the 90 days ending November 8, 2026, Travel ($37,504.52) and Software ($32,713.62) were the two expense categories with spending above the average category total of $28,831.04. Travel had the highest spending, suggesting it may be an area for management to review.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Projects With No Expenses

    Which projects have no recorded expenses?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT p.project_id,
               p.name AS project_name,
               p.status
        FROM PROJECTS AS p
        LEFT JOIN EXPENSES AS e
            ON p.project_id = e.project_id
        WHERE e.expense_id IS NULL
        ORDER BY p.name
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            p.name AS project_name,
            COUNT(e.expense_id) AS expense_count
        FROM PROJECTS AS p
        LEFT JOIN EXPENSES AS e
            ON p.project_id = e.project_id
        GROUP BY p.project_id, p.name
        ORDER BY expense_count ASC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All 12 projects have at least one recorded expense. The query returned 0 projects without expenses, confirming that every project has recorded spending activity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Tasks and Expenses by Project

    How many tasks does each project have, and how much has each project spent?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            p.name AS project_name,
            COALESCE(t.task_count, 0) AS total_tasks,
            COALESCE(e.total_expenses, 0) AS total_expenses
        FROM PROJECTS AS p
        LEFT JOIN (
            SELECT
                project_id,
                COUNT(*) AS task_count
            FROM TASKS
            GROUP BY project_id
        ) AS t
            ON p.project_id = t.project_id
        LEFT JOIN (
            SELECT
                project_id,
                SUM(amount) AS total_expenses
            FROM EXPENSES
            GROUP BY project_id
        ) AS e
            ON p.project_id = e.project_id
        ORDER BY total_expenses DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All 12 projects have recorded tasks and expenses. Document Intelligence has the highest total expenses at $28,705.49 across 24 tasks, followed by Customer Churn Prediction with $26,565.33 across 22 tasks. Automated Invoice Processing has 26 tasks, the highest number among the projects shown, with total expenses of $17,379.00.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            COUNT(*) AS total_tasks
        FROM TASKS
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Checking Task Assignments

    Are any tasks assigned to employees who are not working on the same project?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            t.task_id,
            p.name AS project_name,
            t.description AS task,
            t.assigned_person_id,
            pe.first_name || ' ' || pe.last_name AS assigned_person
        FROM TASKS AS t
        JOIN PROJECTS AS p
            ON t.project_id = p.project_id
        LEFT JOIN PEOPLE AS pe
            ON t.assigned_person_id = pe.person_id
        LEFT JOIN PROJECT_ASSIGNMENTS AS pa
            ON t.project_id = pa.project_id
            AND t.assigned_person_id = pa.person_id
        WHERE t.assigned_person_id IS NOT NULL
            AND pa.person_id IS NULL
        ORDER BY t.task_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The query identified 2 task assignment violations. Task 1, Develop predictive model, was assigned to Taylor Rivera on the Retail Demand Forecasting project, while Task 2, Gather business requirements, was assigned to Finley Allen on the Customer Support AI project. Neither employee is officially assigned to the corresponding project. These are the same two intentional violations created in Part A, confirming that the query correctly identifies assignments that break the business rule.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Employee Task Distribution

    Which employees are responsible for the largest number of tasks across all projects?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            pe.person_id,
            pe.first_name || ' ' || pe.last_name AS employee_name,
            COUNT(t.task_id) AS total_tasks,
            COUNT(DISTINCT t.project_id) AS projects_with_tasks
        FROM PEOPLE AS pe
        LEFT JOIN TASKS AS t
            ON pe.person_id = t.assigned_person_id
        GROUP BY pe.person_id, pe.first_name, pe.last_name
        ORDER BY total_tasks DESC, employee_name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The results show that Finley Allen and Jamie Thompson have the highest number of assigned tasks, with 21 each, across 6 and 5 projects respectively. Sage Scott follows with 20 tasks across 4 projects. This suggests that task assignments are not evenly distributed across employees, and managers may want to review how work is allocated. However, the number of tasks alone does not necessarily indicate workload because some tasks may require more time than others.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. How I Know These Numbers Are Right

    I checked two of my answers using separate SQL queries to make sure the results were consistent.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            COUNT(*) AS total_projects,
            COUNT(*) FILTER (
                WHERE project_id IN (
                    SELECT DISTINCT project_id
                    FROM EXPENSES
                )
            ) AS projects_with_expenses,
            COUNT(*) FILTER (
                WHERE project_id NOT IN (
                    SELECT DISTINCT project_id
                    FROM EXPENSES
                )
            ) AS projects_without_expenses
        FROM PROJECTS
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Verification 1 — Projects With No Expenses**

    My original query returned 0 projects without recorded expenses. I checked this another way by counting the projects with and without expense records. The results show 12 total projects, 12 with expenses, and 0 without expenses. Both queries agree.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            SUM(task_count) AS total_tasks_from_projects
        FROM (
            SELECT
                project_id,
                COUNT(*) AS task_count
            FROM TASKS
            GROUP BY project_id
        ) AS project_task_counts
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            COUNT(*) AS total_tasks_directly
        FROM TASKS
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Verification 2 — Total Project Tasks**

    I verified the task counts from Question 6 by adding together the number of tasks in each project. The total was 275 tasks. I then counted all rows directly in the TASKS table and also got 275. Both methods agree with the number of tasks generated in Part A.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Working With the Agent

    While working on Question 1 (Project Expenses vs. Budget), the AI initially suggested a SQL query that used `project_name`, but that column did not exist in my PROJECTS table. When I ran the query, I received an error.

    Instead of accepting the AI's output, I checked the table structure using `DESCRIBE PROJECTS` and found that the correct column was `name`. I then changed the query to use `p.name AS project_name`.

    After making this correction, I ran the query again, and it successfully returned all 12 projects with their budgets, total expenses, and percentages of budget used. I checked the results to confirm that the query was working correctly.

    I later updated Question 1 to use the `project_budget_summary` view created in Part A. The view returned the same results while making the query simpler and allowing me to reuse work from Part A.

    This experience reminded me that AI-generated code is not always accurate and that it is important to understand the database structure and verify the results rather than just relying on the AI.

    **Where to find the correction:** The original correction involved changing `project_name` to `p.name AS project_name`. The final version of Question 1 now uses the `project_budget_summary` view, which I verified returned the same results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 3: Reading It Back
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT COUNT(*) AS joined_rows
        FROM PROJECTS AS p
        JOIN TASKS AS t
            ON p.project_id = t.project_id
        JOIN EXPENSES AS e
            ON p.project_id = e.project_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### My Prediction and Results

    **Selected question:** How many tasks and how much total expense does each project have?

    **My prediction:** I predicted that joining PROJECTS, TASKS, and EXPENSES would produce a few thousand rows before grouping. This is because each task can be matched with multiple expenses within the same project. For example, a project with 5 tasks and 3 expenses would produce 15 rows.

    **Actual result:** The query returned **3,984 rows** before grouping.

    **Did my prediction match?**

    Yes, my prediction was correct. I expected a few thousand rows, and the join produced 3,984. This happened because each task was matched with every expense belonging to the same project, increasing the number of rows.

    **What does one row of the final result mean?**

    Each row in my final results represents one project, showing its total number of tasks and total recorded expenses. For example, Document Intelligence has 24 tasks and $28,705.49 in expenses. This helps managers understand how much work and spending is associated with each project.

    **Important observation:** Because joining tasks and expenses directly creates repeated combinations, I calculated their totals separately before joining them in my final answer. This prevents tasks or expenses from being counted more than once.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Section 4: Going Further
    """)
    return


@app.cell
def _(ask, mo):

    import altair as alt
    import polars as pl

    # Get project budgets and expenses
    project_budget_data = ask("""
        SELECT
            p.name AS project_name,
            p.budget,
            COALESCE(SUM(e.amount), 0) AS total_expenses
        FROM PROJECTS AS p
        LEFT JOIN EXPENSES AS e
            ON p.project_id = e.project_id
        GROUP BY p.project_id, p.name, p.budget
        ORDER BY p.name
    """)

    # Convert amounts and calculate remaining budget
    project_budget_data = project_budget_data.with_columns(
        pl.col("budget").cast(pl.Float64),
        pl.col("total_expenses").cast(pl.Float64)
    ).with_columns(
        (
            pl.col("budget") - pl.col("total_expenses")
        ).alias("remaining_budget")
    )

    # Create the interactive chart
    project_budget_chart = (
        alt.Chart(project_budget_data)
        .transform_fold(
            ["total_expenses", "remaining_budget"],
            as_=["budget_type", "amount"]
        )
        .mark_bar()
        .encode(
            x=alt.X(
                "project_name:N",
                title="Project",
                sort=None
            ),
            y=alt.Y(
                "sum(amount):Q",
                title="Budget Amount ($)",
                stack="zero"
            ),
            color=alt.Color(
                "budget_type:N",
                title="Budget Breakdown"
            ),
            tooltip=[
                alt.Tooltip("project_name:N", title="Project"),
                alt.Tooltip("budget_type:N", title="Category"),
                alt.Tooltip("amount:Q", title="Amount", format="$,.2f")
            ]
        )
        .properties(
            title="Project Budgets: Spending vs. Remaining",
            width=650,
            height=350
        )
    )

    # Display chart
    mo.ui.altair_chart(project_budget_chart)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 4: Going Further

    For my Going Further section, I wanted to explore how I could turn SQL results into something more useful for business managers.

    I created an interactive chart using Altair that compares the total expenses and remaining budgets of all 12 projects. I used SQL to retrieve the data from the PROJECTS and EXPENSES tables and Polars to calculate the remaining budget.

    The chart makes it easier to compare spending across projects and identify which projects have used a larger portion of their budgets. I also added tooltips so users can hover over the bars to see the dollar amounts.

    This helped me understand how database queries can be used not just to retrieve information, but also to communicate business insights visually.

    **Where to find it:** Section 4 of this notebook, directly above this explanation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 5: Time Spent

    Total time spent outside class: 12 hours.
    """)
    return


if __name__ == "__main__":
    app.run()
