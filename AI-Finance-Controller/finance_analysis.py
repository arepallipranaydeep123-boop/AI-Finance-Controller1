import pandas as pd

# Load master transaction dataset
df = pd.read_csv("data/transactions.csv")

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", df.columns.tolist())

# Convert amount to numeric
df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
)

# Remove invalid amounts
df = df.dropna(
    subset=["amount"]
)

#Calculate Revenue
revenue = df[
    df["type"] == "Revenue"
]["amount"].sum()

print("\nTotal Revenue:")
print(revenue)

#Calculate Expenses
expenses = df[
    df["type"] == "Expense"
]["amount"].sum()

print("\nTotal Expenses:")
print(expenses)

#Calculate Profit
profit = revenue - expenses

print("\nTotal Profit:")
print(profit)

#Calculate Profit Margin
if revenue > 0:
    profit_margin = (
        profit / revenue
    ) * 100
else:
    profit_margin = 0

print("\nProfit Margin:")
print(f"{profit_margin:.2f}%")

#Find the highest expense categories
expense_data = df[
    df["type"] == "Expense"
]

category_expenses = (
    expense_data
    .groupby("category")["amount"]
    .sum()
    .sort_values(
        ascending=False
    )
)

print("\nExpenses by Category:")
print(category_expenses)

#Find the biggest spending category
if len(category_expenses) > 0:

    top_category = (
        category_expenses
        .index[0]
    )

    top_category_amount = (
        category_expenses.iloc[0]
    )

    print("\nHighest Expense Category:")
    print(top_category)

    print("Amount:")
    print(top_category_amount)

    #Monthly analysis

    df["date"] = pd.to_datetime(
    df["date_time"],
    errors="coerce"
)

df = df.dropna(
    subset=["date"]
)
df["month"] = df["date"].dt.to_period(
    "M"
).astype(str)

monthly_revenue = (
    df[df["type"] == "Revenue"]
    .groupby("month")["amount"]
    .sum()
)

monthly_expenses = (
    df[df["type"] == "Expense"]
    .groupby("month")["amount"]
    .sum()
)

print("\nMonthly Revenue:")
print(monthly_revenue)

print("\nMonthly Expenses:")
print(monthly_expenses)

#Calculate monthly profit
monthly_profit = (
    monthly_revenue
    .sub(
        monthly_expenses,
        fill_value=0
    )
)

print("\nMonthly Profit:")
print(monthly_profit)

def get_financial_summary(df):

    revenue = df[
        df["type"] == "Revenue"
    ]["amount"].sum()

    expenses = df[
        df["type"] == "Expense"
    ]["amount"].sum()

    profit = revenue - expenses

    if revenue > 0:
        profit_margin = (
            profit / revenue
        ) * 100
    else:
        profit_margin = 0

    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "profit_margin": profit_margin
    }

summary = get_financial_summary(df)

print("\n==========================")
print("FINANCIAL SUMMARY")
print("==========================")

print(
    f"Revenue: ₹{summary['revenue']:,.2f}"
)

print(
    f"Expenses: ₹{summary['expenses']:,.2f}"
)

print(
    f"Profit: ₹{summary['profit']:,.2f}"
)

print(
    f"Profit Margin: "
    f"{summary['profit_margin']:.2f}%"
)