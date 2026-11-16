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

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3. Reading It Back


    I am picking Q7 from the list: “Every task checked against the rule that its assignee works on its project, and a list of any that break it.”

    *I chose Question 7 because I want to check whether each assigned task goes to someone who works on that project. I expect the joins to return 300 rows before I filter or group the results. I start with 300 tasks. For each task, I look up the assigned employee and check whether they belong to that project. Each task can match at most one employee and one membership for that employee on that project. Since I’m using LEFT JOIN, I keep the task even if either match is missing. That leaves me with one row per task.*
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
