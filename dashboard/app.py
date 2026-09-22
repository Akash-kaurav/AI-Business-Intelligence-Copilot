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
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PROFESSIONAL UI THEME
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #070b14;
        --panel: rgba(17, 24, 39, 0.78);
        --panel-2: rgba(15, 23, 42, 0.92);
        --border: rgba(148, 163, 184, 0.16);
        --text: #f8fafc;
        --muted: #94a3b8;
        --accent: #38bdf8;
        --accent-2: #8b5cf6;
        --success: #34d399;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(56,189,248,.12), transparent 28%),
            radial-gradient(circle at 90% 10%, rgba(139,92,246,.14), transparent 30%),
            linear-gradient(135deg, #070b14 0%, #0b1120 48%, #080d18 100%);
        color: var(--text);
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    [data-testid="stHeader"] {
        background: rgba(7,11,20,.72);
        backdrop-filter: blur(14px);
    }

    .block-container {
        max-width: 1250px;
        padding-top: 5.8rem;
        padding-bottom: 3rem;
    }

    /* Fixed top navigation */
    .st-key-top_nav {
        position: fixed;
        top: 0.55rem;
        left: 50%;
        transform: translateX(-50%);
        width: min(1250px, calc(100vw - 2rem));
        z-index: 999999;
        padding: 8px 10px;
        border: 1px solid rgba(148,163,184,.12);
        border-radius: 18px;
        background: rgba(7,11,20,.72);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0 14px 40px rgba(0,0,0,.28);
    }

    .st-key-top_nav > div {
        margin: 0 !important;
    }

    .st-key-top_nav div[data-testid="stHorizontalBlock"] {
        margin: 0 !important;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 30px 34px;
        border: 1px solid rgba(125,211,252,.18);
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(15,23,42,.92), rgba(17,24,39,.72));
        box-shadow: 0 24px 70px rgba(0,0,0,.28);
        animation: fadeUp .65s ease-out both;
    }

    .hero:before {
        content: '';
        position: absolute;
        width: 240px;
        height: 240px;
        right: -90px;
        top: -120px;
        border-radius: 50%;
        background: rgba(56,189,248,.16);
        filter: blur(12px);
        animation: floatGlow 5s ease-in-out infinite;
    }

    .hero-kicker {
        color: #7dd3fc;
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: .14em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .hero-title {
        color: #f8fafc;
        font-size: clamp(2rem, 4vw, 3.2rem);
        line-height: 1.05;
        font-weight: 800;
        margin: 0;
        letter-spacing: -.04em;
    }

    .hero-title span {
        background: linear-gradient(90deg, #7dd3fc, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #a7b4c7;
        font-size: 1rem;
        margin-top: 12px;
        max-width: 760px;
    }

    .status-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 20px;
    }

    .status-pill {
        padding: 7px 12px;
        border-radius: 999px;
        border: 1px solid var(--border);
        background: rgba(15,23,42,.7);
        color: #cbd5e1;
        font-size: .78rem;
        font-weight: 600;
    }

    .status-pill.live {
        color: #86efac;
        border-color: rgba(52,211,153,.24);
    }

    .question-card {
        margin-top: 24px;
        padding: 22px;
        border-radius: 20px;
        border: 1px solid var(--border);
        background: rgba(15,23,42,.68);
        box-shadow: 0 18px 50px rgba(0,0,0,.18);
        animation: fadeUp .75s .08s ease-out both;
    }

    .section-label {
        color: #e2e8f0;
        font-size: 1.02rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .section-help {
        color: var(--muted);
        font-size: .84rem;
        margin-bottom: 10px;
    }

    div[data-testid="stTextInput"] input {
        background: rgba(2,6,23,.72) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(148,163,184,.20) !important;
        border-radius: 13px !important;
        padding: 14px 16px !important;
        transition: .25s ease;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: rgba(56,189,248,.7) !important;
        box-shadow: 0 0 0 3px rgba(56,189,248,.10), 0 0 28px rgba(56,189,248,.10) !important;
    }

    div[data-testid="stButton"] > button {
        width: 100%;
        min-height: 48px;
        border: 1px solid rgba(125,211,252,.28);
        border-radius: 13px;
        color: #ffffff;
        font-weight: 700;
        background: linear-gradient(135deg, #0ea5e9, #7c3aed);
        box-shadow: 0 10px 28px rgba(59,130,246,.18);
        transition: transform .2s ease, box-shadow .2s ease, filter .2s ease;
    }

    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        filter: brightness(1.08);
        box-shadow: 0 14px 34px rgba(59,130,246,.30);
    }

    .insight-card {
        margin-top: 22px;
        padding: 20px 22px;
        border-radius: 18px;
        border: 1px solid rgba(52,211,153,.20);
        background: linear-gradient(135deg, rgba(6,78,59,.18), rgba(15,23,42,.78));
        box-shadow: 0 18px 45px rgba(0,0,0,.18);
        animation: fadeUp .45s ease-out both;
    }

    .insight-label {
        color: #6ee7b7;
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .examples {
        margin-top: 28px;
        padding: 22px;
        border-radius: 20px;
        border: 1px solid var(--border);
        background: rgba(15,23,42,.56);
        animation: fadeUp .9s .12s ease-out both;
    }

    .examples li {
        color: #b8c4d6;
        margin: 7px 0;
    }

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #cbd5e1;
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        background: rgba(15,23,42,.52) !important;
    }

    .stAlert {
        border-radius: 14px !important;
    }


    /* Top navigation */
    /* Top navigation alignment */
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
        min-height: 42px;
        padding: 8px 16px;
        border-radius: 12px;
        font-size: .84rem;
        letter-spacing: .01em;
        width: 100%;
    }

    div[data-testid="stHorizontalBlock"] > div:first-child div[data-testid="stButton"] > button {
        width: 96px;
    }

    div[data-testid="stHorizontalBlock"] > div:last-child div[data-testid="stButton"] > button {
        width: 110px;
        margin-left: auto;
    }

    div[data-testid="stHorizontalBlock"] {
        align-items: center;
    }

    /* Question area — one real aligned card */
    .st-key-question_area {
        margin-top: 24px;
        padding: 24px 24px 22px;
        border: 1px solid var(--border);
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(15,23,42,.78), rgba(15,23,42,.56));
        box-shadow: 0 18px 55px rgba(0,0,0,.20);
        animation: fadeUp .75s .08s ease-out both;
        position: relative;
        overflow: hidden;
    }

    .st-key-question_area:before {
        content: '';
        position: absolute;
        width: 180px;
        height: 180px;
        right: -80px;
        bottom: -100px;
        border-radius: 50%;
        background: rgba(124,58,237,.14);
        filter: blur(24px);
        animation: pulseGlow 4s ease-in-out infinite;
        pointer-events: none;
    }

    .question-heading {
        margin: 0 0 8px;
        padding: 0;
        border: 0;
        background: transparent;
        box-shadow: none;
    }

    .question-input-row {
        padding: 0;
        border: 0;
        background: transparent;
        box-shadow: none;
        position: relative;
        z-index: 1;
    }

    .question-input-row div[data-testid="stTextInput"] {
        margin-top: 0;
    }

    .question-input-row div[data-testid="stTextInput"] input {
        min-height: 50px;
        box-sizing: border-box;
    }

    .question-input-row div[data-testid="stButton"] > button {
        min-height: 50px;
        margin-top: 0;
    }

    .developer-card {
        display: flex;
        align-items: center;
        gap: 18px;
        margin: 4px 0 22px;
        padding: 20px 22px;
        border: 1px solid rgba(125,211,252,.18);
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(15,23,42,.96), rgba(30,41,59,.78));
        box-shadow: 0 18px 50px rgba(0,0,0,.22);
        animation: fadeUp .35s ease-out both;
    }

    .developer-avatar {
        width: 62px;
        height: 62px;
        min-width: 62px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 18px;
        background: linear-gradient(135deg, #0ea5e9, #7c3aed);
        color: white;
        font-size: 1.15rem;
        font-weight: 800;
        box-shadow: 0 10px 28px rgba(59,130,246,.22);
    }

    .developer-label {
        color: #7dd3fc;
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .16em;
        margin-bottom: 3px;
    }

    .developer-name {
        color: #f8fafc;
        font-size: 1.2rem;
        font-weight: 800;
    }

    .developer-role {
        color: #cbd5e1;
        font-size: .84rem;
        margin-top: 2px;
    }

    .developer-details {
        color: #94a3b8;
        font-size: .78rem;
        line-height: 1.65;
        margin-top: 8px;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes floatGlow {
        0%, 100% { transform: translate(0,0) scale(1); opacity: .65; }
        50% { transform: translate(-24px, 18px) scale(1.12); opacity: .9; }
    }

    @keyframes pulseGlow {
        0%, 100% { transform: scale(1); opacity: .45; }
        50% { transform: scale(1.25); opacity: .8; }
    }

    @media (max-width: 700px) {
        .block-container { padding: 5rem 1rem 2rem; }
        .st-key-top_nav { width: calc(100vw - 1rem); }
        .hero { padding: 24px; border-radius: 20px; }
        .st-key-question_area { padding: 18px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION / NAVIGATION STATE
# =========================================================

if "question_input" not in st.session_state:
    st.session_state.question_input = ""

if "show_developer" not in st.session_state:
    st.session_state.show_developer = False


def go_home():
    st.session_state.question_input = ""
    st.session_state.show_developer = False


def toggle_developer():
    st.session_state.show_developer = not st.session_state.show_developer


# =========================================================
# TOP NAVIGATION
# =========================================================

with st.container(key="top_nav"):
    nav_home, nav_spacer, nav_developer = st.columns([1.0, 6.2, 1.5])

    with nav_home:
        st.button("⌂  Home", key="home_btn", on_click=go_home)

    with nav_developer:
        st.button("Developer", key="developer_btn", on_click=toggle_developer)

if st.session_state.show_developer:
    st.markdown(
        """
        <div class="developer-card">
            <div class="developer-avatar">AK</div>
            <div class="developer-content">
                <div class="developer-label">DEVELOPER</div>
                <div class="developer-name">Akash Kaurav</div>
                <div class="developer-role">Data Analyst • AI / BI Enthusiast</div>
                <div class="developer-details">
                    MCA — Computer Science, MITS Gwalior • 2026<br>
                    Core Skills: SQL, Python, Pandas, Power BI, MySQL, Machine Learning<br>
                    Project: AI Business Intelligence Copilot
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">AI-powered analytics workspace</div>
        <div class="hero-title">AI Business <span>Intelligence Copilot</span></div>
        <div class="hero-subtitle">
            Ask natural-language business questions and turn trusted Olist data into clear, actionable insights.
        </div>
        <div class="status-row">
            <div class="status-pill live">● Copilot Ready</div>
            <div class="status-pill">SQL + Python Analytics</div>
            <div class="status-pill">ML Forecasting</div>
            <div class="status-pill">Data Quality Monitor</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
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

    st.markdown(
        f"""
        <div class=\"insight-card\">
            <div class=\"insight-label\">{title}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

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

with st.container(key="question_area"):
    st.markdown(
        """
        <div class="question-heading">
            <div class="section-label">💬 Ask Your Business Question</div>
            <div class="section-help">Ask about revenue, customers, products, sellers, forecasting, or data quality.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    input_col, ask_col = st.columns([6.4, 1.0], gap="small")

    with input_col:
        question = st.text_input(
            "",
            key="question_input",
            placeholder="Example: Which customers should we prioritize for retention?",
            label_visibility="collapsed"
        )

    with ask_col:
        ask_clicked = st.button("Ask Copilot", key="ask_copilot_btn")


# =========================================================
# ASK COPILOT
# =========================================================

if ask_clicked:

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

st.markdown(
    """
    <div class="examples">
        <div class="section-label">💡 Example Questions</div>
        <div class="section-help">Use these prompts to demonstrate the Copilot during your portfolio presentation.</div>
    """,
    unsafe_allow_html=True
)

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

st.markdown("</div>", unsafe_allow_html=True)
