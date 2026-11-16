import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # BabsonAI Labs — Database Project Part B

    ## Reading It Back

    Selected question: How many tasks and how much total expense does each project have?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### My Prediction

    I predict that joining PROJECTS, TASKS, and EXPENSES will produce several thousand rows before grouping. This is because each task can be matched with every expense belonging to the same project. For example, a project with 5 tasks and 3 expenses would produce 15 rows.
    """)
    return


if __name__ == "__main__":
    app.run()
