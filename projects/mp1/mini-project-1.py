# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.0"
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
    For a coffee shop manager, I want to create an inventory management tool that helps track how many cases of oat milk are being used and when new stock needs to be ordered. Starting with 100 cases, the tool will monitor daily inventory and help determine the best time to reorder to avoid shortages and unnecessary overstocking.
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
    I want to start with 100 cases of oat milk in the coffee shop's inventory.
    Each day, the system will track how many cases of oat milk are being used and subtract that amount from the available inventory.
    I want to test different reorder points of 20, 30, and 40 cases to determine which works best.
    Once the inventory reaches a reorder point, the system should indicate that it's time to place another order.
    I will account for how long it takes for new stock to arrive and add the delivery to the inventory once it comes in.
    I want to simulate the inventory over 30 days to see how often we need to reorder and whether we run out of oat milk.
    Finally, I will compare the results to determine which reorder point helps prevent shortages while avoiding unnecessary overstocking.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I will manually calculate how much oat milk should be left after a day and compare it to what my Python program calculates. For example, if I start with 100 cases and use 15 cases in one day, I should have 85 cases remaining. The manual calculation and the Python result should match
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My loop will keep track of how many cases of oat milk are left at the end of each day. It will subtract the amount used daily and add any new deliveries when they arrive. This way, the inventory is constantly updated, and the system can determine when it's time to reorder.
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
    starting_stock = 60
    order_quantity = 100
    lead_time_days = 3
    reorder_points = [20, 30, 40, 50]

    daily_demand = [
        12, 15, 9, 14, 18, 11, 10, 16, 13, 17,
        8, 12, 20, 14, 11, 9, 15, 13, 16, 12,
        10, 14, 19, 11, 13, 15, 9, 12, 17, 14
    ]

    print("Starting stock:", starting_stock)
    print("Order quantity:", order_quantity)
    print("Delivery time:", lead_time_days, "days")
    print("Reorder points:", reorder_points)
    print("Simulation days:", len(daily_demand))
    return (
        daily_demand,
        lead_time_days,
        order_quantity,
        reorder_points,
        starting_stock,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(daily_demand, lead_time_days, order_quantity, starting_stock):

    def simulate_inventory(reorder_point):
        stock = starting_stock
        pending_orders = []
        daily_records = []

        for day, demand in enumerate(daily_demand, start=1):
            starting_today = stock

            # Receive deliveries due today
            arrived = sum(
                quantity for arrival_day, quantity in pending_orders
                if arrival_day == day
            )
            stock += arrived
            pending_orders = [
                order for order in pending_orders if order[0] > day
            ]

            # Sell available stock and count lost demand
            sold = min(stock, demand)
            lost = demand - sold
            stock -= sold

            # Check stock plus outstanding orders
            on_order = sum(quantity for _, quantity in pending_orders)
            units_ordered = 0

            if stock + on_order <= reorder_point:
                units_ordered = order_quantity
                pending_orders.append(
                    (day + lead_time_days, order_quantity)
                )

            daily_records.append({
                "day": day,
                "starting_stock": starting_today,
                "arrived": arrived,
                "demand": demand,
                "sold": sold,
                "lost": lost,
                "ending_stock": stock,
                "units_ordered": units_ordered
            })

        return daily_records

    records_40 = simulate_inventory(40)
    print("Days simulated:", len(records_40))
    print("Day 1:", records_40[0])

    return records_40, simulate_inventory


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(records_40, reorder_points, simulate_inventory):

    # Table 1: Daily inventory for reorder point 40
    print("DAILY INVENTORY — REORDER POINT 40")
    print(f"{'Day':>3} | {'Start':>5} | {'Arrived':>7} | {'Demand':>6} | {'Sold':>4} | {'Lost':>4} | {'End':>5} | {'Ordered':>7}")

    for daily_record in records_40:
        print(
            f"{daily_record['day']:>3} | "
            f"{daily_record['starting_stock']:>5} | "
            f"{daily_record['arrived']:>7} | "
            f"{daily_record['demand']:>6} | "
            f"{daily_record['sold']:>4} | "
            f"{daily_record['lost']:>4} | "
            f"{daily_record['ending_stock']:>5} | "
            f"{daily_record['units_ordered']:>7}"
        )

    # Table 2: Compare all reorder points
    comparison_results = []

    for point in reorder_points:
        point_records = simulate_inventory(point)

        total_lost = sum(r["lost"] for r in point_records)
        lost_days = sum(1 for r in point_records if r["lost"] > 0)
        orders = sum(1 for r in point_records if r["units_ordered"] > 0)
        average_stock = sum(r["ending_stock"] for r in point_records) / len(point_records)

        comparison_results.append({
            "reorder_point": point,
            "total_lost": total_lost,
            "lost_days": lost_days,
            "orders": orders,
            "average_stock": average_stock
        })

    print("\nREORDER POINT COMPARISON")
    print(f"{'Point':>5} | {'Lost Units':>10} | {'Lost Days':>9} | {'Orders':>6} | {'Avg Ending Stock':>16}")

    for result in comparison_results:
        print(
            f"{result['reorder_point']:>5} | "
            f"{result['total_lost']:>10} | "
            f"{result['lost_days']:>9} | "
            f"{result['orders']:>6} | "
            f"{result['average_stock']:>16.2f}"
        )

    # Recommendation: prioritize fewer lost sales, then lower stock
    best_result = comparison_results[0]

    for candidate in comparison_results:
        if candidate["total_lost"] < best_result["total_lost"]:
            best_result = candidate
        elif candidate["total_lost"] == best_result["total_lost"]:
            if candidate["average_stock"] < best_result["average_stock"]:
                best_result = candidate

    print(
        f"\nRecommendation: Use reorder point {best_result['reorder_point']} "
        f"with {best_result['total_lost']} lost units and average ending stock "
        f"of {best_result['average_stock']:.2f} cartons."
    )


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My Recommendation

    I recommend a reorder point of 40 cartons because it resulted in zero lost sales over the 30 days, with an average ending stock of 48.43 cartons. A reorder point of 50 also had zero lost sales, but it kept more inventory on hand, averaging 58.43 cartons. Since the coffee shop has limited refrigerator space, I think 40 cartons is the better choice.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(records_40):

    # Independently check Day 1
    manual_start = 60
    manual_demand = 12
    manual_end = manual_start - manual_demand

    python_end = records_40[0]["ending_stock"]

    print("Manual ending stock:", manual_end)
    print("Python ending stock:", python_end)
    print("Do they match?", manual_end == python_end)

    # Independently check Day 5
    # Day 2's order arrives at the start of Day 5
    manual_day5_start = 10
    manual_day5_delivery = 100
    manual_day5_demand = 18
    manual_day5_end = manual_day5_start + manual_day5_delivery - manual_day5_demand

    python_day5_end = records_40[4]["ending_stock"]

    print("Manual Day 5 ending stock:", manual_day5_end)
    print("Python Day 5 ending stock:", python_day5_end)
    print("Do they match?", manual_day5_end == python_day5_end)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I manually checked the inventory calculations for Days 1 and 5. On Day 1, the coffee shop started with 60 cartons and sold 12, leaving 48. On Day 5, the shop started with 10 cartons, received 100, and sold 18, leaving 92. Both manual calculations matched the Python results, which gives me confidence that the simulation is updating inventory correctly for these examples.
    """)
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
    I used AI to help me write the Python code for my coffee shop's oat milk inventory simulation. However, when I compared the code with my professor's requirements, I realized that my original plan used different inventory values. I corrected the inputs in Section 3 to match the assignment, including starting with 60 cartons, ordering 100 cartons at a time, allowing three days for delivery, and testing reorder points of 20, 30, 40, and 50.

    I also wanted to make sure the calculations were accurate, so I manually checked Days 1 and 5 in Section 6. Both calculations matched the Python results, which helped me better understand how the inventory changes each day.

    Another example was in Section 8, where AI initially predicted four days when inventory would fall below 20 cartons. However, after running the actual Python code, I found six days instead. This showed me why it's important to use AI as a tool while still checking its work rather than assuming every answer it gives is correct.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(records_40):


    low_stock_limit = 20

    print("OAT MILK LOW-STOCK WARNINGS")

    low_stock_days = 0

    for warning_record in records_40:
        if warning_record["ending_stock"] < low_stock_limit:
            low_stock_days += 1
            print(
                "Day", warning_record["day"],
                "- LOW STOCK:",
                warning_record["ending_stock"],
                "cartons remaining"
            )

    print("Total low-stock days:", low_stock_days)


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For my Going Further section, I decided to add a low-stock warning feature to my coffee shop's oat milk inventory system. I wanted to make the simulation more useful by showing the manager exactly when inventory was getting low, rather than just displaying the daily stock levels.

    In the Python cell above, I used a for loop and an if statement to check the ending inventory for each day. Whenever stock dropped below 20 cartons, the program displayed a warning. After running the simulation, I found six low-stock days: Days 4, 11, 12, 19, 26, and 27.

    I did run into a small issue because marimo wouldn't let me use a variable name that was already defined in another cell. Once I changed the name, the code ran correctly.

    What I found interesting was that even though the reorder point of 40 prevented any lost sales, there were still days when inventory was very low. This showed me how adding a simple warning feature could help a manager keep a closer eye on stock and plan ahead. It also helped me understand how Python can be used to identify potential problems and support everyday business decisions.
    """)
    return


if __name__ == "__main__":
    app.run()
