import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb

    return duckdb, mo


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (database,)


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

    build_complete = True
    print("Created 5 empty tables successfully.")
    return


if __name__ == "__main__":
    app.run()
