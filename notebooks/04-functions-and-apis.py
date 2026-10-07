# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "requests",
# ]
# ///
"""Functions and APIs.
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
    # Functions and APIs

    This session moves between two notebooks. It opens with section 4 of notebook 3, `03-collections-and-apis.py`, then comes here for section 1, on functions. After the break it goes back for section 5 of notebook 3, the first requests to a server, and returns here for the rest: reading an API built for this course, and sending data to it.

    | | |
    |---|---|
    | ✏️ | Your turn. Add cells with the **+** button |
    | 🚀 | This week's work |

    For a written answer, add a cell under the question, open the cell's **⋯** menu and choose **Convert to Markdown**.

    Every ✏️ is part of this week's work. Those marked **Advanced** are optional; try them once the rest is done.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Work with your agent the same way as in notebook 3.** Try it yourself first, or write the steps in words. Then ask your agent, ask it to explain any line you could not have written, and ask which concepts its answer used.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. Functions

    Notebooks 2 and 3 each computed what the portfolio costs, and each time the loop was written out again. A **function** gives that work a name, so it is written once and used on any portfolio. You have called functions since the first day: `len(...)`, `round(...)`, `print(...)`. Each takes something in and gives something back, the way `SUM(A1:A6)` does in a spreadsheet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Start with the smallest one. `def` starts a function, and `add_tax` is its name, a verb and a noun for what it does. `amount` in brackets is its **parameter**, what it takes in, and `return` is what it gives back. Defining it runs nothing; it runs each time it is called. Massachusetts sales tax is 6.25%, so the function multiplies by 1.0625.
    """)
    return


@app.function
def add_tax(amount):
    return round(amount * 1.0625, 2)


@app.cell
def _():
    add_tax(100)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If the tax rate changes, you edit the one line inside `add_tax`, and every call uses the new rate.
    """)
    return


@app.cell
def _():
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]
    holdings
    return (holdings,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Names inside a function belong to that function.** `symbol`, `shares` and `cost_so_far` exist only while it runs, so they need no underscore, and two functions can each use `price` without colliding.
    """)
    return


@app.function
def compute_cost(portfolio):
    cost_so_far = 0
    for symbol, shares, price in portfolio:
        cost_so_far = cost_so_far + shares * price
    return round(cost_so_far, 2)


@app.cell
def _(holdings):
    compute_cost(holdings)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A second client holds two funds and one stock. The same function answers for them, with no new loop.
    """)
    return


@app.cell
def _():
    retirement_holdings = [
        ("VTI", 120, 228.40),
        ("BND", 300, 72.15),
        ("AAPL", 40, 173.93),
    ]
    retirement_holdings
    return (retirement_holdings,)


@app.cell
def _(retirement_holdings):
    compute_cost(retirement_holdings)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Why programs are built from functions:**

    - **A change happens in one place.** Add a trading fee inside `compute_cost` and every portfolio's cost follows.
    - **The name says what the work is for.** `compute_cost(retirement_holdings)` reads as a sentence; a loop has to be read line by line.
    - **Everything it needs comes in through the brackets.** So you can test it on a portfolio whose answer you already know, such as notebook 3's $116,302.70.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ A · Functions of your own

    1. Add a cell that defines `count_shares(portfolio)`. It returns the total number of shares in a portfolio. Call it on both portfolios. *Check yourself: `600` and `460`.*
    2. Add a cell that defines `find_largest(portfolio)`. It returns the ticker and the cost of the holding that cost the most, as a tuple. Call it on both portfolios. *Check yourself: `('TSLA', 38355.0)` and `('VTI', 27408.0)`.*

    **Going further.** Add a second parameter, `n`, and return the `n` largest holdings, largest first.
    """)
    return


@app.function
#1

def count_shares(portfolio):
    total_shares = 0
    for symbol, shares, price in portfolio:
        total_shares = total_shares + shares
    return total_shares


@app.cell
def _(holdings):
    count_shares(holdings)
    return


@app.cell
def _(retirement_holdings):
    count_shares(retirement_holdings)
    return


@app.function
def find_largest(portfolio, n):
    holdings_cost = []
    for symbol, shares, price in portfolio:
        holdings_cost.append((symbol, shares * price))

    largest = []
    for i in range(n):
        best_symbol = holdings_cost[0][0]
        best_cost = holdings_cost[0][1]
        for symbol, cost in holdings_cost:
            if cost > best_cost:
                best_symbol = symbol
                best_cost = cost
        largest.append((best_symbol, best_cost))
        holdings_cost.remove((best_symbol, best_cost))
    return largest


@app.cell
def _(holdings):
    find_largest(holdings, 3)

    return


@app.cell
def _(retirement_holdings):
    find_largest(retirement_holdings, 2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ B · Without `return`

    Copy `count_shares` into a new cell under a new name, and put `print(...)` where the `return` was. Call it and keep the result in a name. In a markdown cell under it, answer: what does that name hold, and what could the next cell do with it?
    """)
    return


@app.function
def count_shares_print(portfolio):
    total_shares = 0
    for symbol, shares, price in portfolio:
        total_shares = total_shares + shares
    print(total_shares)


@app.cell
def _(holdings):
    result = count_shares_print(holdings)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. Calling an API

    Calling an **API** is like calling a function someone else wrote, running on their computer. You call it with a web address, their server runs its code, and the result comes back to you.

    | | Calling a function you wrote | Calling an API |
    |---|---|---|
    | **You call it with** | `get_towns("Norfolk")` | `oim.zhili.dev/ma/towns?county=Norfolk` |
    | **What goes in** | parameters in brackets | parameters after `?` |
    | **What comes back** | the `return` value | a reply, usually JSON |
    | **When it goes wrong** | an error in your notebook | a status code and a message |
    | **Where it runs** | your laptop | somebody else's server |

    You cannot see the code behind an API, so its documentation is how you learn its parameters and what it returns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The course runs its own API at `oim.zhili.dev`. Its Massachusetts endpoints come from the state's [Division of Local Services](https://www.mass.gov/info-details/division-of-local-services-municipal-databank): every city and town, its population and income, and its property tax rates and bills. The documentation is at [oim.zhili.dev/docs](https://oim.zhili.dev/docs), and the API also lists its own endpoints. **Before any code**, open [oim.zhili.dev/mass](https://oim.zhili.dev/mass) and [oim.zhili.dev/ma/towns?county=Norfolk](https://oim.zhili.dev/ma/towns?county=Norfolk) in your browser and read what comes back. `requests` is already in your project from notebook 3.
    """)
    return


@app.cell
def _():
    import requests

    return (requests,)


@app.cell
def _(requests):
    ma_endpoints = requests.get("https://oim.zhili.dev/ma", timeout=10).json()
    ma_endpoints
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `/ma/towns` takes a `county`. Pass parameters as a dictionary with `params=`, and `requests` builds the address. `.url` shows the address it built.
    """)
    return


@app.cell
def _(requests):
    norfolk_reply = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"county": "Norfolk"},
        timeout=10,
    )
    norfolk_reply.status_code, norfolk_reply.url
    return (norfolk_reply,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Why a dictionary.** A value with a space in it has to be encoded before it can go in an address, and `params=` does that for you. Ask for `{"name": "West Newbury"}` and `.url` ends in `name=West+Newbury`.

    The reply is a dictionary with two keys. `pagination` states how much there is.
    """)
    return


@app.cell
def _(norfolk_reply):
    norfolk_page = norfolk_reply.json()
    norfolk_page["pagination"]
    return (norfolk_page,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `items` is a table: a list of records, one per town, the same shape as the orders in notebook 2.
    """)
    return


@app.cell
def _(norfolk_page):
    norfolk_page["items"][0]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Wrap the request in a function and the endpoint becomes a Python function. `get_towns` takes a county and returns its towns, and the cell that calls it never sees the address.
    """)
    return


@app.cell
def _(requests):
    def get_towns(county):
        towns_reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county},
            timeout=10,
        )
        return towns_reply.json()["items"]

    return (get_towns,)


@app.cell
def _(get_towns):
    get_towns("Suffolk")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ C · Read the documentation

    Open [oim.zhili.dev/docs](https://oim.zhili.dev/docs) and find `/ma/towns`. Use its parameters to ask for the five Norfolk towns with the highest income per person, highest first. Let the server do the sorting.

    *Check yourself: Dover, Wellesley, Cohasset, Needham, Westwood.*
    """)
    return


@app.cell
def _(false):
    {
      "items": [
        {
          "dor_code": "018",
          "name": "Avon",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 5.1,
          "founded_year": 1888,
          "population": 4801,
          "income_per_capita_dollars": 44742,
          "equalized_value_dollars": 1239903800,
          "equalized_value_per_capita_dollars": 258259,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 572492,
          "average_single_family_bill_dollars": 7643,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "025",
          "name": "Bellingham",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 16.4,
          "founded_year": 1719,
          "population": 17998,
          "income_per_capita_dollars": 45801,
          "equalized_value_dollars": 4076393600,
          "equalized_value_per_capita_dollars": 226491,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 490174,
          "average_single_family_bill_dollars": 6073,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "040",
          "name": "Braintree",
          "county": "Norfolk",
          "type": "city",
          "area_square_miles": 16.5,
          "founded_year": 1640,
          "population": 39134,
          "income_per_capita_dollars": 52904,
          "equalized_value_dollars": 10340377900,
          "equalized_value_per_capita_dollars": 264230,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 726203,
          "average_single_family_bill_dollars": 7306,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "046",
          "name": "Brookline",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 6.8,
          "founded_year": 1705,
          "population": 63925,
          "income_per_capita_dollars": 100201,
          "equalized_value_dollars": 33768586100,
          "equalized_value_per_capita_dollars": 528253,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 2562186,
          "average_single_family_bill_dollars": 26237,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "050",
          "name": "Canton",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 18.3,
          "founded_year": 1797,
          "population": 25163,
          "income_per_capita_dollars": 73374,
          "equalized_value_dollars": 8267137500,
          "equalized_value_per_capita_dollars": 328543,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 868560,
          "average_single_family_bill_dollars": 8468,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "065",
          "name": "Cohasset",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 9.9,
          "founded_year": 1770,
          "population": 8532,
          "income_per_capita_dollars": 154676,
          "equalized_value_dollars": 4232219500,
          "equalized_value_per_capita_dollars": 496041,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 1481437,
          "average_single_family_bill_dollars": 16814,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "073",
          "name": "Dedham",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 10.2,
          "founded_year": 1636,
          "population": 25485,
          "income_per_capita_dollars": 72590,
          "equalized_value_dollars": 7957982700,
          "equalized_value_per_capita_dollars": 312261,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 810871,
          "average_single_family_bill_dollars": 9974,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "078",
          "name": "Dover",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 15.2,
          "founded_year": 1784,
          "population": 6057,
          "income_per_capita_dollars": 264727,
          "equalized_value_dollars": 3605308900,
          "equalized_value_per_capita_dollars": 595230,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 1705816,
          "average_single_family_bill_dollars": 19088,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "099",
          "name": "Foxborough",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 21.5,
          "founded_year": 1778,
          "population": 18791,
          "income_per_capita_dollars": 64808,
          "equalized_value_dollars": 4537534100,
          "equalized_value_per_capita_dollars": 241474,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 693572,
          "average_single_family_bill_dollars": 9016,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "101",
          "name": "Franklin",
          "county": "Norfolk",
          "type": "city",
          "area_square_miles": 26.8,
          "founded_year": 1778,
          "population": 33742,
          "income_per_capita_dollars": 64589,
          "equalized_value_dollars": 8538330900,
          "equalized_value_per_capita_dollars": 253048,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 731396,
          "average_single_family_bill_dollars": 8353,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "133",
          "name": "Holbrook",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 7,
          "founded_year": 1872,
          "population": 11475,
          "income_per_capita_dollars": 40811,
          "equalized_value_dollars": 2100152500,
          "equalized_value_per_capita_dollars": 183020,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 534082,
          "average_single_family_bill_dollars": 6468,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "175",
          "name": "Medfield",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 14.9,
          "founded_year": 1651,
          "population": 13334,
          "income_per_capita_dollars": 111805,
          "equalized_value_dollars": 4104880400,
          "equalized_value_per_capita_dollars": 307851,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 1028374,
          "average_single_family_bill_dollars": 13904,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "177",
          "name": "Medway",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 13,
          "founded_year": 1713,
          "population": 13836,
          "income_per_capita_dollars": 69807,
          "equalized_value_dollars": 3638444900,
          "equalized_value_per_capita_dollars": 262969,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 698980,
          "average_single_family_bill_dollars": 9786,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "187",
          "name": "Millis",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 14.3,
          "founded_year": 1885,
          "population": 9338,
          "income_per_capita_dollars": 61956,
          "equalized_value_dollars": 2230073300,
          "equalized_value_per_capita_dollars": 238817,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 668161,
          "average_single_family_bill_dollars": 10230,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "189",
          "name": "Milton",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 13,
          "founded_year": 1662,
          "population": 28811,
          "income_per_capita_dollars": 107276,
          "equalized_value_dollars": 9321873200,
          "equalized_value_per_capita_dollars": 323553,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 1081191,
          "average_single_family_bill_dollars": 12769,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "199",
          "name": "Needham",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 12.8,
          "founded_year": 1711,
          "population": 32931,
          "income_per_capita_dollars": 139002,
          "equalized_value_dollars": 14275936100,
          "equalized_value_per_capita_dollars": 433511,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 1541061,
          "average_single_family_bill_dollars": 16690,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "208",
          "name": "Norfolk",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 15,
          "founded_year": 1870,
          "population": 11962,
          "income_per_capita_dollars": 73622,
          "equalized_value_dollars": 2848134600,
          "equalized_value_per_capita_dollars": 238099,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 788035,
          "average_single_family_bill_dollars": 11718,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "220",
          "name": "Norwood",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 10.6,
          "founded_year": 1872,
          "population": 31764,
          "income_per_capita_dollars": 58355,
          "equalized_value_dollars": 8244418000,
          "equalized_value_per_capita_dollars": 259552,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 719477,
          "average_single_family_bill_dollars": 7065,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "238",
          "name": "Plainville",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 10.6,
          "founded_year": 1905,
          "population": 10067,
          "income_per_capita_dollars": 51750,
          "equalized_value_dollars": 2438980600,
          "equalized_value_per_capita_dollars": 242275,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 616329,
          "average_single_family_bill_dollars": 6958,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "243",
          "name": "Quincy",
          "county": "Norfolk",
          "type": "city",
          "area_square_miles": 16.9,
          "founded_year": 1625,
          "population": 103434,
          "income_per_capita_dollars": 48421,
          "equalized_value_dollars": 24356530000,
          "equalized_value_per_capita_dollars": 235479,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 700324,
          "average_single_family_bill_dollars": 8250,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "244",
          "name": "Randolph",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 10.4,
          "founded_year": 1793,
          "population": 35114,
          "income_per_capita_dollars": 34979,
          "equalized_value_dollars": 6232525200,
          "equalized_value_per_capita_dollars": 177494,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 546462,
          "average_single_family_bill_dollars": 6328,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "266",
          "name": "Sharon",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 24,
          "founded_year": 1765,
          "population": 18762,
          "income_per_capita_dollars": 85745,
          "equalized_value_dollars": 5308409500,
          "equalized_value_per_capita_dollars": 282934,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 836893,
          "average_single_family_bill_dollars": 14353,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "285",
          "name": "Stoughton",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 16.8,
          "founded_year": 1726,
          "population": 29457,
          "income_per_capita_dollars": 42818,
          "equalized_value_dollars": 6283557300,
          "equalized_value_per_capita_dollars": 213313,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 606054,
          "average_single_family_bill_dollars": 7157,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "307",
          "name": "Walpole",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 22,
          "founded_year": 1724,
          "population": 26391,
          "income_per_capita_dollars": 73347,
          "equalized_value_dollars": 7392062800,
          "equalized_value_per_capita_dollars": 280098,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 831005,
          "average_single_family_bill_dollars": 10346,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "317",
          "name": "Wellesley",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 10.5,
          "founded_year": 1881,
          "population": 31242,
          "income_per_capita_dollars": 212430,
          "equalized_value_dollars": 18013343600,
          "equalized_value_per_capita_dollars": 576575,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 2020758,
          "average_single_family_bill_dollars": 20551,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "335",
          "name": "Westwood",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 11,
          "founded_year": 1897,
          "population": 16533,
          "income_per_capita_dollars": 127497,
          "equalized_value_dollars": 7283384500,
          "equalized_value_per_capita_dollars": 440536,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 1250705,
          "average_single_family_bill_dollars": 16097,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "336",
          "name": "Weymouth",
          "county": "Norfolk",
          "type": "city",
          "area_square_miles": 17.7,
          "founded_year": 1635,
          "population": 60159,
          "income_per_capita_dollars": 45212,
          "equalized_value_dollars": 13414292900,
          "equalized_value_per_capita_dollars": 222981,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 613486,
          "average_single_family_bill_dollars": 6208,
          "finances_fiscal_year": 2026
        },
        {
          "dor_code": "350",
          "name": "Wrentham",
          "county": "Norfolk",
          "type": "town",
          "area_square_miles": 19.8,
          "founded_year": 1673,
          "population": 12516,
          "income_per_capita_dollars": 73106,
          "equalized_value_dollars": 3513910100,
          "equalized_value_per_capita_dollars": 280753,
          "data_fiscal_year": 2027,
          "average_single_family_value_dollars": 711823,
          "average_single_family_bill_dollars": 8307,
          "finances_fiscal_year": 2026
        }
      ],
      "pagination": {
        "page": 1,
        "per_page": 50,
        "total": 28,
        "pages": 1,
        "has_next": false,
        "has_prev": false
      }
    }
    return


@app.cell
def _(requests):
    norfolk_reeply = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"county": "Norfolk", "per_page": 50},
        timeout=10,
    )
    norfolk_towns = norfolk_reeply.json()["items"]
    return (norfolk_towns,)


@app.cell
def _(norfolk_towns):
    def get_income(town):
        return town["income_per_capita_dollars"]

    top_income_towns = sorted(norfolk_towns, key=get_income, reverse=True)[:5]
    for town in top_income_towns:
        print(town["name"], town["income_per_capita_dollars"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ D · From a Name to a History

    1. Find Wellesley's `dor_code` with the `name` parameter of `/ma/towns`.
    2. Use it to ask `/ma/towns/{dor_code}/history` for fiscal year 2026.
    3. Check the bill a second way: the average value times the tax rate, divided by 1,000.

    *Check yourself: `317`. Then $2,020,758 × 10.17 / 1,000 = $20,551.11, and the reply's bill is $20,551.*

    **Going further.** Write `town_history(name)`, which takes a town's name, makes both requests, and returns the history.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. More Than One Page

    Leave `county` out and `/ma/towns` has every town in the state to give you. Read how many it sends.
    """)
    return


@app.cell
def _(requests):
    state_first_page = requests.get("https://oim.zhili.dev/ma/towns", timeout=10).json()
    len(state_first_page["items"]), state_first_page["pagination"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Why a server sends pages.** It answers many people at once, so it limits what one request can cost it. The course shop has more than 15,000 orders behind `/shop/orders`, with a few more every day, and one reply holding all of them would be slow to send and slow to read. You can ask for bigger pages up to a limit, and past it the server refuses.
    """)
    return


@app.cell
def _(requests):
    too_big_reply = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"per_page": 500},
        timeout=10,
    )
    too_big_reply.status_code, too_big_reply.json()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **422** means the request had the right shape and a value the server will not accept. Its reply names the limit.

    So reading everything takes one request per page. `get_page` asks for one page. `per_page=100` in its brackets is a **default**: `get_page(2)` uses 100, and `get_page(2, 20)` uses 20. The server's parameters have defaults too, which is why leaving out `page` gave page 1.
    """)
    return


@app.cell
def _(requests):
    def get_page(page, per_page=100):
        page_reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"page": page, "per_page": per_page},
            timeout=10,
        )
        return page_reply.json()

    return (get_page,)


@app.cell
def _(get_page):
    get_page(1)["pagination"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ E · Every town

    Write `get_all_towns()`. It reads page 1, takes `pages` from its `pagination`, reads the pages after it with `range(2, pages + 1)`, and returns one list of every town.

    *Check yourself: 351 towns, the same number as `pagination["total"]`. The first is Abington and the last is Yarmouth.*

    The count you collected against the total the server reports is a check you can run on any API that sends pages.

    **Going further.** Which town has the highest average single-family tax bill in the state, and which the lowest?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. Sending Data

    Every request so far has been a **GET**, which asks for data and changes nothing. A **POST** sends data for the server to keep. Submitting a form on a website is a POST.

    The course API has a board, [oim.zhili.dev/live](https://oim.zhili.dev/live), with one line per student. A POST to `/message` writes yours.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The server has to know who sent it.** A request can carry **headers**, lines that travel beside the address. Here the header `x-token` holds your GitHub username, and the board shows your first name. Your username is public, so it can sit in a cell. A real API's key goes in a header the same way, but a key is a secret and never goes in a cell: [Mini Project 2](/assignments/mini-project-2/) says where to keep one.

    **The message goes in the body.** `json=` puts it there, which is where a POST carries its data. `params=` puts values in the address, which is for asking.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ F · Write on the board

    1. Look up a town you know with the `name` parameter of `/ma/towns`. Keep its name as `town_name` and its average single-family bill as `town_bill`.
    2. Add a cell with the code below, put your GitHub username in place of the brackets, and run it.

       ```python
       board_reply = requests.post(
           "https://oim.zhili.dev/message",
           headers={"x-token": "<your-github-username>"},
           json={"message": f"{town_name}: ${town_bill:,}"},
           timeout=10,
       )
       board_reply.status_code, board_reply.json()
       ```

       *Check yourself: **201**, which means the server created something, and your town on the board.*

    3. Delete the `headers=` line and run it again. In a markdown cell under it, answer: what did the server answer, and why does it need to know who sent a message?

    **Going further.** Post something more useful than one town's bill: choose a question somebody would ask, answer it from live data, and post the answer, in 140 characters or fewer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Advanced · G · Take it down.** `requests.delete` on the same address, with the same header, removes your line. Run it twice and compare the two replies.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🚀 This Week's Work

    1. **Notebook 3, sections 4 to 6**, if you have not finished them
    2. **Everything above in this notebook** that is not marked **Advanced**, in your repository under `notebooks/`
    3. **[Mini Project 1](/assignments/mini-project-1/)**, due Sunday 10/11
    4. **[Mini Project 2](/assignments/mini-project-2/)**, due Sunday 10/25
    5. **Commit as you go**, with messages that state what changed, and push before you stop
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What you can do now:**

    - [ ] I can write a function with `def`, with parameters, a default and a `return`
    - [ ] I can state why a piece of work belongs in a function
    - [ ] I can find an endpoint's parameters in an API's documentation and pass them with `params=`
    - [ ] I can read every page of an API that sends pages, and check the count against the total
    - [ ] I can send data to an API with a POST and a header
    """)
    return


if __name__ == "__main__":
    app.run()
