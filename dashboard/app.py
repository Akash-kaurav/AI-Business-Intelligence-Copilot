import streamlit as st
import sys
from pathlib import Path


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


# =========================================================
# IMPORT PROJECT MODULES
# =========================================================

from src.copilot_data import load_copilot_data
from src import business_engine
from src import data_quality_engine
from ai.copilot_llm import generate_llm_response


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Business Intelligence Copilot",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🤖 AI Business Intelligence Copilot")

st.write(
    "Ask business questions and get data-driven insights "
    "from the Olist e-commerce dataset."
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def get_data():
    return load_copilot_data()


data = get_data()


# =========================================================
# DATA REFERENCES
# =========================================================

monthly_business = data["monthly_business"]
monthly_customer = data["monthly_customer"]
monthly_category = data["monthly_category"]

category_kpi = data["category_kpi"]
product_kpi = data["product_kpi"]

customer_rfm = data["customer_rfm"]

daily_sales = data["daily_sales"]


# =========================================================
# SELLER DATA
# =========================================================

seller_analysis = data.get("seller_analysis")
risk_sellers = data.get("risk_sellers")


# =========================================================
# CREATE RISK SELLER DATA IF NOT AVAILABLE
# =========================================================

if risk_sellers is None and seller_analysis is not None:

    required_seller_columns = [
        "total_revenue",
        "late_rate",
        "delivered_orders"
    ]

    if all(
        col in seller_analysis.columns
        for col in required_seller_columns
    ):

        risk_sellers = seller_analysis[
            (seller_analysis["total_revenue"]
             >= seller_analysis["total_revenue"].quantile(0.75))
            &
            (seller_analysis["late_rate"] >= 10)
            &
            (seller_analysis["delivered_orders"] >= 10)
        ].copy()


# =========================================================
# MASTER DATA QUALITY REPORT
# =========================================================

master_quality_report = (
    data_quality_engine.generate_master_quality_report(data)
)


# =========================================================
# HELPER FUNCTION
# =========================================================

def display_copilot_response(
    user_question,
    analytics_result,
    title="🤖 AI Business Insight"
):
    """
    Sends the trusted analytics result to the LLM
    and displays the AI-generated business explanation.
    """

    st.success(title)

    with st.spinner(
        "🤖 AI is analyzing the business result..."
    ):

        ai_response = generate_llm_response(
            user_question,
            analytics_result
        )

    if ai_response.startswith("❌"):

        st.warning(
            "AI explanation could not be generated. "
            "Showing the original analytics result instead."
        )

        st.text(analytics_result)

    else:

        st.markdown(ai_response)

        with st.expander(
            "🔎 View Original Analytics Result"
        ):

            st.text(analytics_result)


# =========================================================
# QUESTION INPUT
# =========================================================

st.subheader("💬 Ask Your Business Question")

question = st.text_input(
    "Enter your question",
    placeholder="Example: How many VIP customers do we have?"
)


# =========================================================
# ASK COPILOT
# =========================================================

if st.button("Ask Copilot"):

    if not question.strip():

        st.warning(
            "Please enter a business question."
        )

    else:

        question_lower = question.lower().strip()


        # =================================================
        # CUSTOMER INTELLIGENCE
        # =================================================

        if (
            "customer" in question_lower
            or "customers" in question_lower
            or "vip" in question_lower
            or "at risk" in question_lower
            or "retention" in question_lower
            or "lost customer" in question_lower
            or "lost customers" in question_lower
            or "customer priority" in question_lower
            or "prioritize customer" in question_lower
            or "prioritize customers" in question_lower
        ):

            # ---------------------------------------------
            # CUSTOMER PRIORITY
            # ---------------------------------------------

            if (
                "priority" in question_lower
                or "prioritize" in question_lower
                or "should we prioritize" in question_lower
                or "who should we prioritize" in question_lower
                or "which customers should we prioritize"
                in question_lower
            ):

                number = business_engine.extract_number(
                    question_lower,
                    default=10
                )

                response = (
                    business_engine
                    .get_customer_priority_insight(
                        customer_rfm,
                        number
                    )
                )

                display_copilot_response(
                    question,
                    response,
                    "🎯 Customer Intelligence"
                )


            # ---------------------------------------------
            # VIP CUSTOMERS
            # ---------------------------------------------

            elif (
                "vip" in question_lower
                or "high value customer" in question_lower
                or "high value customers" in question_lower
            ):

                number = business_engine.extract_number(
                    question_lower,
                    default=10
                )

                response = (
                    business_engine
                    .get_vip_customer_insight(
                        customer_rfm,
                        number
                    )
                )

                display_copilot_response(
                    question,
                    response,
                    "👑 Customer Intelligence"
                )


            # ---------------------------------------------
            # AT-RISK CUSTOMERS
            # ---------------------------------------------

            elif (
                "at risk" in question_lower
                or "risk customer" in question_lower
                or "risk customers" in question_lower
            ):

                number = business_engine.extract_number(
                    question_lower,
                    default=10
                )

                response = (
                    business_engine
                    .get_at_risk_customer_insight(
                        customer_rfm,
                        number
                    )
                )

                display_copilot_response(
                    question,
                    response,
                    "⚠️ Customer Intelligence"
                )


            # ---------------------------------------------
            # CUSTOMER RETENTION
            # ---------------------------------------------

            elif (
                "retention" in question_lower
                or "lost customer" in question_lower
                or "lost customers" in question_lower
            ):

                response = (
                    business_engine
                    .get_customer_retention_insight(
                        customer_rfm
                    )
                )

                display_copilot_response(
                    question,
                    response,
                    "🔄 Customer Retention Intelligence"
                )


            # ---------------------------------------------
            # GENERAL CUSTOMER QUESTION
            # ---------------------------------------------

            else:

                response = (
                    business_engine
                    .get_customer_retention_insight(
                        customer_rfm
                    )
                )

                display_copilot_response(
                    question,
                    response,
                    "👥 Customer Intelligence"
                )


        # =================================================
        # CATEGORY INTELLIGENCE
        # IMPORTANT:
        # CATEGORY MUST COME BEFORE PRODUCT
        # =================================================

        elif (
            "category" in question_lower
            or "categories" in question_lower
        ):

            # ---------------------------------------------
            # CATEGORY PERFORMANCE
            # ---------------------------------------------

            if (
                "performance" in question_lower
                or "high revenue" in question_lower
                or "high sales volume" in question_lower
                or "high volume" in question_lower
                or "business winner" in question_lower
                or "strongest category" in question_lower
                or "best category" in question_lower
                or "prioritize" in question_lower
            ):

                response = (
                    business_engine
                    .analyze_category_performance(
                        category_kpi
                    )
                )

                display_copilot_response(
                    question,
                    response,
                    "📊 Category Performance Intelligence"
                )


            # ---------------------------------------------
            # TOP CATEGORIES BY REVENUE
            # ---------------------------------------------

            else:

                number = business_engine.extract_number(
                    question_lower,
                    default=5
                )

                response = (
                    business_engine
                    .get_top_categories(
                        category_kpi,
                        number
                    )
                )

                display_copilot_response(
                    question,
                    response,
                    "🏆 Category Intelligence"
                )


        # =================================================
        # PRODUCT INTELLIGENCE
        # =================================================

        elif (
            "product" in question_lower
            or "products" in question_lower
            or "business winner" in question_lower
            or "business winners" in question_lower
            or "high demand" in question_lower
        ):

            number = business_engine.extract_number(
                question_lower,
                default=10
            )


            # ---------------------------------------------
            # BUSINESS WINNER PRODUCTS
            # ---------------------------------------------

            if (
                "business winner" in question_lower
                or "business winners" in question_lower
            ):

                response = (
                    business_engine
                    .get_business_winner_products(
                        product_kpi,
                        number
                    )
                )

                display_copilot_response(
                    question,
                    response,
                    "🏆 Product Intelligence"
                )


            # ---------------------------------------------
            # HIGH DEMAND - LOW VALUE PRODUCTS
            # ---------------------------------------------

            elif "high demand" in question_lower:

                response = (
                    business_engine
                    .analyze_product_performance(
                        product_kpi
                    )
                )

                display_copilot_response(
                    question,
                    response,
                    "📦 Product Intelligence"
                )


            # ---------------------------------------------
            # TOP PRODUCTS
            # ---------------------------------------------

            else:

                response = (
                    business_engine
                    .get_top_products(
                        product_kpi,
                        number
                    )
                )

                display_copilot_response(
                    question,
                    response,
                    "📦 Product Intelligence"
                )


        # =================================================
        # SELLER INTELLIGENCE
        # =================================================
        
        elif (
            "seller" in question_lower
            or "sellers" in question_lower
            or "vendor" in question_lower
            or "vendors" in question_lower
        ):
        
            number = business_engine.extract_number(
                question_lower,
                default=10
            )
        
            # ---------------------------------------------
            # TOP / HIGH PERFORMER SELLERS
            # ---------------------------------------------
        
            if (
                "top performer" in question_lower
                or "top performers" in question_lower
                or "high performer" in question_lower
                or "high performers" in question_lower
                or "best seller" in question_lower
                or "best sellers" in question_lower
            ):
        
                if seller_analysis is None or seller_analysis.empty:
        
                    response = (
                        "Seller performance data not available."
                    )
        
                else:
        
                    performance_columns = [
                        "seller_id",
                        "total_revenue",
                        "total_orders",
                        "avg_order_value",
                        "performance_segment"
                    ]
        
                    missing_columns = [
                        col
                        for col in performance_columns
                        if col not in seller_analysis.columns
                    ]
        
                    if missing_columns:
        
                        response = (
                            "Seller performance analysis is missing "
                            "required columns: "
                            + ", ".join(missing_columns)
                        )
        
                    else:
        
                        top_performers = (
                            seller_analysis[
                                seller_analysis[
                                    "performance_segment"
                                ].isin(
                                    [
                                        "Top Performer",
                                        "High Performer"
                                    ]
                                )
                            ]
                            .sort_values(
                                "total_revenue",
                                ascending=False
                            )
                            .head(number)
                        )
        
                        if top_performers.empty:
        
                            response = (
                                "No Top Performer or High Performer "
                                "sellers found."
                            )
        
                        else:
        
                            response = (
                                "🏆 Top Performing Sellers\n\n"
                            )
        
                            for i, (_, row) in enumerate(
                                top_performers.iterrows(),
                                start=1
                            ):
        
                                response += (
                                    f"#{i} Seller: "
                                    f"{row['seller_id']}\n"
                                    f"Performance: "
                                    f"{row['performance_segment']}\n"
                                    f"Revenue: "
                                    f"{row['total_revenue']:,.2f} BRL\n"
                                    f"Orders: "
                                    f"{int(row['total_orders']):,}\n"
                                    f"Average Order Value: "
                                    f"{row['avg_order_value']:,.2f} BRL\n\n"
                                )
        
                display_copilot_response(
                    question,
                    response,
                    "🏆 Seller Performance Intelligence"
                )
        
            # ---------------------------------------------
            # RISKY SELLERS / LATE DELIVERY
            # ---------------------------------------------
        
            else:
        
                if risk_sellers is None:
        
                    response = (
                        "Risky seller data not available."
                    )
        
                elif risk_sellers.empty:
        
                    response = (
                        "No risky sellers found."
                    )
        
                else:
        
                    response = business_engine.get_risky_sellers(
                        risk_sellers,
                        number
                    )
        
                display_copilot_response(
                    question,
                    response,
                    "⚠️ Seller Intelligence"
                )
        
        
                # =================================================
                # DATA QUALITY INTELLIGENCE
                # =================================================
        elif (
                    "data quality" in question_lower
                    or "quality issue" in question_lower
                    or "quality issues" in question_lower
                    or "data issue" in question_lower
                    or "data issues" in question_lower
                    or "data problem" in question_lower
                    or "data problems" in question_lower
                    or "dataset quality" in question_lower
                    or "quality report" in question_lower
                ):
        
                    if (
                        "which dataset" in question_lower
                        or "datasets" in question_lower
                        or "most issues" in question_lower
                        or "highest issues" in question_lower
                    ):
        
                        number = business_engine.extract_number(
                            question_lower,
                            default=10
                        )
        
                        response = (
                            business_engine
                            .get_dataset_quality_issues(
                                master_quality_report,
                                number
                            )
                        )
        
                        display_copilot_response(
                            question,
                            response,
                            "🔎 Data Quality Intelligence"
                        )
        
        
                    else:
        
                        response = (
                            business_engine
                            .get_data_quality_summary(
                                master_quality_report
                            )
                        )
        
                        display_copilot_response(
                            question,
                            response,
                            "🔎 Data Quality Intelligence"
                        )
        
        
                # =================================================
                # REVENUE FORECASTING
                # =================================================
        
        elif (
                    "forecast" in question_lower
                    or "predict" in question_lower
                    or "prediction" in question_lower
                    or "tomorrow" in question_lower
                    or "next day" in question_lower
                    or "future revenue" in question_lower
                ):
        
                    if (
                        "accurate" in question_lower
                        or "accuracy" in question_lower
                        or "model performance" in question_lower
                        or "model perform" in question_lower
                        or "forecast performance" in question_lower
                        or "forecast accuracy" in question_lower
                        or "error" in question_lower
                        or "mae" in question_lower
                        or "rmse" in question_lower
                        or "mape" in question_lower
                    ):
        
                        response = (
                            business_engine
                            .get_revenue_forecast_model_evaluation()
                        )
        
                        display_copilot_response(
                            question,
                            response,
                            "📈 Forecast Model Evaluation"
                        )
        
        
                    else:
        
                        response = (
                            business_engine
                            .predict_next_day_revenue(
                                daily_sales
                            )
                        )
        
                        display_copilot_response(
                            question,
                            response,
                            "🔮 Revenue Forecast Intelligence"
                        )
        
        
                # =================================================
                # REVENUE INTELLIGENCE
                # =================================================
        
        elif "revenue" in question_lower:
        
                    selected_month = (
                        business_engine.extract_month(
                            question_lower
                        )
                    )
        
                    if selected_month is None:
        
                        st.info(
                            "Please specify month and year.\n\n"
                            "Example: Why did revenue decline in June 2018?"
                        )
        
                    else:
        
                        available_months = (
                            monthly_business["month"]
                            .dt.strftime("%Y-%m")
                            .tolist()
                        )
        
                        if selected_month not in available_months:
        
                            st.error(
                                f"No revenue data available for "
                                f"{selected_month}."
                            )
        
                        else:
        
                            response = (
                                business_engine
                                .generate_copilot_business_response(
                                    selected_month,
                                    monthly_business,
                                    monthly_customer,
                                    monthly_category
                                )
                            )
        
                            display_copilot_response(
                                question,
                                response,
                                "📊 Copilot Analysis"
                            )
        
        
                # =================================================
                # UNKNOWN QUESTION
                # =================================================
        
        else:
        
                    st.info(
                        "🤖 I can currently answer questions about:\n\n"
                        "📊 Revenue Intelligence\n"
                        "🔮 Revenue Forecasting\n"
                        "📈 Forecast Model Evaluation\n"
                        "🔎 Data Quality Intelligence\n"
                        "🏆 Product Category Intelligence\n"
                        "📦 Product Intelligence\n"
                        "👥 Customer Intelligence\n"
                        "⚠️ Seller Intelligence\n\n"
                        "More Copilot capabilities will be added next."
                    )
        
        
        # =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.divider()

st.subheader("💡 Example Questions")

st.markdown(
    """
- Why did revenue decline in June 2018?
- Why did revenue decline in February 2018?
- What happened to revenue in May 2018?

- What will tomorrow's revenue be?
- Can you predict the next day's revenue?
- What is the revenue forecast?
- Predict future revenue.

- How accurate is the revenue forecast model?
- How does the forecast model perform?
- What are the MAE, RMSE and MAPE?
- What is the forecast error?

- Are there any data quality issues?
- Give me the data quality summary.
- Which datasets have the most quality issues?
- Which dataset has the highest number of issues?
- Show me the quality report.

- What are the top 5 product categories by revenue?
- What are the top 10 categories by revenue?
- Which categories have high revenue and high sales volume?
- Which are the strongest product categories?
- What are the top 10 products by revenue?
- Which products are business winners?
- Which products have high demand but low value?

- How many VIP customers do we have?
- Which customers are at risk?
- What is our customer retention risk?
- Which customers should we prioritize for retention?

- Show me the top 10 risky sellers.
- Which sellers have the highest late delivery rate?
- Show me risky vendors.
"""
)
