import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


# =========================================================
# LOAD DATA
# =========================================================

def load_olist_data():

    customers = pd.read_csv(
        DATA_DIR / "olist_customers_dataset.csv"
    )

    orders = pd.read_csv(
        DATA_DIR / "olist_orders_dataset.csv"
    )

    order_items = pd.read_csv(
        DATA_DIR / "olist_order_items_dataset.csv"
    )

    products = pd.read_csv(
        DATA_DIR / "olist_products_dataset.csv"
    )

    sellers = pd.read_csv(
        DATA_DIR / "olist_sellers_dataset.csv"
    )

    return (
        customers,
        orders,
        order_items,
        products,
        sellers
    )


# =========================================================
# PREPARE DATE COLUMNS
# =========================================================

def prepare_orders(orders):

    orders = orders.copy()

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:

        if column in orders.columns:

            orders[column] = pd.to_datetime(
                orders[column],
                errors="coerce"
            )

    return orders


# =========================================================
# SALES DATA
# =========================================================

def create_sales_data(
    orders,
    order_items
):

    sales_data = order_items.merge(
        orders[
            [
                "order_id",
                "order_status",
                "order_purchase_timestamp"
            ]
        ],
        on="order_id",
        how="left"
    )

    # Delivered orders only for revenue analysis
    sales_data = sales_data[
        sales_data["order_status"] == "delivered"
    ].copy()

    sales_data["month"] = (
        sales_data["order_purchase_timestamp"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    return sales_data


# =========================================================
# MONTHLY BUSINESS METRICS
# =========================================================

def create_monthly_business(
    sales_data
):

    monthly_business = (
        sales_data
        .groupby("month")
        .agg(
            revenue=("price", "sum"),
            units=("order_item_id", "count"),
            orders=("order_id", "nunique")
        )
        .reset_index()
        .sort_values("month")
    )

    monthly_business["revenue_growth_pct"] = (
        monthly_business["revenue"]
        .pct_change()
        * 100
    )

    monthly_business["order_growth_pct"] = (
        monthly_business["orders"]
        .pct_change()
        * 100
    )

    monthly_business["unit_growth_pct"] = (
        monthly_business["units"]
        .pct_change()
        * 100
    )

    return monthly_business


# =========================================================
# MONTHLY CUSTOMER METRICS
# =========================================================

def create_monthly_customer(
    sales_data,
    orders,
    customers
):

    customer_orders = orders.merge(
        customers[
            [
                "customer_id",
                "customer_unique_id"
            ]
        ],
        on="customer_id",
        how="left"
    )

    customer_orders = customer_orders[
        customer_orders["order_status"] == "delivered"
    ].copy()

    customer_orders["month"] = (
        customer_orders["order_purchase_timestamp"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    # Monthly unique customers
    monthly_customer_count = (
        customer_orders
        .groupby("month")["customer_unique_id"]
        .nunique()
        .reset_index()
    )

    monthly_customer_count.columns = [
        "month",
        "customer_count"
    ]

    # Revenue by customer and month
    sales_customer = sales_data.merge(
        orders[
            [
                "order_id",
                "customer_id"
            ]
        ],
        on="order_id",
        how="left"
    )

    sales_customer = sales_customer.merge(
        customers[
            [
                "customer_id",
                "customer_unique_id"
            ]
        ],
        on="customer_id",
        how="left"
    )

    monthly_customer_revenue = (
        sales_customer
        .groupby("month")["price"]
        .sum()
        .reset_index()
    )

    monthly_customer_revenue.columns = [
        "month",
        "revenue"
    ]

    monthly_customer = monthly_customer_count.merge(
        monthly_customer_revenue,
        on="month",
        how="left"
    )

    monthly_customer["revenue_per_customer"] = (
        monthly_customer["revenue"]
        / monthly_customer["customer_count"]
    )

    monthly_customer["customer_growth_pct"] = (
        monthly_customer["customer_count"]
        .pct_change()
        * 100
    )

    monthly_customer[
        "revenue_per_customer_growth_pct"
    ] = (
        monthly_customer["revenue_per_customer"]
        .pct_change()
        * 100
    )

    return monthly_customer


# =========================================================
# CUSTOMER RFM
# =========================================================

def create_customer_rfm(
    sales_data,
    orders,
    customers
):

    sales_customer = sales_data.merge(
        orders[
            [
                "order_id",
                "customer_id"
            ]
        ],
        on="order_id",
        how="left"
    )

    sales_customer = sales_customer.merge(
        customers[
            [
                "customer_id",
                "customer_unique_id"
            ]
        ],
        on="customer_id",
        how="left"
    )

    customer_rfm = (
        sales_customer
        .groupby("customer_unique_id")
        .agg(
            frequency=("order_id", "nunique"),
            monetary=("price", "sum"),
            last_purchase=(
                "order_purchase_timestamp",
                "max"
            )
        )
        .reset_index()
    )

    reference_date = pd.Timestamp(
        "2018-08-29 15:00:37"
    )

    customer_rfm["recency"] = (
        reference_date
        - customer_rfm["last_purchase"]
    ).dt.days

    customer_rfm["r_score"] = pd.qcut(
        customer_rfm["recency"],
        5,
        labels=[5, 4, 3, 2, 1]
    )

    customer_rfm["f_score"] = pd.qcut(
        customer_rfm["frequency"].rank(
            method="first"
        ),
        5,
        labels=[1, 2, 3, 4, 5]
    )

    customer_rfm["m_score"] = pd.qcut(
        customer_rfm["monetary"],
        5,
        labels=[1, 2, 3, 4, 5]
    )

    customer_rfm["rfm_score"] = (
        customer_rfm["r_score"].astype(int)
        + customer_rfm["f_score"].astype(int)
        + customer_rfm["m_score"].astype(int)
    )

    def segment_customer(row):

        if row["rfm_score"] >= 13:
            return "VIP"

        elif row["rfm_score"] >= 10:
            return "Loyal"

        elif row["rfm_score"] >= 7:
            return "Potential Loyal"

        elif row["rfm_score"] >= 5:
            return "At Risk"

        else:
            return "Lost"

    customer_rfm["customer_segment"] = (
        customer_rfm.apply(
            segment_customer,
            axis=1
        )
    )

    customer_rfm["avg_order_value"] = (
        customer_rfm["monetary"]
        / customer_rfm["frequency"]
    )

    return customer_rfm


# =========================================================
# MONTHLY CATEGORY METRICS
# =========================================================

def create_monthly_category(
    sales_data,
    products
):

    category_sales = sales_data.merge(
        products[
            [
                "product_id",
                "product_category_name"
            ]
        ],
        on="product_id",
        how="left"
    )

    category_sales["product_category_name"] = (
        category_sales["product_category_name"]
        .fillna("Unknown")
    )

    monthly_category = (
        category_sales
        .groupby(
            [
                "month",
                "product_category_name"
            ]
        )
        .agg(
            revenue=("price", "sum"),
            units=("order_item_id", "count")
        )
        .reset_index()
        .sort_values(
            [
                "product_category_name",
                "month"
            ]
        )
    )

    monthly_category["revenue_growth"] = (
        monthly_category
        .groupby("product_category_name")["revenue"]
        .pct_change()
        * 100
    )

    return monthly_category


# =========================================================
# CATEGORY KPI
# =========================================================

def create_category_kpi(
    sales_data,
    products
):

    category_sales = sales_data.merge(
        products[
            [
                "product_id",
                "product_category_name"
            ]
        ],
        on="product_id",
        how="left"
    )

    category_sales["product_category_name"] = (
        category_sales["product_category_name"]
        .fillna("Unknown")
    )

    category_kpi = (
        category_sales
        .groupby("product_category_name")
        .agg(
            revenue=("price", "sum"),
            units=("order_item_id", "count")
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    return category_kpi


# =========================================================
# PRODUCT KPI
# =========================================================

def create_product_kpi(
    sales_data,
    products
):

    product_sales = sales_data.merge(
        products[
            [
                "product_id",
                "product_category_name"
            ]
        ],
        on="product_id",
        how="left"
    )

    product_sales["product_category_name"] = (
        product_sales["product_category_name"]
        .fillna("Unknown")
    )

    product_kpi = (
        product_sales
        .groupby(
            [
                "product_id",
                "product_category_name"
            ]
        )
        .agg(
            total_revenue=("price", "sum"),
            total_units=("order_item_id", "count"),
            total_orders=("order_id", "nunique"),
            avg_price=("price", "mean")
        )
        .reset_index()
        .sort_values(
            "total_revenue",
            ascending=False
        )
    )

    # -----------------------------------------------------
    # Compatibility columns
    # -----------------------------------------------------

    product_kpi["revenue"] = (
        product_kpi["total_revenue"]
    )

    product_kpi["units"] = (
        product_kpi["total_units"]
    )

    product_kpi["orders"] = (
        product_kpi["total_orders"]
    )

    # -----------------------------------------------------
    # Product business segmentation
    #
    # Business rules:
    #
    # High Revenue = revenue >= 1000 BRL
    # High Volume  = units >= 10
    #
    # High Revenue + High Volume
    #       -> Business Winner
    #
    # High Revenue + Low Volume
    #       -> Premium Product
    #
    # Low Revenue + High Volume
    #       -> High Demand - Low Value
    #
    # Low Revenue + Low Volume
    #       -> Low Performer
    # -----------------------------------------------------

    def classify_product(row):

        high_revenue = (
            row["total_revenue"] >= 1000
        )

        high_volume = (
            row["total_units"] >= 10
        )

        if high_revenue and high_volume:
            return "Business Winner"

        elif high_revenue and not high_volume:
            return "Premium Product"

        elif not high_revenue and high_volume:
            return "High Demand - Low Value"

        else:
            return "Low Performer"

    product_kpi["product_segment"] = (
        product_kpi.apply(
            classify_product,
            axis=1
        )
    )

    return product_kpi


# =========================================================
# SELLER ANALYSIS
# =========================================================

def create_seller_analysis(
    orders,
    order_items,
    sellers
):
    """
    Create seller-level revenue and delivery performance.

    Delivery is calculated at seller-order level so that
    multiple products inside the same order do not
    artificially increase the seller's delivery count.
    """

    # -----------------------------------------------------
    # Seller revenue
    # -----------------------------------------------------

    seller_revenue = (
        order_items
        .groupby("seller_id")
        .agg(
            total_revenue=("price", "sum"),
            total_orders=("order_id", "nunique"),
            total_items=("order_item_id", "count")
        )
        .reset_index()
    )

    # -----------------------------------------------------
    # Seller-order delivery data
    # -----------------------------------------------------

    seller_orders = order_items[
        [
            "seller_id",
            "order_id"
        ]
    ].drop_duplicates()

    seller_orders = seller_orders.merge(
        orders[
            [
                "order_id",
                "order_status",
                "order_delivered_customer_date",
                "order_estimated_delivery_date"
            ]
        ],
        on="order_id",
        how="left"
    )

    # Only delivered orders are used for delivery performance
    seller_orders = seller_orders[
        seller_orders["order_status"] == "delivered"
    ].copy()

    seller_orders["delivery_delay_days"] = (
        seller_orders["order_delivered_customer_date"]
        - seller_orders["order_estimated_delivery_date"]
    ).dt.days

    seller_delivery = (
        seller_orders
        .groupby("seller_id")
        .agg(
            delivered_orders=("order_id", "nunique"),
            late_orders=(
                "delivery_delay_days",
                lambda x: (x > 0).sum()
            )
        )
        .reset_index()
    )

    seller_delivery["late_rate"] = (
        seller_delivery["late_orders"]
        / seller_delivery["delivered_orders"]
        * 100
    )

    # -----------------------------------------------------
    # Combine revenue + delivery
    # -----------------------------------------------------

    seller_analysis = seller_revenue.merge(
        seller_delivery,
        on="seller_id",
        how="left"
    )

    seller_analysis = seller_analysis.merge(
        sellers[
            [
                "seller_id",
                "seller_city",
                "seller_state"
            ]
        ],
        on="seller_id",
        how="left"
    )

    seller_analysis["delivered_orders"] = (
        seller_analysis["delivered_orders"]
        .fillna(0)
    )

    seller_analysis["late_orders"] = (
        seller_analysis["late_orders"]
        .fillna(0)
    )

    seller_analysis["late_rate"] = (
        seller_analysis["late_rate"]
        .fillna(0)
    )

    seller_analysis["avg_order_value"] = (
        seller_analysis["total_revenue"]
        / seller_analysis["total_orders"]
    )

    # -----------------------------------------------------
    # Seller performance score
    # -----------------------------------------------------

    seller_analysis["revenue_score"] = (
        seller_analysis["total_revenue"]
        .rank(pct=True)
        * 100
    )

    seller_analysis["orders_score"] = (
        seller_analysis["total_orders"]
        .rank(pct=True)
        * 100
    )

    seller_analysis["aov_score"] = (
        seller_analysis["avg_order_value"]
        .rank(pct=True)
        * 100
    )

    seller_analysis["performance_score"] = (
        seller_analysis["revenue_score"] * 0.50
        + seller_analysis["orders_score"] * 0.30
        + seller_analysis["aov_score"] * 0.20
    )

    seller_analysis["performance_segment"] = pd.cut(
        seller_analysis["performance_score"],
        bins=[
            -float("inf"),
            25,
            50,
            75,
            float("inf")
        ],
        labels=[
            "Low Performer",
            "Average Performer",
            "High Performer",
            "Top Performer"
        ]
    )

    # Keep the previous column name as a compatibility alias.
    seller_analysis["performance_category"] = (
        seller_analysis["performance_segment"]
    )

    return seller_analysis


# =========================================================
# RISKY SELLERS
# =========================================================

def create_risk_sellers(
    seller_analysis
):
    """
    Identify high-revenue sellers with elevated late delivery rates.

    Business rules:
    - Revenue >= 75th percentile
    - Late rate >= 10%
    - At least 10 delivered orders
    """

    if seller_analysis is None or seller_analysis.empty:
        return pd.DataFrame()

    revenue_threshold = (
        seller_analysis["total_revenue"]
        .quantile(0.75)
    )

    risk_sellers = seller_analysis[
        (seller_analysis["total_revenue"] >= revenue_threshold)
        &
        (seller_analysis["late_rate"] >= 10)
        &
        (seller_analysis["delivered_orders"] >= 10)
    ].copy()

    return risk_sellers.sort_values(
        ["late_rate", "total_revenue"],
        ascending=[False, False]
    )


# =========================================================
# DAILY SALES
# =========================================================

def build_daily_sales(sales_data):
    """
    Build daily revenue, units and order metrics
    for revenue forecasting.
    """

    if sales_data is None or sales_data.empty:
        return pd.DataFrame()

    daily_sales = (
        sales_data
        .groupby(
            sales_data["order_purchase_timestamp"].dt.date
        )
        .agg(
            revenue=("price", "sum"),
            units=("order_item_id", "count"),
            orders=("order_id", "nunique")
        )
        .reset_index()
    )

    daily_sales = daily_sales.rename(
        columns={
            "order_purchase_timestamp": "date"
        }
    )

    daily_sales["date"] = pd.to_datetime(
        daily_sales["date"]
    )

    daily_sales = daily_sales.sort_values(
        "date"
    )

    # Complete daily calendar
    all_dates = pd.date_range(
        start=daily_sales["date"].min(),
        end=daily_sales["date"].max(),
        freq="D"
    )

    daily_sales = (
        daily_sales
        .set_index("date")
        .reindex(all_dates)
        .rename_axis("date")
        .reset_index()
    )

    daily_sales["revenue"] = (
        daily_sales["revenue"].fillna(0)
    )

    daily_sales["units"] = (
        daily_sales["units"].fillna(0)
    )

    daily_sales["orders"] = (
        daily_sales["orders"].fillna(0)
    )

    # Previous-day features
    daily_sales["previous_day_revenue"] = (
        daily_sales["revenue"].shift(1)
    )

    daily_sales["previous_day_units"] = (
        daily_sales["units"].shift(1)
    )

    daily_sales["previous_day_orders"] = (
        daily_sales["orders"].shift(1)
    )

    # Previous-week features
    daily_sales["previous_week_revenue"] = (
        daily_sales["revenue"].shift(7)
    )

    daily_sales["previous_week_units"] = (
        daily_sales["units"].shift(7)
    )

    daily_sales["previous_week_orders"] = (
        daily_sales["orders"].shift(7)
    )

    # 7-day rolling features
    daily_sales["rolling_7d_revenue"] = (
        daily_sales["revenue"]
        .rolling(7)
        .mean()
    )

    daily_sales["rolling_7d_units"] = (
        daily_sales["units"]
        .rolling(7)
        .mean()
    )

    daily_sales["rolling_7d_orders"] = (
        daily_sales["orders"]
        .rolling(7)
        .mean()
    )

    # Calendar features
    daily_sales["day_of_week"] = (
        daily_sales["date"].dt.dayofweek
    )

    daily_sales["month"] = (
        daily_sales["date"].dt.month
    )

    daily_sales["year"] = (
        daily_sales["date"].dt.year
    )

    daily_sales["is_weekend"] = (
        daily_sales["day_of_week"] >= 5
    ).astype(int)

    return daily_sales


# =========================================================
# MAIN DATA LOADER
# =========================================================

def load_copilot_data():

    (
        customers,
        orders,
        order_items,
        products,
        sellers
    ) = load_olist_data()

    # -----------------------------------------------------
    # Prepare orders
    # -----------------------------------------------------

    orders = prepare_orders(
        orders
    )

    # -----------------------------------------------------
    # Sales data
    # -----------------------------------------------------

    sales_data = create_sales_data(
        orders,
        order_items
    )

    # -----------------------------------------------------
    # Monthly business
    # -----------------------------------------------------

    monthly_business = create_monthly_business(
        sales_data
    )

    # -----------------------------------------------------
    # Monthly customer
    # -----------------------------------------------------

    monthly_customer = create_monthly_customer(
        sales_data,
        orders,
        customers
    )

    # -----------------------------------------------------
    # Customer RFM
    # -----------------------------------------------------

    customer_rfm = create_customer_rfm(
        sales_data,
        orders,
        customers
    )

    # -----------------------------------------------------
    # Monthly category
    # -----------------------------------------------------

    monthly_category = create_monthly_category(
        sales_data,
        products
    )

    # -----------------------------------------------------
    # Category KPI
    # -----------------------------------------------------

    category_kpi = create_category_kpi(
        sales_data,
        products
    )

    # -----------------------------------------------------
    # Product KPI
    # -----------------------------------------------------

    product_kpi = create_product_kpi(
        sales_data,
        products
    )

    # -----------------------------------------------------
    # Seller analysis
    # -----------------------------------------------------

    seller_analysis = create_seller_analysis(
        orders,
        order_items,
        sellers
    )

    # -----------------------------------------------------
    # Risky sellers
    # -----------------------------------------------------

    risk_sellers = create_risk_sellers(
        seller_analysis
    )

    # -----------------------------------------------------
    # Daily sales
    # -----------------------------------------------------

    daily_sales = build_daily_sales(
        sales_data
    )

    # -----------------------------------------------------
    # Return all data
    # -----------------------------------------------------

    return {
        "customers": customers,
        "orders": orders,
        "order_items": order_items,
        "products": products,
        "sellers": sellers,
        "sales_data": sales_data,
        "monthly_business": monthly_business,
        "monthly_customer": monthly_customer,
        "customer_rfm": customer_rfm,
        "monthly_category": monthly_category,
        "category_kpi": category_kpi,
        "product_kpi": product_kpi,
        "seller_analysis": seller_analysis,
        "risk_sellers": risk_sellers,
        "daily_sales": daily_sales
    }