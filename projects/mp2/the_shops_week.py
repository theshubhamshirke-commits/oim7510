import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #THE SHOP'S WEEK
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *SECTION 1: The Question:*

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Answer*

    Northwind Traders’ operations manager needs a report showing how the business performed over the last seven days, including today. The report will show the number of orders, total revenue excluding freight, revenue by destination country, the five products with the most units sold, and orders from this period that have not shipped yet. This will help the manager understand sales activity and identify orders that need shipping follow-up.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *SECTION 2: MY PLAN BEFORE AI*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. I will keep the number of days as an input at the top of the notebook, starting with seven days.

    2. I will calculate the reporting period so that it includes today and the previous six days.

    3. I will request the orders placed during this period from the shop API.

    4. I will check the pagination information and request any remaining pages so that I collect every order in the period.

    5. For each order, I will request its details to get the products and quantities ordered.

    6. I will count the orders and add their order totals to calculate total revenue, excluding freight.

    7. I will use a dictionary to group order revenue by destination country.

    8. I will use another dictionary to add the quantities sold for each product, then rank the products and select the top five.

    9. I will identify orders that have not shipped by checking whether their shipped_date is empty.

    10. I will print the results in clearly labeled tables and generate a sentence summarizing the findings for the manager.

    11. I will save the fetched records in a JSON file inside projects/mp2/data/ and commit that file.

    12. I will check at least one result independently before accepting the report.

    13. For Going Further, I will group order revenue by date and create a chart showing daily revenue during the reporting period, including days with no orders. This will help the manager see which days generated the most revenue.

    14. I will verify that the daily revenue amounts add up to the total revenue in the main report. I will then describe what the chart shows, including the day or days with the highest revenue, in Section 9.
    """)
    return


if __name__ == "__main__":
    app.run()
