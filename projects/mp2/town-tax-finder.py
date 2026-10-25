import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. The Question
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A couple is planning to purchase a single-family home in Middlesex County, Massachusetts, with a maximum budget of $700,000. Since the purchase price is only one part of homeownership, they also want to keep their annual property taxes below $8,000 to better manage their long-term housing expenses. This tool will help them identify towns where both the average single-family home value and average annual property tax bill meet their financial limits, ranking the qualifying towns from lowest to highest tax bill so they can make a more informed decision about where to begin their home search.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. My Plan Before AI

    Start with the couple's budget. I want to start by setting the county to Middlesex, the home budget to $700,000, the annual property tax limit to $8,000, and the fiscal year to 2026. Having these inputs together will make it easier to change the numbers later without having to redo the entire analysis.

    Understand where the information is coming from. Before writing the code, I want to look at the Massachusetts API to see what information is available and how it's organized. I especially want to understand how the town names, property values, and tax information are displayed, since I'll need those numbers to make the comparisons.

    Collect the information for each town. My plan is to first get the list of towns in Middlesex County and then use each town's DOR code to find its property tax information for 2026. I want to make sure I'm comparing information from the same year so the results are consistent.

    Make sure I'm not leaving out any towns. I know that an API might not return every town in one request, so I'll need to check whether there are additional pages of results. I'll compare the number of towns I collected with the total number the API reports to make sure nothing was missed.

    Check the information before comparing anything. Once I have the records, I'll look at the average single-family home values, residential tax rates, and average property tax bills. I'll also check whether any values are missing or need to be converted into numbers before using them.

    Find the towns that fit the budget. I'll use a Python for loop to go through each town and check whether the average home value is $700,000 or less and the average annual property tax bill is below $8,000. If a town meets both requirements, I'll add it to a separate list.

    Organize the results. After identifying the towns that qualify, I'll sort them by their average annual property tax bill, starting with the lowest. I think this will make the results more useful because the couple can see which towns might be more affordable in the long run.

    Make the answer easy to understand. I want the final output to be a simple table showing the town name, average home value, residential tax rate, and average annual tax bill. I'll also include a short explanation of how many towns qualify and which town has the lowest average bill.

    Double-check the results and take it a little further. I want to make sure the number of towns I collected matches what the API says should be there. I also think it would be interesting to estimate the property taxes on a home purchased for exactly $700,000. The average tax bill might be different from what someone actually pays, so this could give the couple another way to think about their budget.

    Functions I Plan to Use

    I think I'll need one function that takes the county and fiscal year, requests the town and property tax information from the API, and returns the records. I'll also need a function that goes through those records, checks the couple's budget requirements, and returns the towns that qualify.

    API Addresses

    I'll use two API addresses:

    https://oim.zhili.dev/ma/towns?county=Middlesex to get the towns in Middlesex County.

    https://oim.zhili.dev/ma/towns/{dor_code}/history to find each town's historical property tax information.

    How I'll Know I Have Every Record

    I'll check how many towns the API says are available and compare that with how many I actually collected. If the numbers don't match, I'll know I need to look for missing pages or records.

    How I'll Check My Results in Section 6

    I'll compare the total number of towns collected with the total reported by the API. Both numbers should match. I'll also pick a town from my final table and compare its property value and tax bill against the original API response to make sure the numbers are correct.
    """)
    return


if __name__ == "__main__":
    app.run()
