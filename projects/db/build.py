import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl
    import matplotlib.pyplot as plt

    return duckdb, mo, pl, plt


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, database


@app.cell
def _(mo):
    mo.md("""
    # BabsonAI Labs — Database Build

    ## 1. The Tables

    This section defines the five tables, their primary and foreign
    keys, and the rules that the database will enforce.
    """)
    return


@app.cell
def _(database, duckdb):
    # Remove the old database so every build starts fresh.
    if database.exists():
        database.unlink()

    # Create the database and close the connection when finished.
    with duckdb.connect(database) as _con:
        _con.execute("""
            CREATE TABLE people (
                person_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                work_email VARCHAR NOT NULL UNIQUE,
                title VARCHAR NOT NULL,
                start_date DATE NOT NULL,
                manager_id INTEGER REFERENCES people(person_id),

                CHECK (
                    manager_id IS NULL OR manager_id <> person_id
                )
            );

            CREATE TABLE projects (
                project_id INTEGER PRIMARY KEY,
                project_name VARCHAR NOT NULL,
                client_name VARCHAR,
                category VARCHAR NOT NULL
                    CHECK (
                        category IN (
                            'LLM app',
                            'data pipeline',
                            'internal tool'
                        )
                    ),
                budget DECIMAL(12, 2) NOT NULL CHECK (budget > 0),
                start_date DATE NOT NULL,
                status VARCHAR NOT NULL DEFAULT 'planned'
                    CHECK (
                        status IN ('planned', 'active', 'paused', 'done')
                    )
            );

            CREATE TABLE project_memberships (
                person_id INTEGER REFERENCES people(person_id),
                project_id INTEGER REFERENCES projects(project_id),
                project_role VARCHAR NOT NULL,
                weekly_hours DECIMAL(5, 2) NOT NULL
                    CHECK (weekly_hours BETWEEN 1 AND 40),
                joined_date DATE NOT NULL,

                PRIMARY KEY (person_id, project_id)
            );

            CREATE TABLE tasks (
                task_id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL REFERENCES projects(project_id),
                description VARCHAR NOT NULL,
                created_date DATE NOT NULL,
                assigned_person_id INTEGER REFERENCES people(person_id),
                assigned_date DATE,
                due_date DATE NOT NULL,
                completed_date DATE,

                CHECK (
                    completed_date IS NULL
                    OR completed_date >= created_date
                ),

                CHECK (
                    (assigned_person_id IS NULL AND assigned_date IS NULL)
                    OR
                    (assigned_person_id IS NOT NULL AND assigned_date IS NOT NULL)
                ),

                CHECK (
                    assigned_date IS NULL
                    OR assigned_date >= created_date
                )
            );

            CREATE TABLE expenses (
                expense_id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL REFERENCES projects(project_id),
                expense_date DATE NOT NULL,
                amount DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
                category VARCHAR NOT NULL
                    CHECK (
                        category IN (
                            'GPU cloud',
                            'data labeling',
                            'software',
                            'travel'
                        )
                    ),
                note VARCHAR NOT NULL
            );
        """)

        # Locate the folder containing the CSV files.
        _data_folder = database.parent / "data"

        # Read employees in ID order: managers come before their reports.
        _people_rows = _con.execute(
            "SELECT * FROM read_csv(?, header = true) ORDER BY person_id",
            [str(_data_folder / "people.csv")]
        ).fetchall()

        # Insert employees individually because people references itself.
        for _person in _people_rows:
            _con.execute(
                "INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?)",
                _person
            )

        # Load the remaining tables in dependency order.
        for _table in [
            "projects",
            "project_memberships",
            "tasks",
            "expenses"
        ]:
            _csv_path = str(_data_folder / f"{_table}.csv")

            _con.execute(
                f"INSERT INTO {_table} SELECT * FROM read_csv(?, header = true)",
                [_csv_path]
            )

        # Display the number of rows actually loaded into each table.
        for _table in [
            "people",
            "projects",
            "project_memberships",
            "tasks",
            "expenses"
        ]:
            _count = _con.execute(
                f"SELECT COUNT(*) FROM {_table}"
            ).fetchall()[0][0]

            print(f"{_table}: {_count} rows")

    build_complete = True
    print("Database rebuilt and CSV data loaded successfully.")
    return (build_complete,)


@app.cell
def _(mo):
    mo.md("""
    ## 2. The Data

    The data is fictional and is generated by `make_data.py`.
    The script uses random seed 42 so its results can be reproduced.

    The reporting date (`as_of`) is October 31, 2026.
    The data covers November 1, 2025 through October 31, 2026.

    The CSV files contain:
    - 25 people
    - 12 projects
    - 60 project memberships
    - 300 tasks
    - 180 expenses

    Two tasks deliberately break the rule that an assignee must
    belong to the task's project:
    - Task 299 assigns employee 25 to project 1.
    - Task 300 assigns employee 25 to project 1.

    Employee 25 exists but is not a member of project 1.
    Both tasks have valid employment and assignment dates.

    Projects 11 and 12 intentionally have no expenses.
    Employee 25 intentionally has no project memberships.
    There are also 30 unassigned tasks.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 3. A Look at the Data

    I read `expenses.csv` with Polars and counted the expense
    records in each month to inspect their distribution over time.
    """)
    return


@app.cell
def _(mo, pl):
    expenses_csv = pl.read_csv(
        mo.notebook_dir() / "data" / "expenses.csv",
        try_parse_dates=True
    )

    expenses_by_month = (
        expenses_csv
        .with_columns(
            pl.col("expense_date").dt.strftime("%Y-%m").alias("month")
        )
        .group_by("month")
        .agg(
            pl.len().alias("expense_count")
        )
        .sort("month")
    )

    expenses_by_month
    return (expenses_by_month,)


@app.cell
def _(expenses_by_month, plt):
    _fig, _ax = plt.subplots(figsize=(10, 4))

    _bars = _ax.bar(
        expenses_by_month["month"].to_list(),
        expenses_by_month["expense_count"].to_list(),
        color="steelblue"
    )

    _ax.set_title(
        "BabsonAI Labs: Expense Records by Month (Synthetic Data)"
    )
    _ax.set_xlabel("Month")
    _ax.set_ylabel("Number of expense records")

    _ax.tick_params(axis="x", labelrotation=45)
    _ax.set_ylim(0, expenses_by_month["expense_count"].max() + 5)
    _ax.bar_label(_bars, padding=3)

    _fig.tight_layout()

    _fig
    return


@app.cell
def _(mo):
    mo.md("""
    The variation in monthly expense counts looks plausible for
    a simplified startup dataset where projects start, finish,
    or pause at different times, so I kept `make_data.py` unchanged.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 4. Row Counts

    The following table shows the number of rows stored in each
    database table after loading the CSV files.
    """)
    return


@app.cell
def _(ask, build_complete):
    assert build_complete, "Run the database build cell first."

    row_counts = ask("""
        SELECT 'people' AS table_name, COUNT(*) AS row_count
        FROM people

        UNION ALL

        SELECT 'projects', COUNT(*)
        FROM projects

        UNION ALL

        SELECT 'project_memberships', COUNT(*)
        FROM project_memberships

        UNION ALL

        SELECT 'tasks', COUNT(*)
        FROM tasks

        UNION ALL

        SELECT 'expenses', COUNT(*)
        FROM expenses

        ORDER BY table_name;
    """)

    row_counts
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
