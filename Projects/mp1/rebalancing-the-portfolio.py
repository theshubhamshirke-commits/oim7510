# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As the title says, Rebalancing the portfolio, this particular tool will help a financial advisor/ people handing their own portfolio to balance different aspects of their portfolio ensuring that the overall allocation aligns with the desired risk tolerance and investment goals. It also calculates how many shares of each stock to buy or sell and how much cash will remain after those trades.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So, for this particular tool, I would carry the following steps:

    1. Start by calculating the current value of each stock. For ex: AAPL: 100 (shares) * 173.93 (current price). So, for AAPL, the current value = 100 *173.93 = $17,393.
    2. Step 1 will repeated for other stocks as well.
    3. After the current value of all 6 stocks in known, I will add them all up plus add the $5000 cash available, which wil give me the total portfolio value (TPV).
    4. Now, once the  TPV is known, I will again calculate the percentage allocation of each stock in the portfolio by dividing the current value of each stock by the TPV, and then multiplying by 100. For ex: AAPL allocation % = (17,393 / TPV) * 100.
    5. This will be repeated for all 6 stocks, plus the cash position, so that the sum of all allocation percentages equals 100%.
    6. Once I have the percentage allocation of each stock, I will compare it against the target allocation to see which stocks are overweight or underweight relative to the desired portfolio mix.
    7. For each stock, I will multiply the total portfolio value by its target allocation to calculate the dollar amount that should be invested in it.
    8. I will divide this target dollar amount by the stock’s price and round down to a whole number, since the brokerage only allows whole shares.
    9. I will subtract the current number of shares from the target number of shares. A positive result means buy, a negative result means sell, and zero means hold.
    10. I will calculate the remaining cash by adding the money received from selling shares and subtracting the money spent on buying shares.
    11. I will calculate each stock’s value and percentage allocation after the trades, including the remaining cash in the total portfolio value.
    12. I will compare the final allocations with the targets in percentage points and decide whether the differences are small enough.
    13. Finally, I will check that the remaining cash is not negative and that the total value of the stocks plus cash is the same before and after rebalancing, since there are no trading fees.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What does your loop carry from one step to the next, the way a running total carries its sum?

    When calculating the total portfolio value (TPV), my loop carries a running total and adds each stock’s value to it. When calculating the trades, it carries the remaining cash balance, adding money from sales and subtracting money spent on purchases.




    Which check will you use in section 6, and which two numbers should agree?

    I will independently calculate the value of the final stock holdings and add the remaining cash. This total should equal the original portfolio value, including the starting cash, because the trades happen at the same prices with no fees.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    # Your inputs.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
