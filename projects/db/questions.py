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
    return (q5_no_expenses,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two of the 12 projects have no recorded expenses: Customer Feedback Pilot, which is active, and Employee Onboarding Tool, which is planned.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 6. How many tasks does each project have, and how much has it spent?
    """)
    return


@app.cell
def _(ask):
    q6_project_summary = ask("""
        WITH task_counts AS (
            SELECT project_id, COUNT(*) AS task_count
            FROM tasks
            GROUP BY project_id
        ),
        expense_totals AS (
            SELECT project_id, SUM(amount) AS total_expenses
            FROM expenses
            GROUP BY project_id
        )
        SELECT
            p.project_id,
            p.project_name,
            COALESCE(t.task_count, 0) AS task_count,
            COALESCE(e.total_expenses, 0) AS total_expenses,

            COALESCE(t.task_count, 0) = (
                SELECT COUNT(*)
                FROM tasks
                WHERE project_id = p.project_id
            ) AS task_count_matches,

            COALESCE(e.total_expenses, 0) = (
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE project_id = p.project_id
            ) AS expenses_match

        FROM projects AS p
        LEFT JOIN task_counts AS t ON p.project_id = t.project_id
        LEFT JOIN expense_totals AS e ON p.project_id = e.project_id
        ORDER BY p.project_id
    """)

    q6_project_summary
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Across the 12 projects, I counted 300 tasks and $224,178.85 in total expenses, and both checks matched for every project.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 7. Which tasks are assigned to someone who is not a member of the task’s project?
    """)
    return


@app.cell
def _(ask):
    q7_joins = """
        FROM tasks AS t
        LEFT JOIN people AS p
            ON t.assigned_person_id = p.person_id
        LEFT JOIN project_memberships AS m
            ON t.project_id = m.project_id
            AND t.assigned_person_id = m.person_id
    """

    q7_violations = ask(f"""
        SELECT
            t.task_id,
            t.project_id,
            t.assigned_person_id,
            p.first_name || ' ' || p.last_name AS assigned_to
        {q7_joins}
        WHERE t.assigned_person_id IS NOT NULL
          AND m.person_id IS NULL
        ORDER BY t.task_id
    """)

    q7_violations
    return (q7_violations,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two tasks broke the membership rule: tasks 299 and 300 were both assigned to Omar Said (employee 25) on project 1, even though he was not a member of that project.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 8. Which projects take the longest, on average, to assign a task after it is created?
    """)
    return


@app.cell
def _(ask):
    q8_assignment_time = ask("""
        SELECT
            p.project_name,
            COUNT(*) AS assigned_tasks,
            ROUND(AVG(t.assigned_date - t.created_date), 2) AS avg_days_to_assign
        FROM tasks AS t
        JOIN projects AS p ON t.project_id = p.project_id
        WHERE t.assigned_date IS NOT NULL
        GROUP BY p.project_id, p.project_name
        ORDER BY AVG(t.assigned_date - t.created_date) DESC, p.project_id
    """)

    q8_assignment_time
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Among the 11 projects with assigned tasks, Internal Knowledge Search had the longest average wait at 2.81 days across 26 tasks, followed by Customer Support Copilot at 2.35 days across 26 tasks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. How I Know These Numbers Are Right

    I checked two answers a second way. For Question 5, I compared the IDs
    of projects with no expenses. For Question 7, I compared the IDs of
    tasks assigned to someone outside the project.
    """)
    return


@app.cell
def _(ask, q5_no_expenses):
    _q5_check = ask("""
        SELECT project_id FROM projects
        EXCEPT
        SELECT project_id FROM expenses
        ORDER BY project_id
    """)

    _original = q5_no_expenses["project_id"].to_list()
    _checked = _q5_check["project_id"].to_list()

    print("Question 5 project IDs:", _original)
    print("Independent check:", _checked)
    print("IDs match:", _original == _checked)
    return


@app.cell
def _(ask, q7_violations):
    _q7_check = ask("""
        SELECT t.task_id
        FROM tasks AS t
        WHERE t.assigned_person_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1
              FROM project_memberships AS m
              WHERE m.person_id = t.assigned_person_id
                AND m.project_id = t.project_id
          )
        ORDER BY t.task_id
    """)

    _original = q7_violations["task_id"].to_list()
    _checked = _q7_check["task_id"].to_list()

    print("Question 7 task IDs:", _original)
    print("Independent check:", _checked)
    print("IDs match:", _original == _checked)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Working With the Agent

    For Question 4, the agent’s first query showed that GPU cloud was the
    only expense category above average. I wanted to understand where the
    $11,874.30 average came from, so I added a cell called
    `q4_category_totals` to show the spending for all four categories.

    The four totals added up to $47,497.19. Dividing by four gave me
    $11,874.30, rounded to the nearest cent. With all four amounts visible,
    I could see that only GPU cloud, at $36,733.93, was above that average.

    [See my Question 4 commit.](https://github.com/theshubhamshirke-commits/oim7510/commit/7de4ddec8cb69515cbecc97599182fc55587985d)
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
