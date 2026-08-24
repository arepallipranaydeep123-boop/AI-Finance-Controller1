import pandas as pd


def calculate_financial_risk(
    anomaly_df,
    budget_df
):

    # --------------------------------
    # 1. ANOMALY RISK
    # --------------------------------

    high_risk_transactions = anomaly_df[
        anomaly_df["risk_level"] == "High"
    ]

    if len(anomaly_df) > 0:

        anomaly_risk = (
            len(high_risk_transactions)
            / len(anomaly_df)
        ) * 100

    else:

        anomaly_risk = 0


    # --------------------------------
    # 2. BUDGET RISK
    # --------------------------------

    high_budget_risk = budget_df[
        budget_df["status"] == "High Risk"
    ]

    over_budget = budget_df[
        budget_df["status"] == "Over Budget"
    ]

    if len(budget_df) > 0:

        budget_risk = (
            (
                len(high_budget_risk) * 2
                + len(over_budget)
            )
            / len(budget_df)
        ) * 100

    else:

        budget_risk = 0


    # --------------------------------
    # 3. LIMIT SCORES
    # --------------------------------

    anomaly_risk = min(
        anomaly_risk,
        100
    )

    budget_risk = min(
        budget_risk,
        100
    )


    # --------------------------------
    # 4. COMBINED SCORE
    # --------------------------------

    financial_risk = (
        anomaly_risk * 0.5
        + budget_risk * 0.5
    )


    # --------------------------------
    # 5. RISK LEVEL
    # --------------------------------

    if financial_risk >= 70:

        risk_level = "High"

    elif financial_risk >= 40:

        risk_level = "Medium"

    else:

        risk_level = "Low"


    return {
        "financial_risk": financial_risk,
        "anomaly_risk": anomaly_risk,
        "budget_risk": budget_risk,
        "risk_level": risk_level
    }

if __name__ == "__main__":

    transactions = pd.read_csv(
        "data/transactions.csv"
    )

    from anomaly_detection import (
        detect_anomalies,
        add_risk_reason,
        calculate_risk_score
    )

    from budget_analysis import (
        calculate_budget_risk
    )

    anomalies = detect_anomalies(
        transactions
    )

    anomalies = add_risk_reason(
        anomalies
    )

    anomalies = calculate_risk_score(
        anomalies
    )

    budget = calculate_budget_risk(
        transactions
    )

    result = calculate_financial_risk(
        anomalies,
        budget
    )

    print("\n==============================")
    print("FINANCIAL RISK SCORE")
    print("==============================")

    print(
        f"Financial Risk: "
        f"{result['financial_risk']:.1f}/100"
    )

    print(
        f"Anomaly Risk: "
        f"{result['anomaly_risk']:.1f}/100"
    )

    print(
        f"Budget Risk: "
        f"{result['budget_risk']:.1f}/100"
    )

    print(
        f"Risk Level: "
        f"{result['risk_level']}"
    )
if __name__ == "__main__":

    transactions = pd.read_csv(
        "data/transactions.csv"
    )

    from anomaly_detection import (
        detect_anomalies,
        add_risk_reason,
        calculate_risk_score
    )

    from budget_analysis import (
        calculate_budget_risk
    )

    anomalies = detect_anomalies(
        transactions
    )

    anomalies = add_risk_reason(
        anomalies
    )

    anomalies = calculate_risk_score(
        anomalies
    )

    budget = calculate_budget_risk(
        transactions
    )

    result = calculate_financial_risk(
        anomalies,
        budget
    )

    print("\n==============================")
    print("FINANCIAL RISK SCORE")
    print("==============================")

    print(
        f"Financial Risk: "
        f"{result['financial_risk']:.1f}/100"
    )

    print(
        f"Anomaly Risk: "
        f"{result['anomaly_risk']:.1f}/100"
    )

    print(
        f"Budget Risk: "
        f"{result['budget_risk']:.1f}/100"
    )

    print(
        f"Risk Level: "
        f"{result['risk_level']}"
    )