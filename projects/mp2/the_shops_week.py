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
    *SECTION 1: THE QUESTION*

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *SECTION 3: INPUTS*
    """)
    return


@app.cell
def _():
    import requests
    import json
    from datetime import date, timedelta
    from pathlib import Path

    days = 7
    base_url = "https://oim.zhili.dev"
    report_end = date.today()


    return Path, base_url, days, json, report_end, requests, timedelta


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *SECTION 4: THE WORK*
    """)
    return


@app.cell
def _(requests):
    #4A: Functions to retrieve the data

    def fetch_order_lines(base_url, order_id):
        # Build the address for one order.
        url = f"{base_url}/shop/orders/{order_id}"

        # Request the order details.
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Convert the API response into a Python dictionary.
        order_details = response.json()

        # Get the list of products in this order.
        lines = order_details["lines"]

        if len(lines) != order_details["line_count"]:
            raise ValueError("Some product lines are missing.")

        return lines


    def fetch_orders(base_url, start_date, end_date):
        all_orders = []
        order_ids = []

        page = 1
        more_pages = True

        while more_pages:
            # Set the dates and the page we want.
            parameters = {
                "from_date": str(start_date),
                "to_date": str(end_date),
                "page": page,
                "per_page": 10
            }

            # Request one page of orders.
            url = f"{base_url}/shop/orders"

            response = requests.get(
                url,
                params=parameters,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            # Add each order to our list.
            for order in data["items"]:
                order_id = order["order_id"]

                if order_id in order_ids:
                    raise ValueError("An order was collected more than once.")

                order_ids.append(order_id)
                all_orders.append(order)

            # Read the API's pagination information.
            total_expected = data["pagination"]["total"]
            more_pages = data["pagination"]["has_next"]

            page = page + 1

        # Check that we collected every order.
        if len(all_orders) != total_expected:
            raise ValueError("The number of orders does not match the API.")

        # Add the product lines to each order.
        for order in all_orders:
            order_id = order["order_id"]
            order["lines"] = fetch_order_lines(base_url, order_id)

        return all_orders

    return (fetch_orders,)


@app.cell
def _(base_url, days, fetch_orders, report_end, timedelta):
    #4B: Retrieve and summarize the orders


    # Make sure the number of days is valid.
    if type(days) is not int or days < 1:
        raise ValueError("Enter a positive whole number for days.")

    # Include today, so seven days means today plus six earlier days.
    report_start = report_end - timedelta(days=days - 1)

    # Fetch the orders and their product lines.
    orders = fetch_orders(base_url, report_start, report_end)

    # Create starting values for the calculations.
    order_count = len(orders)
    total_revenue = 0

    revenue_by_country = {}
    product_sales = {}
    unshipped_orders = []

    # Process one order at a time.
    for _order in orders:

        # Add this order's revenue.
        total_revenue = total_revenue + _order["order_total_dollars"]

        # Find its shipping destination.
        _country = _order["ship_country"]

        if _country is None or _country == "":
            _country = "Unknown"

        # Create an entry if this is the first order for this country.
        if _country not in revenue_by_country:
            revenue_by_country[_country] = 0

        # Add this order's revenue to the country total.
        revenue_by_country[_country] = (
            revenue_by_country[_country]
            + _order["order_total_dollars"]
        )

        # Keep orders that have not shipped.
        if _order["shipped_date"] is None:
            unshipped_orders.append(_order)

        # Process each product line in this order.
        for _line in _order["lines"]:
            _product_id = _line["product_id"]

            # Create an entry when a product first appears.
            if _product_id not in product_sales:
                product_sales[_product_id] = {
                    "product_id": _product_id,
                    "product_name": _line["product_name"],
                    "units": 0
                }

            # Add the quantity to this product's running total.
            product_sales[_product_id]["units"] = (
                product_sales[_product_id]["units"]
                + _line["quantity"]
            )

    total_revenue = round(total_revenue, 2)

    print(f"Reporting period: {report_start} to {report_end}")
    print(f"Orders collected: {order_count}")
    print(f"Revenue excluding freight: ${total_revenue:,.2f}")
    print(f"Orders not shipped: {len(unshipped_orders)}")
    return (
        order_count,
        orders,
        product_sales,
        report_start,
        revenue_by_country,
        total_revenue,
        unshipped_orders,
    )


@app.cell
def _(product_sales, revenue_by_country, unshipped_orders):
    #4C: Prepare the report lists




    # Tell Python which value to use when sorting.
    def get_country_revenue(country_record):
        return country_record["revenue"]


    def get_product_units(product_record):
        return product_record["units"]


    def get_order_date(order_record):
        return order_record["order_date"]


    # Create a list of country results.
    country_rows = []

    for _country in revenue_by_country:
        _country_record = {
            "country": _country,
            "revenue": round(revenue_by_country[_country], 2)
        }

        country_rows.append(_country_record)

    # Put the highest-revenue countries first.
    country_rows = sorted(
        country_rows,
        key=get_country_revenue,
        reverse=True
    )


    # Create a list of product results.
    product_rows = []

    for _product_id in product_sales:
        product_rows.append(product_sales[_product_id])

    # Put the products with the most units first.
    product_rows = sorted(
        product_rows,
        key=get_product_units,
        reverse=True
    )

    # Keep the first five products.
    top_products = product_rows[:5]


    # Put the oldest unshipped orders first.
    sorted_unshipped_orders = sorted(
        unshipped_orders,
        key=get_order_date
    )
   
  
    return country_rows, sorted_unshipped_orders, top_products


@app.cell
def _(Path, json, orders, report_end, report_start):
    #4D: Save the fetched data



    # Create the data folder if it does not already exist.
    data_folder = Path("projects/mp2/data")
    data_folder.mkdir(parents=True, exist_ok=True)

    # Create a filename containing the reporting dates.
    file_name = f"orders_{report_start}_to_{report_end}.json"
    saved_file = data_folder / file_name

    # Save all fetched orders, including their product lines.
    with saved_file.open("w", encoding="utf-8") as _file:
        json.dump(orders, _file, indent=2, ensure_ascii=False)

    print(f"Saved {len(orders)} orders to {saved_file}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *SECTION 5: THE ANSWER*
    """)
    return


@app.cell
def _(
    country_rows,
    days,
    order_count,
    report_end,
    report_start,
    sorted_unshipped_orders,
    top_products,
    total_revenue,
):
    # Display the report title and dates.
    print("NORTHWIND TRADERS — SALES REPORT")
    print(f"Reporting period: {report_start} to {report_end}")
    print(f"Number of days: {days}")
    print()


    # 1. Display the overall results.
    print("OVERALL RESULTS")
    print("-" * 50)

    print(f"Number of orders: {order_count}")
    print(f"Revenue excluding freight: ${total_revenue:,.2f}")
    print(f"Orders not shipped: {len(sorted_unshipped_orders)}")
    print()


    # 2. Display revenue by shipping destination.
    print("REVENUE BY DESTINATION COUNTRY")
    print(f"{'Country':<30}{'Revenue ($)':>18}")
    print("-" * 48)

    if len(country_rows) == 0:
        print("No orders were received during this period.")

    for _row in country_rows:
        print(f"{_row['country']:<30}{_row['revenue']:>18,.2f}")

    print()


    # 3. Display the five products with the most units sold.
    print("TOP FIVE PRODUCTS BY UNITS SOLD")
    print(f"{'Product':<45}{'Units sold':>12}")
    print("-" * 57)

    if len(top_products) == 0:
        print("No products were sold during this period.")

    for _product in top_products:
        print(
            f"{_product['product_name']:<45}"
            f"{_product['units']:>12,}"
        )

    print()


    # 4. Display unshipped orders, oldest first.
    print("ORDERS FROM THIS PERIOD THAT HAVE NOT SHIPPED")

    print(
        f"{'Order ID':<12}"
        f"{'Order date':<14}"
        f"{'Customer':<45}"
        f"{'Total ($)':>15}"
    )

    print("-" * 86)

    if len(sorted_unshipped_orders) == 0:
        print("No orders from this period are awaiting shipment.")

    for _order in sorted_unshipped_orders:
        # Keep only the date portion of the date-and-time field.
        _order_date = _order["order_date"][:10]

        _customer_name = _order["customer_name"]

        if _customer_name is None or _customer_name == "":
            _customer_name = "Unknown"

        print(
            f"{_order['order_id']:<12}"
            f"{_order_date:<14}"
            f"{_customer_name:<45}"
            f"{_order['order_total_dollars']:>15,.2f}"
        )

    print()


    # 5. Generate a summary sentence for the manager.
    print("SUMMARY FOR THE MANAGER")

    if len(top_products) > 0:
        print(
            f"From {report_start} to {report_end}, Northwind Traders "
            f"received {order_count} orders worth ${total_revenue:,.2f} "
            f"excluding freight across {len(country_rows)} destination "
            f"country groups, with {top_products[0]['product_name']} "
            f"ranked first by units sold at {top_products[0]['units']} units "
            f"and {len(sorted_unshipped_orders)} orders from this period "
            f"still awaiting shipment."
        )
    else:
        print(
            f"From {report_start} to {report_end}, Northwind Traders "
            f"received {order_count} orders worth ${total_revenue:,.2f} "
            f"excluding freight, with no product sales recorded and "
            f"{len(sorted_unshipped_orders)} orders awaiting shipment."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *SECTION 6: HOW DO I KNOW THESE NUMBERS ARE RIGHT?*
    """)
    return


@app.cell
def _(orders, total_revenue):
    # CHECK 1: Calculate total revenue from the product lines.
    revenue_from_lines = 0

    for _order in orders:
        for _line in _order["lines"]:
            revenue_from_lines = (
                revenue_from_lines + _line["line_total_dollars"]
            )

    revenue_from_lines = round(revenue_from_lines, 2)

    print("CHECK 1: TOTAL REVENUE CALCULATED TWO WAYS")
    print("-" * 55)

    print(f"Revenue from order totals: ${total_revenue:,.2f}")
    print(f"Revenue from product lines: ${revenue_from_lines:,.2f}")

    if total_revenue == revenue_from_lines:
        print("PASS: Both calculations give the same total revenue.")
    else:
        print("FAIL: The totals are different and need investigation.")

    print()


    # CHECK 2: Recalculate one order using prices and quantities.
    print("CHECK 2: RECALCULATE ONE ORDER")
    print("-" * 55)

    if len(orders) > 0:
        _sample_order = orders[0]
        _calculated_order_total = 0

        print(f"Order ID: {_sample_order['order_id']}")
        print()

        print(
            f"{'Product ID':<12}"
            f"{'Price ($)':>12}"
            f"{'Quantity':>12}"
            f"{'Discount':>12}"
            f"{'Calculated ($)':>18}"
        )

        for _line in _sample_order["lines"]:
            # Calculate the product-line value after its discount.
            _calculated_line_total = (
                _line["unit_price_dollars"]
                * _line["quantity"]
                * (1 - _line["discount_fraction"])
            )

            # The API reports each line total to the nearest cent.
            _calculated_line_total = round(_calculated_line_total, 2)

            _calculated_order_total = (
                _calculated_order_total + _calculated_line_total
            )

            print(
                f"{_line['product_id']:<12}"
                f"{_line['unit_price_dollars']:>12,.2f}"
                f"{_line['quantity']:>12}"
                f"{_line['discount_fraction']:>12.0%}"
                f"{_calculated_line_total:>18,.2f}"
            )

        _calculated_order_total = round(_calculated_order_total, 2)
        _api_order_total = round(_sample_order["order_total_dollars"], 2)

        print()
        print(f"Order total reported by the API: ${_api_order_total:,.2f}")
        print(f"Order total calculated by me: ${_calculated_order_total:,.2f}")

        if _api_order_total == _calculated_order_total:
            print("PASS: The independently calculated order total matches.")
        else:
            print("FAIL: The order totals differ and need investigation.")

    else:
        print("No orders are available to check individually.")
        print("Matching zero totals alone does not verify an actual order.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *SECTION 7: WORKING WITH THE AGENT*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The AI helped me write the code to fetch orders, calculate the report, and save the data. However, its original code for Section 4C assigned the sorted list back to `unshipped_orders`, which was already defined in Section 4B. When I ran Cell 4C, marimo reported that the variable was already defined.

    I reported the error to the AI. Following its explanation, I changed the name of the sorted list to `sorted_unshipped_orders` in Section 4C. This kept the original list in Section 4B and gave the sorted list a separate name. Section 5 then used the new name when displaying unshipped orders.

    I verified the correction by rerunning Cell 4C, which completed without the duplicate-variable error. This taught me that marimo does not allow the same variable to be defined in two different cells. The relevant code is in Cells 4B and 4C.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *SECTION 8: READING IT BACK*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Function 1: fetch_order_lines

    This function takes two inputs: the API’s base address and the ID of one order. It requests the details of that order and returns a list of its product lines. Each line contains information such as the product name, quantity, unit price, and discount.

    One line I reviewed with the AI was:

    `order_details = response.json()`

    This line converts the API’s JSON response into a Python dictionary. The function can then access the product lines using `order_details["lines"]`.

    ### Function 2: fetch_orders

    This function takes three inputs: the API’s base address, the start date, and the end date. It returns a list of all orders within that reporting period, including each order’s product lines.

    The function collects orders one page at a time. It checks for duplicate order IDs and compares the number collected with the total reported by the API. It then calls `fetch_order_lines` for each order to add its product details.

    One line I reviewed with the AI was:

    `more_pages = data["pagination"]["has_next"]`

    This line reads whether another page of orders is available. If the value is `True`, the loop requests the next page. If it is `False`, the loop stops after processing the current page.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### My proposed change and prediction

    I will change `days` from 7 to 14 while keeping the same reporting end date.

    I expect the number of orders to increase or remain unchanged because the longer period includes all the original orders plus any orders from the additional seven days. Assuming the additional orders have non-negative totals, revenue should also increase or remain unchanged.

    The top-five product ranking may change because products that sold strongly during the additional week could move higher in the ranking.

    ### Results before the change

    - Reporting period: October 17–23, 2026 (7 days)
    - Number of orders: 22
    - Total revenue excluding freight: $569,630.89
    - Highest-ranked product: Manjimup Dried Apples
    - Units sold of the highest-ranked product: 363
    - Orders not shipped: 17
    """)
    return


if __name__ == "__main__":
    app.run()
