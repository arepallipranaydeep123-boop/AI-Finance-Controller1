import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    # Only analyze expenses
    expenses = df[
        df["type"] == "Expense"
    ].copy()

    # Make sure amount is numeric
    expenses["amount"] = pd.to_numeric(
        expenses["amount"],
        errors="coerce"
    )

    expenses = expenses.dropna(
        subset=["amount"]
    )

    # If there aren't enough transactions,
    # don't run anomaly detection
    if len(expenses) < 10:
        expenses["anomaly"] = 1
        expenses["risk_level"] = "Low"
        return expenses

    # Isolation Forest
    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    expenses["anomaly"] = model.fit_predict(
        expenses[["amount"]]
    )

    # Convert anomaly result into risk
    expenses["risk_level"] = expenses[
        "anomaly"
    ].apply(
        lambda x: "High" if x == -1 else "Low"
    )

    return expenses

if __name__ == "__main__":

    df = pd.read_csv(
        "data/transactions.csv"
    )

    anomalies = detect_anomalies(df)

    print("\n==========================")
    print("ANOMALY DETECTION")
    print("==========================")

    print(
        anomalies[
            anomalies["anomaly"] == -1
        ][
            ["amount", "category", "risk_level"]
        ]
    )

def add_risk_reason(df):

    df = df.copy()

    expense_mean = df[
        df["type"] == "Expense"
    ]["amount"].mean()

    def reason(row):

        if row["risk_level"] == "High":

            if row["amount"] > expense_mean * 3:
                return (
                    "Transaction is more than "
                    "3x the average expense."
                )

            return (
                "Transaction is significantly "
                "higher than normal."
            )

        return "Normal transaction."

    df["risk_reason"] = df.apply(
        reason,
        axis=1
    )

    return df


def calculate_risk_score(df):

    df = df.copy()

    expense_mean = df[
        df["type"] == "Expense"
    ]["amount"].mean()

    if pd.isna(expense_mean) or expense_mean == 0:
        df["risk_score"] = 0.0
        return df

    df["risk_score"] = (
        df["amount"] / expense_mean * 25
    ).clip(upper=100).round(2)

    return df