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
    ## 2. My Plan Before AI

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs
    """)
    return


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    county, budget_dollars, tax_limit_dollars, fiscal_year
    return budget_dollars, county, fiscal_year, tax_limit_dollars


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work
    """)
    return


@app.cell
def _(county):
    import requests

    url = "https://oim.zhili.dev/ma/towns"

    town_reply = requests.get(
        url,
        params={"county": county, "limit": 100},
        timeout=10,
    )

    town_reply.status_code
    return requests, town_reply


@app.cell
def _(town_reply):
    town_data = town_reply.json()

    town_data
    return


@app.cell
def _(requests):
    def fetch_towns(county_name):
        all_towns = []
        page = 1
        total = 0

        while True:
            reply = requests.get(
                "https://oim.zhili.dev/ma/towns",
                params={
                    "county": county_name,
                    "page": page,
                    "per_page": 50,
                },
                timeout=10,
            )

            reply.raise_for_status()
            data = reply.json()

            total = data["pagination"]["total"]

            for _town in data["items"]:
                all_towns.append(_town)

            if not data["pagination"]["has_next"]:
                break

            page += 1

        return all_towns, total

    return (fetch_towns,)


@app.cell
def _(county, fetch_towns):
    all_towns, expected_total = fetch_towns(county)

    print("Towns collected:", len(all_towns))
    print("API reported total:", expected_total)
    print("Counts match:", len(all_towns) == expected_total)
    return all_towns, expected_total


@app.cell
def _(requests):
    history_url = "https://oim.zhili.dev/ma/towns/002/history"

    history_reply = requests.get(history_url, timeout=10)
    history_reply.raise_for_status()

    history_data = history_reply.json()

    history_data
    return


@app.cell
def _(requests):
    def fetch_tax_history(towns, year):
        tax_records = []

        for _town in towns:
            dor_code = _town["dor_code"]

            url = f"https://oim.zhili.dev/ma/towns/{dor_code}/history"

            reply = requests.get(url, timeout=10)
            reply.raise_for_status()

            history = reply.json()

            for _record in history["years"]:
                if _record["fiscal_year"] == year:
                    tax_records.append({
                        "name": _town["name"],
                        "dor_code": dor_code,
                        "fiscal_year": year,
                        "average_value": _record["average_single_family_value_dollars"],
                        "average_tax": _record["average_single_family_bill_dollars"],
                        "tax_rate": _record["residential_rate_per_thousand"]
                    })

        return tax_records

    return (fetch_tax_history,)


@app.cell
def _(all_towns, fetch_tax_history, fiscal_year):
    tax_records = fetch_tax_history(all_towns, fiscal_year)

    print("Municipalities with 2026 data:", len(tax_records))
    print("First record:", tax_records[0])
    return (tax_records,)


@app.cell
def _(budget_dollars, tax_limit_dollars, tax_records):
    qualifying_towns = []

    for _town in tax_records:
        if _town["average_value"] is not None and _town["average_tax"] is not None:
            if _town["average_value"] <= budget_dollars and _town["average_tax"] < tax_limit_dollars:
                qualifying_towns.append(_town)

    print("Municipalities that qualify:", len(qualifying_towns))
    return (qualifying_towns,)


@app.cell
def _(qualifying_towns):
    ranked_towns = sorted(
        qualifying_towns,
        key=lambda _town: _town["average_tax"]
    )

    ranked_towns
    return (ranked_towns,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer
    """)
    return


@app.cell
def _(budget_dollars, county, fiscal_year, ranked_towns, tax_limit_dollars):
    print(f"FY {fiscal_year} - {county} County")
    print(f"Maximum home value: ${budget_dollars:,}")
    print(f"Annual property tax limit: Under ${tax_limit_dollars:,}")
    print()

    print("Rank | Municipality | Avg Home Value | Tax Rate | Avg Tax Bill")
    print("-" * 75)

    for _rank, _town in enumerate(ranked_towns, start=1):
        print(
            f'{_rank} | '
            f'{_town["name"]} | '
            f'${_town["average_value"]:,} | '
            f'${_town["tax_rate"]:.2f} | '
            f'${_town["average_tax"]:,}'
        )

    print()
    print(
        f"Based on FY {fiscal_year} data, {len(ranked_towns)} municipalities "
        f"in {county} County meet both the home value and property tax limits."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I checked whether the number of municipalities retrieved matched
    the total reported by the API. Both numbers were 54, confirming
    that the pagination process collected all the records.

    I also independently retrieved Malden's historical tax data using
    its DOR code, 165. For fiscal year 2026, the API reported an
    average single-family home value of $434,420 and an average
    annual property tax bill of $4,952. These values matched my
    ranked results.
    """)
    return


@app.cell
def _(all_towns, expected_total, fiscal_year, requests):
    check_url = "https://oim.zhili.dev/ma/towns/165/history"

    check_reply = requests.get(check_url, timeout=10)
    check_reply.raise_for_status()

    check_data = check_reply.json()

    for _year in check_data["years"]:
        if _year["fiscal_year"] == fiscal_year:
            print("Independent check: Malden")
            print("Fiscal year:", _year["fiscal_year"])
            print("Average home value:", _year["average_single_family_value_dollars"])
            print("Average property tax:", _year["average_single_family_bill_dollars"])

    print()
    print("All municipalities collected:", len(all_towns) == expected_total)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    I used ChatGPT to help me organize my Python code and work through the API requests. One important thing I learned was that getting a successful API response does not necessarily mean I have collected all the data. My first request returned 50 municipalities, but the API reported 54 in total.

    I adjusted the code to retrieve the remaining page and then checked that the number of records matched the API's total. I also verified Malden's 2026 home value and property tax bill directly from its historical record instead of relying only on the final results.

    This helped me understand why checking the data is just as important as getting the code to run.

    For evidence of my development process, see my GitHub commits mp2: plan before AI and mp2: prediction, which document my initial planning and prediction test.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Reading It Back

    ### Function 1: fetch_towns()

    The `fetch_towns()` function takes a county name as its input. It sends requests to the API and uses a loop to collect municipalities from each page. It returns the complete list of municipalities and the total number reported by the API.

    ### Function 2: fetch_tax_history()

    The `fetch_tax_history()` function takes the list of municipalities and a fiscal year as inputs. It retrieves the historical tax records for each municipality, finds the requested year, and saves the average home value, average property tax bill, and residential tax rate.

    ### A line I wanted to understand

    The line `reply.raise_for_status()` checks whether the API request was successful. If the server returns an HTTP error, it raises an exception rather than letting the program continue as though the request worked.

    ### My prediction

    If I reduce the maximum home value from $700,000 to $500,000, I predict that fewer municipalities will qualify because some of the original 12 have average home values above $500,000.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What happened when I tested it

    After changing the maximum average home value from $700,000 to $500,000, the number of qualifying municipalities decreased from 12 to 4. The remaining municipalities were Malden, Everett, Ashby, and Townsend.

    This matched my prediction that fewer municipalities would qualify when I lowered the budget. It also showed me that changing one input can affect the final results without having to rewrite the filtering code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Going Further

    I wanted to estimate how much property tax the couple might pay if they purchased a home assessed at exactly $700,000 in each qualifying municipality, instead of using the municipality's average tax bill.

    To do this, I used the residential property tax rate per $1,000 of assessed value. This is an estimate, and the actual tax bill may differ depending on the property's assessment and any applicable exemptions.
    """)
    return


@app.cell
def _(ranked_towns):
    print("Municipality | Estimated Tax on $700,000")

    for _town in ranked_towns:
        if _town["tax_rate"] is not None:
            _estimated_tax = 700 * float(_town["tax_rate"])
            print(_town["name"], "|", f"${_estimated_tax:,.2f}")


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What I Learned

    I found that the estimated property tax on a $700,000 home can be different from the average property tax bill reported for each municipality. For example, Malden's estimated tax was $7,980, while Ashby's was $11,032.

    This showed me why it is important to consider the residential tax rate when comparing towns. Even if a municipality meets the original budget requirements based on average values, the taxes on a specific property could be higher.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Time Spent

    I spent approximately 4 hours completing this project. This included planning, collecting information from the API, debugging the pagination, filtering and ranking municipalities, verifying the results, and testing a different budget.
    """)
    return


@app.cell
def _(all_towns, ranked_towns, tax_records):
    import json
    from pathlib import Path

    data_folder = Path("projects/mp2/data")
    data_folder.mkdir(parents=True, exist_ok=True)

    with open(data_folder / "middlesex_towns.json", "w") as file:
        json.dump(all_towns, file, indent=2)

    with open(data_folder / "middlesex_tax_2026.json", "w") as file:
        json.dump(tax_records, file, indent=2)

    with open(data_folder / "qualifying_towns.json", "w") as file:
        json.dump(ranked_towns, file, indent=2)

    print("Data saved successfully!")
    print("Folder:", data_folder)
    return


if __name__ == "__main__":
    app.run()
