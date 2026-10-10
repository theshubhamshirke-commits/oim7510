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
    # # Each entry contains: stock ticker, shares owned, price per share.
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]

    # Cash currently available in the account.
    cash = 5000.00

    # Desired allocation for each stock.
    # 0.20 means 20%, and 0.15 means 15%.
    target_weights = {
        "AAPL": 0.20,
        "MSFT": 0.20,
        "GOOG": 0.15,
        "AMZN": 0.15,
        "NVDA": 0.15,
        "TSLA": 0.15,
    }
    return cash, holdings, target_weights


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(cash, holdings, target_weights):
    # STEP 1: Calculate the total portfolio value.

    total_portfolio_value = cash

    for ticker, shares, price in holdings:
        current_value = shares * price
        total_portfolio_value = total_portfolio_value + current_value

    total_portfolio_value = round(total_portfolio_value, 2)

    print(f"Total portfolio value: ${total_portfolio_value:,.2f}")
    print()


    # STEP 2: Compare current allocations with target allocations.

    for ticker, shares, price in holdings:
        current_stock_value = shares * price
        current_percentage = (current_stock_value / total_portfolio_value) * 100
        target_percentage = target_weights[ticker] * 100

        print(
            f"{ticker}: Current = {current_percentage:.2f}%, "
            f"Target = {target_percentage:.2f}%"
        )

    cash_percentage = (cash / total_portfolio_value) * 100

    print(f"Cash allocation: {cash_percentage:.2f}%")
    print()


    # STEP 3: Calculate trades and remaining cash.

    remaining_cash = cash
    rebalance_results = []

    for ticker, shares, price in holdings:
        # Calculate the target dollar amount for this stock.
        target_value = total_portfolio_value * target_weights[ticker]

        # Divide by the price and round down to whole shares.
        target_shares = int(target_value // price)

        # Positive means buy; negative means sell; zero means hold.
        shares_to_trade = target_shares - shares

        # Subtract purchases from cash and add sale proceeds.
        trade_value = round(shares_to_trade * price, 2)
        remaining_cash = round(remaining_cash - trade_value, 2)

        # Calculate the stock's value after rebalancing.
        value_after = round(target_shares * price, 2)

        # Calculate its final allocation, including cash in the total.
        percentage_after = (value_after / total_portfolio_value) * 100

        # Calculate the difference from the target in percentage points.
        target_percentage = target_weights[ticker] * 100
        gap_percentage_points = percentage_after - target_percentage

        # Store the results for the table in Section 5.
        rebalance_results.append(
            (
                ticker,
                shares,
                target_shares,
                shares_to_trade,
                value_after,
                percentage_after,
                gap_percentage_points,
            )
        )

    #print(f"Cash remaining after all trades: ${remaining_cash:,.2f}")
    return rebalance_results, remaining_cash, total_portfolio_value


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(rebalance_results, remaining_cash, total_portfolio_value):
    # Check that the remaining cash is not negative.
    if remaining_cash < 0:
        raise ValueError("The trades would leave a negative cash balance.")

    # Print the table headings.
    print(
        f"{'Ticker':<8}"
        f"{'Shares now':>12}"
        f"{'Target shares':>15}"
        f"{'Buy/Sell':>12}"
        f"{'Value after ($)':>18}"
        f"{'Weight after':>15}"
        f"{'Gap (pp)':>12}"
    )

    # Track the largest absolute gap from a target.
    _largest_gap = 0

    # Print one row for each stock.
    for _row in rebalance_results:
        (
            _ticker,
            _shares_now,
            _target_shares,
            _trade,
            _value_after,
            _percentage_after,
            _gap,
        ) = _row

        print(
            f"{_ticker:<8}"
            f"{_shares_now:>12}"
            f"{_target_shares:>15}"
            f"{_trade:>+12}"
            f"{_value_after:>18,.2f}"
            f"{_percentage_after:>14.4f}%"
            f"{_gap:>+12.4f}"
        )

        _largest_gap = max(_largest_gap, abs(_gap))

    # Display the remaining cash.
    print()
    print(f"Cash remaining: ${remaining_cash:,.2f}")
    print(
        f"Cash as a share of the portfolio: "
        f"{remaining_cash / total_portfolio_value:.4%}"
    )

    # Explain how to read the table.
    print()
    print("Buy/Sell: positive means buy; negative means sell; zero means hold.")
    print("Gap (pp): difference from the target in percentage points.")
    print("A negative gap means below target; a positive gap means above target.")

    # Summarize the distance from the targets.
    print()
    print(
        f"The largest absolute gap from a target is "
        f"{_largest_gap:.4f} percentage points."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I checked whether the total portfolio value before rebalancing equals the value after rebalancing. To calculate the final value independently, I multiplied each final share count by its original stock price and added the remaining cash. The final stocks are worth $120,577.08, and the remaining cash is $725.62, giving a total of $121,302.70. This matches the original portfolio value, so the difference is $0.00.
    """)
    return


@app.cell
def _(holdings, rebalance_results, remaining_cash, total_portfolio_value):
    # Independently calculate the final stock values using
    # the final share counts and the prices from the inputs.
    _checked_stock_value = 0

    for _holding in holdings:
        _ticker, _original_shares, _price = _holding

        for _result in rebalance_results:
            if _result[0] == _ticker:
                _final_shares = _result[2]
                _checked_stock_value += _final_shares * _price

    _checked_stock_value = round(_checked_stock_value, 2)

    # Add the remaining cash to get the final portfolio value.
    _checked_portfolio_value = round(
        _checked_stock_value + remaining_cash, 2
    )

    # Compare the final value with the original value.
    _difference = round(
        _checked_portfolio_value - total_portfolio_value, 2
    )

    print(f"Original portfolio value: ${total_portfolio_value:,.2f}")
    print(f"Final stock value:        ${_checked_stock_value:,.2f}")
    print(f"Remaining cash:           ${remaining_cash:,.2f}")
    print(f"Final portfolio value:    ${_checked_portfolio_value:,.2f}")
    print(f"Difference:              ${_difference:,.2f}")

    if _difference == 0:
        print("Check passed: the portfolio value is unchanged.")
    else:
        print("Check failed: review the calculations.")
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
    I verified the agent’s calculations by manually working through Apple and Tesla using a calculator and pen and paper. For each stock, I calculated its current value, target dollar amount, whole-share target, required trade, final value, and final portfolio weight. My calculations showed that Apple required buying 39 shares and Tesla required selling 79 shares, matching the results in Section 5. Checking both a purchase and a sale helped me verify that the code calculated the trade quantities and directions correctly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # *GOING "2" STEPS FURTHER.*#
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # *A. Use today's (Oct 9, 2026) prices from yfinance in place of the listed ones.*#
    """)
    return


@app.cell
def _():
    updated_holdings = [
        ("AAPL", 100, 336.64),
        ("MSFT", 50, 535.07),
        ("GOOG", 80, 347.86),
        ("AMZN", 200, 262.43),
        ("NVDA", 20, 229.28),
        ("TSLA", 150, 382.70),
    ]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For this extension, I used an updated stock-price snapshot while keeping the original share counts, $5,000 cash balance, and target allocations unchanged. I assumed there were no trading fees.

    The calculation method remains the same as in Sections 4 and 5: calculate the total portfolio value, determine the whole-share targets, calculate the required trades, and report the remaining cash and gaps from the targets. Only the stock prices change, which produces different results.

    I kept Sections 3–6 unchanged to preserve the original assignment results and used the updated prices separately in Section 8 for comparison.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # *B. Importing Netflix stock price by importing a yfinance library*#


    This code uses the yfinance library to retrieve Netflix’s recent stock-price history and display its latest available daily closing price and date. It fetches the data automatically rather than using a manually entered price.
    """)
    return


@app.cell
def _():
    # Import the library used to fetch prices.
    import yfinance as _yf_test

    # Fetch recent price history for Netflix.
    _netflix_history = _yf_test.Ticker("NFLX").history(
        period="5d",
        auto_adjust=False
    )

    # Check whether any prices were returned.
    if _netflix_history.empty:
        print("No price was returned. The download did not succeed.")
    else:
        _netflix_price = float(_netflix_history["Close"].iloc[-1])
        _netflix_date = _netflix_history.index[-1].strftime("%Y-%m-%d")

        print("Price successfully fetched using yfinance.")
        print("Stock: Netflix (NFLX)")
        print(f"Latest available closing price: ${_netflix_price:,.2f}")
        print(f"Price date: {_netflix_date}")
    return


if __name__ == "__main__":
    app.run()
