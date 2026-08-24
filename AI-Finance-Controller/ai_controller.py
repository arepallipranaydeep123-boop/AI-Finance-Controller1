def generate_finance_insights(
    financial_summary,
    risk_result,
    budget_result,
    anomaly_result
):

    insights = []
    recommendations = []

    revenue = financial_summary["revenue"]
    expenses = financial_summary["expenses"]
    profit = financial_summary["profit"]
    margin = financial_summary["profit_margin"]

    risk_score = risk_result["financial_risk"]
    risk_level = risk_result["risk_level"]

    # =====================================
    # 1. PROFIT ANALYSIS
    # =====================================

    if profit < 0:

        insights.append(
            "The business is currently operating "
            "at a loss."
        )

        recommendations.append(
            "Review major expense categories "
            "and reduce non-essential spending."
        )

    elif margin < 10:

        insights.append(
            "Profit margin is relatively low."
        )

        recommendations.append(
            "Identify opportunities to reduce "
            "operating costs and improve revenue."
        )

    else:

        insights.append(
            "The business is generating a "
            "positive operating result."
        )


    # =====================================
    # 2. BUDGET ANALYSIS
    # =====================================

    high_budget = budget_result[
        budget_result["status"] == "High Risk"
    ]

    over_budget = budget_result[
        budget_result["status"] == "Over Budget"
    ]

    if len(high_budget) > 0:

        for _, row in high_budget.iterrows():

            insights.append(
                f"{row['category']} is "
                f"{row['variance_percent']:.1f}% "
                f"over budget."
            )

            recommendations.append(
                f"Investigate {row['category']} "
                f"spending and review non-essential "
                f"expenses."
            )

    elif len(over_budget) > 0:

        insights.append(
            f"{len(over_budget)} categories "
            "are above their allocated budget."
        )

        recommendations.append(
            "Review categories that are "
            "currently over budget."
        )


    # =====================================
    # 3. ANOMALY ANALYSIS
    # =====================================

    high_anomalies = anomaly_result[
        anomaly_result["risk_level"] == "High"
    ]

    if len(high_anomalies) > 0:

        insights.append(
            f"{len(high_anomalies)} unusual "
            "expense transactions were detected."
        )

        recommendations.append(
            "Review high-value transactions "
            "for approval, duplication, or "
            "unexpected spending."
        )

    else:

        insights.append(
            "No significant transaction anomalies "
            "were detected."
        )


    # =====================================
    # 4. OVERALL RISK
    # =====================================

    if risk_level == "High":

        insights.append(
            f"Overall financial risk is HIGH "
            f"at {risk_score:.1f}/100."
        )

        recommendations.append(
            "Management should prioritize "
            "financial risk review immediately."
        )

    elif risk_level == "Medium":

        insights.append(
            f"Overall financial risk is MEDIUM "
            f"at {risk_score:.1f}/100."
        )

        recommendations.append(
            "Management should monitor spending "
            "and budget variance closely."
        )

    else:

        insights.append(
            f"Overall financial risk is LOW "
            f"at {risk_score:.1f}/100."
        )

        recommendations.append(
            "Continue monitoring financial "
            "performance regularly."
        )


    return {
        "insights": insights,
        "recommendations": recommendations
    }


def generate_management_summary(
    financial_summary,
    risk_result
):

    revenue = financial_summary["revenue"]
    expenses = financial_summary["expenses"]
    profit = financial_summary["profit"]
    margin = financial_summary["profit_margin"]

    risk_score = risk_result["financial_risk"]
    risk_level = risk_result["risk_level"]

    summary = f"""
### Management Financial Summary

**Revenue:** ₹{revenue:,.0f}

**Expenses:** ₹{expenses:,.0f}

**Profit:** ₹{profit:,.0f}

**Profit Margin:** {margin:.2f}%

**Financial Risk:** {risk_score:.1f}/100

**Risk Level:** {risk_level}

The Finance Controller has analyzed revenue,
expenses, profitability, transaction anomalies,
and budget performance to identify potential
financial risks and recommended actions.
"""

    return summary