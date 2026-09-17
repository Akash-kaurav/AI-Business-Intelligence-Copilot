import pandas as pd
import numpy as np
import re

from src import data_quality_engine


# ============================================================
# CATEGORY / PRODUCT / SELLER INSIGHTS
# ============================================================

def get_top_categories(category_kpi, n=5):
    """
    Return top product categories by revenue.
    """

    if category_kpi is None or category_kpi.empty:
        return "Category data not available."

    required_columns = [
        "product_category_name",
        "revenue"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in category_kpi.columns
    ]

    if missing_columns:
        return (
            "Category data is missing required columns: "
            + ", ".join(missing_columns)
        )

    top_categories = (
        category_kpi
        .sort_values("revenue", ascending=False)
        .head(n)
    )

    response = "🏆 Top Categories by Revenue\n\n"

    for i, (_, row) in enumerate(top_categories.iterrows(), start=1):

        category = row["product_category_name"]
        revenue = row["revenue"]

        response += (
            f"#{i} {category}\n"
            f"   Revenue: {revenue:,.2f} BRL\n\n"
        )

    return response


def get_customer_segments(customer_summary):
    """
    Summarize customer segments.
    """

    if customer_summary is None or customer_summary.empty:
        return "Customer segment data not available."

    required_columns = [
        "customer_segment",
        "total_customers",
        "total_revenue",
        "average_revenue"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in customer_summary.columns
    ]

    if missing_columns:
        return (
            "Customer segment data is missing required columns: "
            + ", ".join(missing_columns)
        )

    response = "👥 Customer Segment Analysis\n\n"

    for _, row in customer_summary.iterrows():

        response += (
            f"{row['customer_segment']}\n"
            f"Customers: {int(row['total_customers']):,}\n"
            f"Revenue: {row['total_revenue']:,.2f} BRL\n"
            f"Average Revenue: {row['average_revenue']:,.2f} BRL\n\n"
        )

    return response


def get_top_products(product_sales_category, n=5):
    """
    Return top products by revenue.
    """

    if product_sales_category is None or product_sales_category.empty:
        return "Product data not available."

    required_columns = [
        "product_id",
        "product_category_name",
        "total_revenue",
        "total_units",
        "avg_price"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in product_sales_category.columns
    ]

    if missing_columns:
        return (
            "Product data is missing required columns: "
            + ", ".join(missing_columns)
        )

    top_products = (
        product_sales_category
        .sort_values("total_revenue", ascending=False)
        .head(n)
    )

    response = "🏆 Top Products by Revenue\n\n"

    for i, (_, row) in enumerate(top_products.iterrows(), start=1):

        response += (
            f"#{i} Product: {row['product_id']}\n"
            f"   Category: {row['product_category_name']}\n"
            f"   Revenue: {row['total_revenue']:,.2f} BRL\n"
            f"   Units Sold: {int(row['total_units'])}\n"
            f"   Average Price: {row['avg_price']:,.2f} BRL\n\n"
        )

    return response


def get_risky_sellers(risk_sellers, n=10):
    """
    Return sellers with the highest late delivery rates.
    """

    if risk_sellers is None or risk_sellers.empty:
        return "No risky sellers found."

    required_columns = [
        "seller_id",
        "total_revenue",
        "late_rate",
        "delivered_orders"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in risk_sellers.columns
    ]

    if missing_columns:
        return (
            "Seller risk data is missing required columns: "
            + ", ".join(missing_columns)
        )

    risky = (
        risk_sellers
        .sort_values(
            ["late_rate", "total_revenue"],
            ascending=[False, False]
        )
        .head(n)
    )

    response = "⚠️ Risky Sellers\n\n"

    for i, (_, row) in enumerate(risky.iterrows(), start=1):

        response += (
            f"#{i} Seller: {row['seller_id']}\n"
            f"   Revenue: {row['total_revenue']:,.2f} BRL\n"
            f"   Late Rate: {row['late_rate']:.2f}%\n"
            f"   Delivered Orders: {int(row['delivered_orders'])}\n\n"
        )

    return response


# ============================================================
# REVENUE DIAGNOSIS
# ============================================================

def generate_revenue_diagnosis(
    month,
    monthly_business,
    monthly_customer
):
    """
    Generate a basic revenue diagnosis for a selected month.
    """

    if monthly_business is None or monthly_business.empty:
        return "Business data not available."

    if monthly_customer is None or monthly_customer.empty:
        return "Customer data not available."

    business_row = monthly_business[
        monthly_business["month"] == pd.to_datetime(month + "-01")
    ]

    customer_row = monthly_customer[
        monthly_customer["month"] == month
    ]

    if business_row.empty:
        return f"No business data available for {month}."

    row = business_row.iloc[0]

    revenue_growth = row.get("revenue_growth_pct", np.nan)

    if pd.isna(revenue_growth):
        return "Not enough historical data to diagnose revenue."

    explanation = (
        f"Revenue changed by {revenue_growth:.2f}% in {month}."
    )

    if not customer_row.empty:

        customer_data = customer_row.iloc[0]

        customer_growth = customer_data.get(
            "customer_growth_pct",
            np.nan
        )

        rpc_growth = customer_data.get(
            "revenue_per_customer_growth_pct",
            np.nan
        )

        if not pd.isna(customer_growth):
            explanation += (
                f" Customer count changed by "
                f"{customer_growth:.2f}%."
            )

        if not pd.isna(rpc_growth):
            explanation += (
                f" Revenue per customer changed by "
                f"{rpc_growth:.2f}%."
            )

    return explanation


def get_declining_categories(
    month,
    monthly_category,
    n=3
):
    """
    Return categories contributing to revenue decline.
    """

    if monthly_category is None or monthly_category.empty:
        return []

    data = monthly_category[
        monthly_category["month"] == month
    ].copy()

    if data.empty:
        return []

    if "revenue_growth" in data.columns:
        growth_column = "revenue_growth"
    elif "revenue_growth_pct" in data.columns:
        growth_column = "revenue_growth_pct"
    else:
        return []

    declining = data[
        data[growth_column] < 0
    ].sort_values(
        growth_column,
        ascending=True
    ).head(n)

    return declining["product_category_name"].tolist()


def generate_full_revenue_diagnosis(
    month,
    monthly_business,
    monthly_customer,
    monthly_category
):
    """
    Generate detailed revenue diagnosis including
    customer metrics and declining categories.
    """

    if monthly_business is None or monthly_business.empty:
        return "Business data not available."

    if monthly_customer is None or monthly_customer.empty:
        return "Customer data not available."

    business_row = monthly_business[
        monthly_business["month"] == pd.to_datetime(month + "-01")
    ]

    customer_row = monthly_customer[
        monthly_customer["month"] == month
    ]

    if business_row.empty:
        return f"No business data available for {month}."

    row = business_row.iloc[0]

    revenue_growth = row.get(
        "revenue_growth_pct",
        np.nan
    )

    if pd.isna(revenue_growth):
        return "Not enough historical data."

    diagnosis = (
        f"Revenue changed by {revenue_growth:.2f}% "
        f"in {month}."
    )

    if not customer_row.empty:

        customer_data = customer_row.iloc[0]

        customer_growth = customer_data.get(
            "customer_growth_pct",
            np.nan
        )

        rpc_growth = customer_data.get(
            "revenue_per_customer_growth_pct",
            np.nan
        )

        if not pd.isna(customer_growth):
            diagnosis += (
                f" Customer count changed by "
                f"{customer_growth:.2f}%."
            )

        if not pd.isna(rpc_growth):
            diagnosis += (
                f" Revenue per customer changed by "
                f"{rpc_growth:.2f}%."
            )

    declining_categories = get_declining_categories(
        month,
        monthly_category,
        n=3
    )

    if declining_categories:

        diagnosis += (
            " The main category decline contributors were "
            + ", ".join(declining_categories)
            + "."
        )

    return diagnosis


# ============================================================
# BUSINESS RECOMMENDATION
# ============================================================

def generate_business_recommendation(
    month,
    monthly_business,
    monthly_customer
):
    """
    Generate business recommendations for a month.
    """

    if monthly_customer is None or monthly_customer.empty:
        return "Customer data not available."

    if monthly_business is None or monthly_business.empty:
        return "Business data not available."

    customer_row = monthly_customer[
        monthly_customer["month"] == month
    ]

    business_row = monthly_business[
        monthly_business["month"] ==
        pd.to_datetime(month + "-01")
    ]

    if customer_row.empty or business_row.empty:
        return "Data not available."

    customer_data = customer_row.iloc[0]
    business_data = business_row.iloc[0]

    customer_growth = customer_data.get(
        "customer_growth_pct",
        np.nan
    )

    rpc_growth = customer_data.get(
        "revenue_per_customer_growth_pct",
        np.nan
    )

    revenue_growth = business_data.get(
        "revenue_growth_pct",
        np.nan
    )

    recommendations = []

    if not pd.isna(revenue_growth):

        if revenue_growth < -10:

            recommendations.append(
                "Investigate the main causes of the revenue decline."
            )

        if customer_growth < -5:

            recommendations.append(
                "Focus on customer acquisition and retention."
            )

        if rpc_growth < -5:

            recommendations.append(
                "Review product mix, pricing, and cross-selling "
                "opportunities to improve revenue per customer."
            )

        if revenue_growth > 10:

            recommendations.append(
                "Identify the products and categories driving growth "
                "and consider increasing their availability."
            )

    if not recommendations:

        recommendations.append(
            "Continue monitoring performance and identify "
            "emerging trends."
        )

    return " ".join(recommendations)


def generate_copilot_business_response(
    month,
    monthly_business,
    monthly_customer,
    monthly_category
):
    """
    Generate combined business diagnosis and recommendation.
    """

    diagnosis = generate_full_revenue_diagnosis(
        month,
        monthly_business,
        monthly_customer,
        monthly_category
    )

    recommendation = generate_business_recommendation(
        month,
        monthly_business,
        monthly_customer
    )

    return (
        f"📊 Business Diagnosis — {month}\n\n"
        f"{diagnosis}\n\n"
        f"💡 Recommended Actions\n\n"
        f"{recommendation}"
    )


# ============================================================
# MONTH EXTRACTION
# ============================================================

def extract_month(question):
    """
    Extract YYYY-MM, YYYY/MM or Month YYYY from a question.
    """

    if not question:
        return None

    question = question.lower().strip()

    # YYYY-MM
    match = re.search(
        r"\b(20\d{2})[-/](0?[1-9]|1[0-2])\b",
        question
    )

    if match:

        year = match.group(1)
        month = int(match.group(2))

        return f"{year}-{month:02d}"

    # Month YYYY
    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }

    for month_name, month_number in months.items():

        pattern = rf"\b{month_name}\s+(20\d{{2}})\b"

        match = re.search(pattern, question)

        if match:

            year = match.group(1)

            return f"{year}-{month_number:02d}"

    return None


# ============================================================
# CUSTOMER SEGMENT INSIGHTS
# ============================================================

def generate_customer_segment_insight(
    customer_summary,
    segment
):
    """
    Generate insight for a customer segment.
    """

    if customer_summary is None or customer_summary.empty:
        return "Customer segment data not available."

    data = customer_summary[
        customer_summary["customer_segment"].str.lower()
        == segment.lower()
    ]

    if data.empty:
        return f"No data available for {segment} customers."

    row = data.iloc[0]

    return (
        f"{segment} Customers\n\n"
        f"Customers: {int(row['total_customers']):,}\n"
        f"Total Revenue: {row['total_revenue']:,.2f} BRL\n"
        f"Average Revenue per Customer: "
        f"{row['average_revenue']:,.2f} BRL"
    )


def get_customer_attention_insight(customer_rfm):
    """
    Show customer retention risk counts.
    """

    if customer_rfm is None or customer_rfm.empty:
        return "Customer RFM data not available."

    at_risk_count = (
        customer_rfm["customer_segment"]
        .eq("At Risk")
        .sum()
    )

    lost_count = (
        customer_rfm["customer_segment"]
        .eq("Lost")
        .sum()
    )

    retention_count = at_risk_count + lost_count

    retention_data = customer_rfm[
        customer_rfm["customer_segment"].isin(
            ["At Risk", "Lost"]
        )
    ]

    revenue = retention_data["monetary"].sum()

    average_revenue = (
        revenue / retention_count
        if retention_count > 0
        else 0
    )

    average_orders = (
        retention_data["frequency"].mean()
        if not retention_data.empty
        else 0
    )

    return (
        "Customer Retention Risk\n\n"
        f"Retention-Risk Customers: {retention_count:,}\n"
        f"At Risk Customers: {at_risk_count:,}\n"
        f"Lost Customers: {lost_count:,}\n"
        f"Associated Revenue: {revenue:,.2f} BRL\n"
        f"Average Revenue per Customer: "
        f"{average_revenue:,.2f} BRL\n"
        f"Average Orders per Customer: "
        f"{average_orders:.2f}\n\n"
        "Priority: Focus on At Risk customers first, "
        "then launch win-back campaigns for Lost customers."
    )


def extract_number(question, default=10):
    """
    Extract first positive integer from a question.
    """

    if not question:
        return default

    match = re.search(
        r"\b\d+\b",
        str(question)
    )

    if match:

        number = int(match.group())

        if number > 0:
            return number

    return default


# ============================================================
# VIP CUSTOMER INSIGHT
# ============================================================

def get_vip_customer_insight(
    customer_rfm,
    n=10
):
    """
    Show high-value VIP customers.
    """

    if customer_rfm is None or customer_rfm.empty:
        return "Customer RFM data not available."

    vip = customer_rfm[
        customer_rfm["customer_segment"] == "VIP"
    ].copy()

    if vip.empty:
        return "No VIP customers found."

    vip = vip.sort_values(
        "monetary",
        ascending=False
    ).head(n)

    response = ""

    for i, (_, row) in enumerate(
        vip.iterrows(),
        start=1
    ):

        response += (
            f"#{i} Customer: "
            f"{row['customer_unique_id']}\n"
            f"   Revenue: {row['monetary']:,.2f} BRL\n"
            f"   Orders: {int(row['frequency'])}\n"
            f"   Recency: {int(row['recency'])} days\n\n"
        )

    return response


# ============================================================
# AT-RISK CUSTOMER INSIGHT
# ============================================================

def get_at_risk_customer_insight(
    customer_rfm,
    n=10
):
    """
    Show customers currently classified as At Risk.
    """

    if customer_rfm is None or customer_rfm.empty:
        return "Customer RFM data not available."

    at_risk = customer_rfm[
        customer_rfm["customer_segment"] == "At Risk"
    ].copy()

    if at_risk.empty:
        return "No At Risk customers found."

    at_risk = at_risk.sort_values(
        ["monetary", "recency"],
        ascending=[False, False]
    ).head(n)

    response = ""

    for i, (_, row) in enumerate(
        at_risk.iterrows(),
        start=1
    ):

        response += (
            f"#{i} Customer: "
            f"{row['customer_unique_id']}\n"
            f"   Revenue: {row['monetary']:,.2f} BRL\n"
            f"   Orders: {int(row['frequency'])}\n"
            f"   Recency: {int(row['recency'])} days\n\n"
        )

    return response


# ============================================================
# RETENTION INSIGHT
# ============================================================

def get_customer_retention_insight(
    customer_rfm
):
    """
    Summarize retention-risk customers.
    """

    if customer_rfm is None or customer_rfm.empty:
        return "Customer RFM data not available."

    retention = customer_rfm[
        customer_rfm["customer_segment"].isin(
            ["At Risk", "Lost"]
        )
    ].copy()

    if retention.empty:
        return "No retention-risk customers found."

    at_risk = (
        retention["customer_segment"]
        .eq("At Risk")
        .sum()
    )

    lost = (
        retention["customer_segment"]
        .eq("Lost")
        .sum()
    )

    total_revenue = retention["monetary"].sum()

    average_revenue = (
        retention["monetary"].mean()
    )

    average_orders = (
        retention["frequency"].mean()
    )

    return (
        "Customer Retention Risk\n\n"
        f"Retention-Risk Customers: {len(retention):,}\n"
        f"At Risk Customers: {at_risk:,}\n"
        f"Lost Customers: {lost:,}\n"
        f"Associated Revenue: {total_revenue:,.2f} BRL\n"
        f"Average Revenue per Customer: "
        f"{average_revenue:,.2f} BRL\n"
        f"Average Orders per Customer: "
        f"{average_orders:.2f}\n\n"
        "Priority: Focus on At Risk customers first, "
        "then launch win-back campaigns for Lost customers."
    )


# ============================================================
# CUSTOMER PRIORITY — V3
# ============================================================

def get_customer_priority_insight(
    customer_rfm,
    n=10
):
    """
    Identify customers that should receive retention attention first.

    Priority model:

        Revenue Value       -> 35%
        Order Frequency     -> 25%
        Recency Risk        -> 25%
        Segment Risk        -> 15%

    Important:
    - Frequency score is based on actual order frequency.
    - A one-order customer is NOT treated as a repeat customer.
    - Percentile ranking is not used for frequency because
      thousands of customers have exactly one order.
    """

    if customer_rfm is None or customer_rfm.empty:
        return "Customer RFM data not available."

    required_columns = [
        "customer_unique_id",
        "customer_segment",
        "monetary",
        "frequency",
        "recency"
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in customer_rfm.columns
    ]

    if missing_columns:
        return (
            "Customer RFM data is missing required columns: "
            + ", ".join(missing_columns)
        )

    data = customer_rfm.copy()

    # --------------------------------------------------------
    # Only customers requiring retention attention
    # --------------------------------------------------------

    retention_customers = data[
        data["customer_segment"].isin(
            ["At Risk", "Lost"]
        )
    ].copy()

    if retention_customers.empty:
        return "No customers currently require retention attention."

    # --------------------------------------------------------
    # Clean numeric values
    # --------------------------------------------------------

    retention_customers["monetary"] = pd.to_numeric(
        retention_customers["monetary"],
        errors="coerce"
    ).fillna(0)

    retention_customers["frequency"] = pd.to_numeric(
        retention_customers["frequency"],
        errors="coerce"
    ).fillna(0)

    retention_customers["recency"] = pd.to_numeric(
        retention_customers["recency"],
        errors="coerce"
    ).fillna(0)

    # --------------------------------------------------------
    # 1. Revenue / Customer Value Score
    #
    # Percentile ranking works well here because revenue
    # varies significantly between customers.
    # --------------------------------------------------------

    if len(retention_customers) > 1:

        retention_customers["revenue_score"] = (
            retention_customers["monetary"]
            .rank(pct=True)
            * 100
        )

    else:

        retention_customers["revenue_score"] = 100.0

    # --------------------------------------------------------
    # 2. Frequency Score
    #
    # DO NOT use percentile rank.
    #
    # Most Olist customers have one order, so percentile
    # ranking would incorrectly make many one-order customers
    # look like high-frequency customers.
    #
    # Log normalization gives:
    #
    # 1 order  -> 0
    # 2 orders -> higher
    # 3 orders -> higher
    # 4+       -> progressively higher
    # --------------------------------------------------------

    max_frequency = retention_customers["frequency"].max()

    if max_frequency <= 1:

        retention_customers["frequency_score"] = 0.0

    else:

        retention_customers["frequency_score"] = (
            np.log1p(
                retention_customers["frequency"]
            )
            / np.log1p(max_frequency)
        ) * 100

    # --------------------------------------------------------
    # 3. Recency Risk Score
    #
    # Higher number of inactive days = higher risk.
    # --------------------------------------------------------

    if len(retention_customers) > 1:

        retention_customers["recency_risk_score"] = (
            retention_customers["recency"]
            .rank(pct=True)
            * 100
        )

    else:

        retention_customers["recency_risk_score"] = 100.0

    # --------------------------------------------------------
    # 4. Segment Risk Score
    #
    # At Risk is more actionable for retention.
    # Lost is still important but requires win-back.
    # --------------------------------------------------------

    retention_customers["segment_score"] = (
        retention_customers["customer_segment"]
        .map({
            "At Risk": 100,
            "Lost": 70
        })
        .fillna(50)
    )

    # --------------------------------------------------------
    # Final Priority Score
    # --------------------------------------------------------

    retention_customers["priority_score"] = (
        retention_customers["revenue_score"] * 0.35
        + retention_customers["frequency_score"] * 0.25
        + retention_customers["recency_risk_score"] * 0.25
        + retention_customers["segment_score"] * 0.15
    )

    # --------------------------------------------------------
    # Priority Level
    # --------------------------------------------------------

    def priority_level(score):

        if score >= 75:
            return "Critical Priority"

        elif score >= 60:
            return "High Priority"

        elif score >= 45:
            return "Medium Priority"

        else:
            return "Low Priority"

    retention_customers["priority_level"] = (
        retention_customers["priority_score"]
        .apply(priority_level)
    )

    # --------------------------------------------------------
    # Priority Reason
    # --------------------------------------------------------

    def generate_priority_reason(row):

        revenue = row["monetary"]
        frequency = row["frequency"]
        recency = row["recency"]
        segment = row["customer_segment"]

        max_revenue = retention_customers["monetary"].max()
        max_recency = retention_customers["recency"].max()

        high_value = (
            revenue >=
            retention_customers["monetary"].quantile(0.75)
        )

        long_inactive = (
            recency >=
            retention_customers["recency"].quantile(0.75)
        )

        repeat_customer = frequency > 1

        if repeat_customer and high_value and long_inactive:

            return (
                "Repeat customer with high historical value "
                "and long inactivity period."
            )

        elif high_value and long_inactive:

            return (
                "High-value customer with a long inactivity "
                "period."
            )

        elif repeat_customer and long_inactive:

            return (
                "Repeat customer with a long inactivity period "
                "and retention risk."
            )

        elif high_value:

            return (
                "High historical customer value makes retention "
                "worth prioritizing."
            )

        elif long_inactive:

            return (
                "Long inactivity period indicates elevated "
                "retention risk."
            )

        elif repeat_customer:

            return (
                "Repeat customer with demonstrated purchase "
                "history and retention risk."
            )

        elif segment == "At Risk":

            return (
                "At Risk customer requiring proactive retention "
                "attention."
            )

        else:

            return (
                "Lost customer suitable for a targeted "
                "win-back campaign."
            )

    retention_customers["priority_reason"] = (
        retention_customers
        .apply(generate_priority_reason, axis=1)
    )

    # --------------------------------------------------------
    # Recommended Action
    # --------------------------------------------------------

    def generate_action(row):

        segment = row["customer_segment"]
        frequency = row["frequency"]
        score = row["priority_score"]
        revenue = row["monetary"]

        if score >= 75:

            if segment == "At Risk":

                if frequency > 1:

                    return (
                        "Immediately launch a personalized "
                        "retention campaign for this repeat customer."
                    )

                elif revenue >= retention_customers[
                    "monetary"
                ].quantile(0.75):

                    return (
                        "Immediately launch a targeted retention "
                        "campaign with personalized offers."
                    )

                else:

                    return (
                        "Launch a targeted retention campaign "
                        "and test a personalized incentive."
                    )

            else:

                return (
                    "Launch a targeted win-back campaign with "
                    "personalized offers."
                )

        elif score >= 60:

            if segment == "At Risk":

                return (
                    "Prioritize for targeted retention outreach."
                )

            return (
                "Include in a targeted win-back campaign."
            )

        elif score >= 45:

            return (
                "Monitor engagement and include in retention "
                "campaigns when appropriate."
            )

        else:

            return (
                "Monitor customer activity and consider "
                "low-cost re-engagement."
            )

    retention_customers["action"] = (
        retention_customers
        .apply(generate_action, axis=1)
    )

    # --------------------------------------------------------
    # Sort customers
    # --------------------------------------------------------

    retention_customers = retention_customers.sort_values(
        [
            "priority_score",
            "monetary",
            "frequency",
            "recency"
        ],
        ascending=[
            False,
            False,
            False,
            False
        ]
    ).head(n)

    # --------------------------------------------------------
    # Final Response
    # --------------------------------------------------------

    response = ""

    for i, (_, row) in enumerate(
        retention_customers.iterrows(),
        start=1
    ):

        response += (
            f"#{i} Customer: "
            f"{row['customer_unique_id']}\n"
            f"   Segment: {row['customer_segment']}\n"
            f"   Priority Level: {row['priority_level']}\n"
            f"   Revenue: {row['monetary']:,.2f} BRL\n"
            f"   Orders: {int(row['frequency'])}\n"
            f"   Recency: {int(row['recency'])} days\n"
            f"   Revenue Score: {row['revenue_score']:.2f}\n"
            f"   Frequency Score: {row['frequency_score']:.2f}\n"
            f"   Recency Risk Score: "
            f"{row['recency_risk_score']:.2f}\n"
            f"   Segment Score: {row['segment_score']:.2f}\n"
            f"   Priority Score: {row['priority_score']:.2f}\n"
            f"   Priority Reason: {row['priority_reason']}\n"
            f"   Action: {row['action']}\n\n"
        )

    return response


# ============================================================
# DATA QUALITY COPILOT
# ============================================================

def generate_data_quality_copilot_response(
    quality_report
):
    """
    Generate overall data-quality business interpretation.
    """

    if quality_report is None or quality_report.empty:
        return "Data quality report not available."

    status = data_quality_engine.get_overall_data_quality_status(
        quality_report
    )

    insight = data_quality_engine.generate_data_quality_insight(
        quality_report
    )

    return (
        f"🔎 Data Quality Status: {status}\n\n"
        f"{insight}"
    )


def generate_column_quality_copilot_response(
    quality_report,
    dataset,
    column
):
    """
    Generate column-level data quality insight.
    """

    if quality_report is None or quality_report.empty:
        return "Data quality report not available."

    result = data_quality_engine.get_column_quality_report(
        quality_report,
        dataset,
        column
    )

    return result


def generate_master_quality_copilot_response(
    master_quality_report
):
    """
    Generate master data quality report interpretation.
    """

    if (
        master_quality_report is None
        or master_quality_report.empty
    ):
        return "Master quality report not available."

    status = data_quality_engine.get_overall_data_quality_status(
        master_quality_report
    )

    insight = data_quality_engine.generate_data_quality_insight(
        master_quality_report
    )

    return (
        f"🔎 Master Data Quality Status: {status}\n\n"
        f"{insight}"
    )


# ============================================================
# PRODUCT BUSINESS INTELLIGENCE
# ============================================================

def get_business_winner_products(
    product_sales,
    n=10
):
    """
    Return products classified as Business Winner.
    """

    if product_sales is None or product_sales.empty:
        return "Product sales data not available."

    if "product_segment" not in product_sales.columns:
        return (
            "Product segment information is not available."
        )

    winners = product_sales[
        product_sales["product_segment"]
        == "Business Winner"
    ].copy()

    if winners.empty:
        return "No Business Winner products found."

    winners = winners.sort_values(
        "total_revenue",
        ascending=False
    ).head(n)

    response = "🏆 Business Winner Products\n\n"

    for i, (_, row) in enumerate(
        winners.iterrows(),
        start=1
    ):

        response += (
            f"#{i} Product: {row['product_id']}\n"
            f"   Revenue: {row['total_revenue']:,.2f} BRL\n"
            f"   Units Sold: {int(row['total_units'])}\n"
            f"   Average Price: {row['avg_price']:,.2f} BRL\n"
            f"   Segment: {row['product_segment']}\n\n"
        )

    return response


def analyze_product_performance(
    product_sales
):
    """
    Analyze product performance segments
    and return detailed products for each segment.
    """

    if product_sales is None or product_sales.empty:
        return "Product sales data not available."

    required_columns = [
        "product_id",
        "product_segment",
        "total_revenue",
        "total_units",
        "avg_price"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in product_sales.columns
    ]

    if missing_columns:
        return (
            "Product performance analysis is missing "
            "required columns: "
            + ", ".join(missing_columns)
        )

    data = product_sales.copy()

    data["total_revenue"] = pd.to_numeric(
        data["total_revenue"],
        errors="coerce"
    ).fillna(0)

    data["total_units"] = pd.to_numeric(
        data["total_units"],
        errors="coerce"
    ).fillna(0)

    data["avg_price"] = pd.to_numeric(
        data["avg_price"],
        errors="coerce"
    ).fillna(0)

    # --------------------------------------------------
    # SEGMENT SUMMARY
    # --------------------------------------------------

    summary = (
        data
        .groupby("product_segment")
        .agg(
            product_count=("product_id", "count"),
            total_revenue=("total_revenue", "sum"),
            total_units=("total_units", "sum")
        )
        .reset_index()
        .sort_values(
            "total_revenue",
            ascending=False
        )
    )

    response = "📦 Product Performance Analysis\n\n"

    for _, row in summary.iterrows():

        response += (
            f"{row['product_segment']}\n"
            f"Products: {int(row['product_count']):,}\n"
            f"Revenue: {row['total_revenue']:,.2f} BRL\n"
            f"Units Sold: {int(row['total_units']):,}\n\n"
        )

    # --------------------------------------------------
    # BUSINESS WINNERS
    # --------------------------------------------------

    business_winners = (
        data[
            data["product_segment"]
            == "Business Winner"
        ]
        .sort_values(
            "total_revenue",
            ascending=False
        )
        .head(10)
    )

    if not business_winners.empty:

        response += (
            "🏆 Top Business Winner Products\n\n"
        )

        for i, (_, row) in enumerate(
            business_winners.iterrows(),
            start=1
        ):

            response += (
                f"{i}. {row['product_id']}\n"
                f"Revenue: "
                f"{row['total_revenue']:,.2f} BRL\n"
                f"Units Sold: "
                f"{int(row['total_units']):,}\n"
                f"Average Price: "
                f"{row['avg_price']:,.2f} BRL\n\n"
            )

    # --------------------------------------------------
    # HIGH DEMAND - LOW VALUE
    # --------------------------------------------------

    high_demand_low_value = (
        data[
            data["product_segment"]
            == "High Demand - Low Value"
        ]
        .sort_values(
            "total_units",
            ascending=False
        )
        .head(10)
    )

    if not high_demand_low_value.empty:

        response += (
            "📈 Top High Demand - Low Value Products\n\n"
        )

        for i, (_, row) in enumerate(
            high_demand_low_value.iterrows(),
            start=1
        ):

            response += (
                f"{i}. {row['product_id']}\n"
                f"Revenue: "
                f"{row['total_revenue']:,.2f} BRL\n"
                f"Units Sold: "
                f"{int(row['total_units']):,}\n"
                f"Average Price: "
                f"{row['avg_price']:,.2f} BRL\n\n"
            )

    # --------------------------------------------------
    # PREMIUM PRODUCTS
    # --------------------------------------------------

    premium_products = (
        data[
            data["product_segment"]
            == "Premium Product"
        ]
        .sort_values(
            "total_revenue",
            ascending=False
        )
        .head(10)
    )

    if not premium_products.empty:

        response += (
            "💎 Top Premium Products\n\n"
        )

        for i, (_, row) in enumerate(
            premium_products.iterrows(),
            start=1
        ):

            response += (
                f"{i}. {row['product_id']}\n"
                f"Revenue: "
                f"{row['total_revenue']:,.2f} BRL\n"
                f"Units Sold: "
                f"{int(row['total_units']):,}\n"
                f"Average Price: "
                f"{row['avg_price']:,.2f} BRL\n\n"
            )

    return response

# ============================================================
# REVENUE FORECASTING
# ============================================================

def predict_next_day_revenue(daily_sales):
    """
    Predict next-day revenue using the trained
    Random Forest forecasting model.
    """

    if daily_sales is None or daily_sales.empty:
        return "Daily sales data not available."

    required_columns = [
        "date",
        "revenue",
        "units",
        "orders",
        "previous_day_revenue",
        "previous_day_units",
        "previous_day_orders",
        "previous_week_revenue",
        "previous_week_units",
        "previous_week_orders",
        "rolling_7d_revenue",
        "rolling_7d_units",
        "rolling_7d_orders",
        "day_of_week",
        "month",
        "year",
        "is_weekend"
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in daily_sales.columns
    ]

    if missing_columns:
        return (
            "Daily sales data is missing required columns: "
            + ", ".join(missing_columns)
        )

    try:
        import joblib
        from pathlib import Path

        # ----------------------------------------------------
        # Model path
        # ----------------------------------------------------

        project_root = Path(__file__).resolve().parent.parent

        model_path = (
            project_root
            / "models"
            / "daily_revenue_forecast_model.pkl"
        )

        if not model_path.exists():
            return (
                "Revenue forecasting model not found at: "
                f"{model_path}"
            )

        # ----------------------------------------------------
        # Load trained model
        # ----------------------------------------------------

        forecast_model = joblib.load(model_path)

        # ----------------------------------------------------
        # Feature columns
        # ----------------------------------------------------

        feature_columns = [
            "revenue",
            "units",
            "orders",
            "previous_day_revenue",
            "previous_day_units",
            "previous_day_orders",
            "previous_week_revenue",
            "previous_week_units",
            "previous_week_orders",
            "rolling_7d_revenue",
            "rolling_7d_units",
            "rolling_7d_orders",
            "day_of_week",
            "month",
            "year",
            "is_weekend"
        ]

        # ----------------------------------------------------
        # Use the latest complete row
        # ----------------------------------------------------

        forecast_data = (
            daily_sales
            .dropna(subset=feature_columns)
            .sort_values("date")
        )

        if forecast_data.empty:
            return (
                "Not enough data available for revenue forecasting."
            )

        latest = forecast_data.iloc[-1]

        # ----------------------------------------------------
        # Create model input
        # ----------------------------------------------------

        X_latest = pd.DataFrame(
            [[latest[column] for column in feature_columns]],
            columns=feature_columns
        )

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        prediction = forecast_model.predict(
            X_latest
        )[0]

        prediction = max(float(prediction), 0)

        next_date = (
            pd.to_datetime(latest["date"])
            + pd.Timedelta(days=1)
        )

        # ----------------------------------------------------
        # Business response
        # ----------------------------------------------------

        return (
            "🔮 Next-Day Revenue Forecast\n\n"
            f"Forecast Date: "
            f"{next_date.strftime('%Y-%m-%d')}\n"
            f"Predicted Revenue: "
            f"{prediction:,.2f} BRL\n\n"
            "Model: Random Forest Regressor"
        )

    except Exception as e:

        return (
            "❌ Revenue forecasting failed.\n\n"
            f"Error: {str(e)}"
        )
    # ============================================================
# REVENUE FORECAST MODEL EVALUATION
# ============================================================

def get_revenue_forecast_model_evaluation():
    """
    Returns the evaluation metrics of the trained
    Random Forest revenue forecasting model.
    """

    model_name = "Random Forest Regressor"

    baseline_mae = 6554.08
    baseline_rmse = 8299.86

    model_mae = 5330.03
    model_rmse = 7317.85
    model_mape = 27.91

    mae_improvement = (
        (baseline_mae - model_mae)
        / baseline_mae
    ) * 100

    rmse_improvement = (
        (baseline_rmse - model_rmse)
        / baseline_rmse
    ) * 100

    return f"""
Revenue Forecast Model Evaluation

Model: {model_name}

MAE: {model_mae:,.2f} BRL
RMSE: {model_rmse:,.2f} BRL
MAPE: {model_mape:.2f}%

Baseline MAE: {baseline_mae:,.2f} BRL
Baseline RMSE: {baseline_rmse:,.2f} BRL

MAE Improvement vs Baseline:
{mae_improvement:.2f}%

RMSE Improvement vs Baseline:
{rmse_improvement:.2f}%

Interpretation:
The Random Forest model achieved lower MAE and RMSE
than the baseline model.

However, MAPE was higher than the baseline, so the model
should not be described as universally more accurate.
MAE and RMSE are more useful primary metrics for this
forecasting task because very low revenue days can make
percentage-based errors unstable.
"""
# ============================================================
# DATA QUALITY BUSINESS INTELLIGENCE
# ============================================================

def get_data_quality_summary(master_quality_report):
    """
    Generate a business-friendly summary of data quality findings.
    """

    if (
        master_quality_report is None
        or master_quality_report.empty
    ):
        return "Master data quality report not available."

    required_columns = [
        "dataset",
        "check_type",
        "check_name",
        "issue_count",
        "status"
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in master_quality_report.columns
    ]

    if missing_columns:
        return (
            "Master quality report is missing required columns: "
            + ", ".join(missing_columns)
        )

    report = master_quality_report.copy()

    report["issue_count"] = pd.to_numeric(
        report["issue_count"],
        errors="coerce"
    ).fillna(0)

    total_findings = int(report["issue_count"].sum())

    critical_findings = int(
        report.loc[
            report["status"].str.upper() == "CRITICAL",
            "issue_count"
        ].sum()
    )

    warning_findings = int(
        report.loc[
            report["status"].str.upper() == "WARNING",
            "issue_count"
        ].sum()
    )

    good_checks = int(
        (
            report["status"].str.upper() == "GOOD"
        ).sum()
    )

    critical_datasets = report[
        report["status"].str.upper() == "CRITICAL"
    ]["dataset"].nunique()

    warning_datasets = report[
        report["status"].str.upper() == "WARNING"
    ]["dataset"].nunique()

    return (
        "🔎 Data Quality Summary\n\n"
        f"Total Findings: {total_findings:,}\n"
        f"Critical Findings: {critical_findings:,}\n"
        f"Warning Findings: {warning_findings:,}\n"
        f"Good Checks: {good_checks:,}\n"
        f"Datasets with Critical Issues: "
        f"{critical_datasets:,}\n"
        f"Datasets with Warnings: "
        f"{warning_datasets:,}\n\n"
        "Business Interpretation:\n"
        "Critical findings should be investigated before "
        "using affected data for important business decisions. "
        "Warning findings should be reviewed to determine "
        "whether they represent expected business behavior "
        "or genuine data-quality problems."
    )


def get_dataset_quality_issues(
    master_quality_report,
    n=10
):
    """
    Return datasets with the highest number of quality issues.
    """

    if (
        master_quality_report is None
        or master_quality_report.empty
    ):
        return "Master data quality report not available."

    required_columns = [
        "dataset",
        "issue_count",
        "status"
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in master_quality_report.columns
    ]

    if missing_columns:
        return (
            "Master quality report is missing required columns: "
            + ", ".join(missing_columns)
        )

    report = master_quality_report.copy()

    report["issue_count"] = pd.to_numeric(
        report["issue_count"],
        errors="coerce"
    ).fillna(0)

    dataset_summary = (
        report
        .groupby("dataset")
        .agg(
            total_issues=("issue_count", "sum")
        )
        .reset_index()
        .sort_values(
            "total_issues",
            ascending=False
        )
        .head(n)
    )

    if dataset_summary.empty:
        return "No dataset quality issues found."

    response = "⚠️ Datasets with Quality Issues\n\n"

    for i, (_, row) in enumerate(
        dataset_summary.iterrows(),
        start=1
    ):

        response += (
            f"#{i} {row['dataset']}\n"
            f"   Total Issues: "
            f"{int(row['total_issues']):,}\n\n"
        )

    return response
def analyze_category_performance(category_kpi):
    """
    Analyze product categories using revenue and sales volume.

    Categories are classified using median revenue and median units.
    """

    if category_kpi is None or category_kpi.empty:
        return "Category performance data is not available."

    required_columns = [
        "product_category_name",
        "revenue",
        "units"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in category_kpi.columns
    ]

    if missing_columns:
        return (
            "Category KPI is missing required columns: "
            + ", ".join(missing_columns)
        )

    df = category_kpi.copy()

    df["revenue"] = pd.to_numeric(
        df["revenue"],
        errors="coerce"
    )

    df["units"] = pd.to_numeric(
        df["units"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "product_category_name",
            "revenue",
            "units"
        ]
    )

    if df.empty:
        return "No valid category performance data found."

    # =================================================
    # MEDIAN THRESHOLDS
    # =================================================

    revenue_median = df["revenue"].median()
    units_median = df["units"].median()

    # =================================================
    # CLASSIFICATION
    # =================================================

    def classify_category(row):

        high_revenue = row["revenue"] >= revenue_median
        high_volume = row["units"] >= units_median

        if high_revenue and high_volume:
            return "Business Winner"

        elif high_revenue and not high_volume:
            return "Premium Category"

        elif not high_revenue and high_volume:
            return "High Volume - Low Value"

        else:
            return "Low Performer"

    df["category_segment"] = df.apply(
        classify_category,
        axis=1
    )

    # =================================================
    # BUSINESS WINNERS
    # =================================================

    business_winners = (
        df[
            df["category_segment"] == "Business Winner"
        ]
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    # =================================================
    # PREMIUM CATEGORIES
    # =================================================

    premium_categories = (
        df[
            df["category_segment"] == "Premium Category"
        ]
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    # =================================================
    # HIGH VOLUME - LOW VALUE
    # =================================================

    high_volume_low_value = (
        df[
            df["category_segment"]
            == "High Volume - Low Value"
        ]
        .sort_values(
            "units",
            ascending=False
        )
    )

    # =================================================
    # SEGMENT SUMMARY
    # =================================================

    segment_summary = (
        df.groupby("category_segment")
        .agg(
            categories=("product_category_name", "count"),
            revenue=("revenue", "sum"),
            units=("units", "sum")
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    # =================================================
    # RESPONSE
    # =================================================

    response = "📊 Category Performance Analysis\n\n"

    response += (
        f"Revenue Median: "
        f"{revenue_median:,.2f} BRL\n"
    )

    response += (
        f"Units Median: "
        f"{units_median:,.0f}\n\n"
    )

    # =================================================
    # SEGMENT SUMMARY
    # =================================================

    response += "📋 Performance Segments\n\n"

    for _, row in segment_summary.iterrows():

        response += (
            f"🔹 {row['category_segment']}\n"
            f"   Categories: {int(row['categories'])}\n"
            f"   Revenue: {row['revenue']:,.2f} BRL\n"
            f"   Units: {int(row['units']):,}\n\n"
        )

    # =================================================
    # BUSINESS WINNERS
    # =================================================

    if not business_winners.empty:

        response += (
            "🏆 Business Winner Categories\n\n"
        )

        for i, (_, row) in enumerate(
            business_winners.iterrows(),
            start=1
        ):

            response += (
                f"{i}. "
                f"{row['product_category_name']} — "
                f"Revenue: {row['revenue']:,.2f} BRL | "
                f"Units: {int(row['units']):,}\n"
            )

        response += "\n"

    # =================================================
    # PREMIUM CATEGORIES
    # =================================================

    if not premium_categories.empty:

        response += (
            "💎 Top Premium Categories\n\n"
        )

        for i, (_, row) in enumerate(
            premium_categories.head(10).iterrows(),
            start=1
        ):

            response += (
                f"{i}. "
                f"{row['product_category_name']} — "
                f"Revenue: {row['revenue']:,.2f} BRL | "
                f"Units: {int(row['units']):,}\n"
            )

        response += "\n"

    # =================================================
    # HIGH VOLUME - LOW VALUE
    # =================================================

    if not high_volume_low_value.empty:

        response += (
            "📦 High Volume - Low Value Categories\n\n"
        )

        for i, (_, row) in enumerate(
            high_volume_low_value.head(10).iterrows(),
            start=1
        ):

            response += (
                f"{i}. "
                f"{row['product_category_name']} — "
                f"Revenue: {row['revenue']:,.2f} BRL | "
                f"Units: {int(row['units']):,}\n"
            )

        response += "\n"

    return response