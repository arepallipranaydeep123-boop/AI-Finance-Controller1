
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from ai_controller import (
    generate_finance_insights,
    generate_management_summary
)

from anomaly_detection import (
    detect_anomalies,
    add_risk_reason,
    calculate_risk_score
)

from budget_analysis import (
    calculate_budget_risk
)

from financial_risk import (
    calculate_financial_risk
)

BASE_DIR = Path(__file__).resolve().parent

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Finance Controller",
    page_icon="💰",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("💰 AI Finance Controller")

st.write(
    "AI-powered financial monitoring and decision support"
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        BASE_DIR / "data" / "transactions.csv"
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["date"] = pd.to_datetime(
        df["date_time"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["amount", "date"]
    )

    return df


df = load_data()
if "description" not in df.columns:
    df["description"] = df["tags"].fillna(
        "Uncategorized transaction"
    )

anomalies_df = detect_anomalies(df)

anomalies_df = add_risk_reason(
    anomalies_df
)

anomalies_df = calculate_risk_score(
    anomalies_df
)

budget_result = calculate_budget_risk(
    df
)

st.subheader(
    "📊 Budget vs Actual Spending"
)

budget_chart = budget_result.dropna(
    subset=["budget"]
)

fig = px.bar(
    budget_chart,
    x="category",
    y=["budget", "actual"],
    barmode="group",
    title="Budget vs Actual Spending"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

financial_risk = calculate_financial_risk(
    anomalies_df,
    budget_result
)

# ==========================================
# FINANCIAL CALCULATIONS
# ==========================================

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

financial_summary = {
    "revenue": revenue,
    "expenses": expenses,
    "profit": profit,
    "profit_margin": profit_margin
}

ai_result = generate_finance_insights(
    financial_summary,
    financial_risk,
    budget_result,
    anomalies_df
)

management_summary = generate_management_summary(
    financial_summary,
    financial_risk
)

# ==========================================
# KPI CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Revenue",
    f"₹{revenue:,.0f}"
)

col2.metric(
    "💸 Total Expenses",
    f"₹{expenses:,.0f}"
)

col3.metric(
    "📈 Profit",
    f"₹{profit:,.0f}"
)

col4.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)

st.divider()

st.subheader(
    "🚨 Overall Financial Risk"
)

risk_score = financial_risk[
    "financial_risk"
]

risk_level = financial_risk[
    "risk_level"
]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Financial Risk Score",
    f"{risk_score:.1f}/100"
)

col2.metric(
    "Anomaly Risk",
    f"{financial_risk['anomaly_risk']:.1f}/100"
)

col3.metric(
    "Budget Risk",
    f"{financial_risk['budget_risk']:.1f}/100"
)

if risk_level == "High":

    st.error(
        f"🔴 HIGH FINANCIAL RISK — "
        f"{risk_score:.1f}/100"
    )

elif risk_level == "Medium":

    st.warning(
        f"🟠 MEDIUM FINANCIAL RISK — "
        f"{risk_score:.1f}/100"
    )

else:

    st.success(
        f"🟢 LOW FINANCIAL RISK — "
        f"{risk_score:.1f}/100"
    )

st.subheader(
    "🎯 Overall Financial Risk Score"
)

fig = px.pie(
    values=[
        risk_score,
        100 - risk_score
    ],
    names=[
        "Risk",
        "Remaining"
    ],
    hole=0.7
)

fig.update_layout(
    showlegend=True,
    annotations=[
        {
            "text": f"{risk_score:.0f}/100",
            "x": 0.5,
            "y": 0.5,
            "font_size": 28,
            "showarrow": False
        }
    ]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

#Revenue vs Expense chart
# ==========================================
# REVENUE VS EXPENSE
# ==========================================

st.subheader("📊 Revenue vs Expenses")

summary = pd.DataFrame({
    "Type": ["Revenue", "Expense"],
    "Amount": [revenue, expenses]
})

fig = px.bar(
    summary,
    x="Type",
    y="Amount",
    text="Amount",
    title="Revenue vs Expenses"
)

fig.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

#expense category chart
# ==========================================
# EXPENSES BY CATEGORY
# ==========================================

st.subheader("💸 Expenses by Category")

expense_data = df[
    df["type"] == "Expense"
]

category_expenses = (
    expense_data
    .groupby("category")["amount"]
    .sum()
    .reset_index()
    .sort_values(
        "amount",
        ascending=False
    )
)

fig = px.bar(
    category_expenses,
    x="category",
    y="amount",
    text="amount",
    title="Expenses by Category"
)

fig.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


#monthly financial trend

# ==========================================
# MONTHLY TREND
# ==========================================

st.subheader("📈 Monthly Financial Trend")

df["month"] = (
    df["date"]
    .dt.to_period("M")
    .astype(str)
)

monthly = (
    df.groupby(
        ["month", "type"]
    )["amount"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly,
    x="month",
    y="amount",
    color="type",
    markers=True,
    title="Monthly Revenue and Expenses"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

#transaction table
# ==========================================
# TRANSACTIONS
# ==========================================

st.subheader("📋 Transactions")

st.dataframe(
    df,
    use_container_width=True
)

#a sidebar
# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("⚙️ Finance Controller")

st.sidebar.write(
    "Filter your financial data"
)

transaction_type = st.sidebar.multiselect(
    "Transaction Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)

df = df[
    df["type"].isin(transaction_type)
]

#category filter
categories = st.sidebar.multiselect(
    "Category",
    options=sorted(
        df["category"].dropna().unique()
    ),
    default=sorted(
        df["category"].dropna().unique()
    )
)

df = df[
    df["category"].isin(categories)
]

st.sidebar.subheader("📅 Date Filter")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

start_date = st.sidebar.date_input(
    "Start Date",
    min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End Date",
    max_date,
    min_value=min_date,
    max_value=max_date
)

df = df[
    (df["date"].dt.date >= start_date)
    &
    (df["date"].dt.date <= end_date)
]

st.divider()

st.subheader("🚨 Financial Risk Detection")

high_risk = anomalies_df[
    anomalies_df["risk_level"] == "High"
]

if len(high_risk) > 0:

    st.warning(
        f"{len(high_risk)} unusual transactions detected."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🚨 High Risk Transactions",
        len(high_risk)
    )

    col2.metric(
        "💰 Risk Amount",
        f"₹{high_risk['amount'].sum():,.0f}"
    )

    if len(high_risk) > 0:
        average_score = high_risk[
            "risk_score"
        ].mean()
    else:
        average_score = 0

    col3.metric(
        "📊 Average Risk Score",
        f"{average_score:.0f}/100"
    )

    high_budget_risk = budget_result[
        budget_result["status"] == "High Risk"
    ]

    over_budget = budget_result[
        budget_result["status"] == "Over Budget"
    ]

    col1, col2 = st.columns(2)

    col1.metric(
        "🔴 High Budget Risks",
        len(high_budget_risk)
    )

    col2.metric(
        "🟠 Over Budget Categories",
        len(over_budget)
    )

    if len(high_budget_risk) > 0:

        st.error(
            "⚠️ High budget risk detected!"
        )

        for _, row in high_budget_risk.iterrows():

            st.write(
                f"🔴 **{row['category']}** is "
                f"{row['variance_percent']:.1f}% "
                f"over budget."
            )

    else:

        st.success(
            "✅ No categories are significantly "
            "over budget."
        )

    st.dataframe(
        high_risk[
            [
                "date",
                "description",
                "category",
                "amount",
                "risk_score",
                "risk_level",
                "risk_reason"
            ]
        ],
        use_container_width=True
    )

else:

    st.success(
        "No unusual transactions detected."
    )

st.divider()

st.subheader("🤖 AI Finance Controller")

st.write(
    "The controller automatically analyzes "
    "financial performance, budget variance, "
    "and transaction risk."
)

st.markdown("### 🔎 Key Insights")

for insight in ai_result["insights"]:

    st.info(
        f"💡 {insight}"
    )

st.markdown("### 🎯 Recommended Actions")

for recommendation in ai_result[
    "recommendations"
]:

    st.success(
        f"✅ {recommendation}"
    )

st.divider()

st.subheader("📋 Management Summary")

st.markdown(
    management_summary
)

st.subheader(
    "🚨 Top 5 Risky Transactions"
)

top_risky = (
    anomalies_df
    .sort_values(
        "risk_score",
        ascending=False
    )
    .head(5)
)

st.dataframe(
    top_risky[
        [
            "date",
            "category",
            "amount",
            "risk_score",
            "risk_level",
            "risk_reason"
        ]
    ],
    use_container_width=True
)

st.subheader(
    "📥 Export Financial Data"
)

csv = df.to_csv(
    index=False
)

st.download_button(
    label="Download Transactions CSV",
    data=csv,
    file_name="finance_transactions.csv",
    mime="text/csv"
)

risk_csv = top_risky.to_csv(
    index=False
)

st.download_button(
    label="Download Risk Report",
    data=risk_csv,
    file_name="financial_risk_report.csv",
    mime="text/csv"
)

