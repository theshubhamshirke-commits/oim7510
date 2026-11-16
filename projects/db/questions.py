import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    from datetime import date

    return date, duckdb, mo


@app.cell
def _(date, duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"
    as_of = date(2026, 10, 31)

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return as_of, ask


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 1. How much of its budget has each project spent?
    """)
    return


@app.cell
def _(ask):
    q1_budget = ask("""
        SELECT
            project_name,
            budget,
            total_expenses,
            remaining_budget,
            ROUND(100.0 * total_expenses / budget, 2) AS percent_spent
        FROM project_budget_summary
        ORDER BY total_expenses / budget DESC, project_id
    """)

    q1_budget
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Six of the 12 projects spent more than their budgets, and Customer Support Copilot spent the largest share at $42,586.60, or 354.89% of its $12,000 budget.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2. Which tasks were overdue and still unfinished, which projects did they belong to, and who was assigned to them?
    """)
    return


@app.cell
def _(as_of, ask):
    q2_overdue = ask(f"""
        SELECT
            t.task_id,
            t.description,
            p.project_name,
            COALESCE(e.first_name || ' ' || e.last_name, 'Unassigned') AS assigned_to,
            t.due_date
        FROM tasks AS t
        JOIN projects AS p
            ON t.project_id = p.project_id
        LEFT JOIN people AS e
            ON t.assigned_person_id = e.person_id
        WHERE t.due_date < DATE '{as_of}'
          AND (t.completed_date IS NULL OR t.completed_date > DATE '{as_of}')
        ORDER BY t.due_date, t.task_id
    """)

    q2_overdue
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As of October 31, 2026, 106 tasks were past their due date and still unfinished, including 82 assigned to an employee and 24 that were unassigned.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3. How many hours per week has each person committed to active projects, and who is above 40 hours?
    """)
    return


@app.cell
def _(ask):
    q3_hours = ask("""
        WITH active_hours AS (
            SELECT
                m.person_id,
                SUM(m.weekly_hours) AS weekly_hours
            FROM project_memberships AS m
            JOIN projects AS p
                ON m.project_id = p.project_id
            WHERE p.status = 'active'
            GROUP BY m.person_id
        )
        SELECT
            e.person_id,
            e.first_name || ' ' || e.last_name AS employee_name,
            COALESCE(a.weekly_hours, 0) AS active_weekly_hours,
            COALESCE(a.weekly_hours, 0) > 40 AS above_40_hours
        FROM people AS e
        LEFT JOIN active_hours AS a
            ON e.person_id = a.person_id
        ORDER BY active_weekly_hours DESC, e.person_id
    """)

    q3_hours
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Across the nine active projects, two of the 25 employees have committed more than 40 hours per week: Rohan Patel at 100 hours and Noah Kim at 80 hours.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 4. Which expense categories had above-average total spending in the last 90 days?
    """)
    return


@app.cell
def _(as_of, ask):
    q4_expenses = ask(f"""
        WITH category_totals AS (
            SELECT
                category,
                SUM(amount) AS total_spent
            FROM expenses
            WHERE expense_date BETWEEN DATE '{as_of}' - 89 AND DATE '{as_of}'
            GROUP BY category
        )
        SELECT
            category,
            total_spent
        FROM category_totals
        WHERE total_spent > (SELECT AVG(total_spent) FROM category_totals)
        ORDER BY total_spent DESC
    """)

    q4_expenses
    return


@app.cell
def _(as_of, ask):
    q4_category_totals = ask(f"""
        SELECT
            category,
            SUM(amount) AS total_spent
        FROM expenses
        WHERE expense_date BETWEEN DATE '{as_of}' - 89 AND DATE '{as_of}'
        GROUP BY category
        ORDER BY total_spent DESC
    """)

    q4_category_totals
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From August 3 through October 31, 2026, the four categories totaled $47,497.19, giving an average of $11,874.30 per category ($47,497.19/4); only GPU cloud exceeded that average, with $36,733.93 in expenses.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 5. Which projects have no recorded expenses?
    """)
    return


@app.cell
def _(ask):
    q5_no_expenses = ask("""
        SELECT
            p.project_id,
            p.project_name,
            p.status
        FROM projects AS p
        LEFT JOIN expenses AS e
            ON p.project_id = e.project_id
        WHERE e.expense_id IS NULL
        ORDER BY p.project_id
    """)

    q5_no_expenses
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two of the 12 projects have no recorded expenses: Customer Feedback Pilot, which is active, and Employee Onboarding Tool, which is planned.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Reading It Back


    I am picking Q7 from the list: “Every task checked against the rule that its assignee works on its project, and a list of any that break it.”

    *I chose Question 7 because I want to check whether each assigned task goes to someone who works on that project. I expect the joins to return 300 rows before I filter or group the results. I start with 300 tasks. For each task, I look up the assigned employee and check whether they belong to that project. Each task can match at most one employee and one membership for that employee on that project. Since I’m using LEFT JOIN, I keep the task even if either match is missing. That leaves me with one row per task.*
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
