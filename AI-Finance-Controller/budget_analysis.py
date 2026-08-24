import pandas as pd


def calculate_budget_risk(df):

    expenses = df[
        df["type"] == "Expense"
    ]

    budget_result = (
        expenses
        .groupby("category")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "actual_amount"})
    )
    budget_result["actual"] = budget_result[
        "actual_amount"
    ]

    if budget_result.empty:
        budget_result["budget"] = pd.Series(dtype=float)
        budget_result["variance_percent"] = pd.Series(dtype=float)
        budget_result["status"] = pd.Series(dtype=str)
        return budget_result

    budget_result["budget"] = budget_result[
        "actual_amount"
    ].mean()

    if budget_result["budget"].iloc[0] == 0:
        budget_result["variance_percent"] = 0.0
    else:
        budget_result["variance_percent"] = (
            (
                budget_result["actual_amount"]
                - budget_result["budget"]
            )
            / budget_result["budget"]
        ) * 100

    budget_result["status"] = budget_result[
        "variance_percent"
    ].apply(
        lambda value: "High Risk"
        if value >= 50
        else "Over Budget"
        if value > 0
        else "Within Budget"
    )

    return budget_result
