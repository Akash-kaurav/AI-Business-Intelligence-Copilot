# =========================================================
# BUSINESS INTENT ROUTER
# =========================================================

def detect_business_intent(question):
    """
    Detect the main business intent from a user's question.

    Priority is important because some questions contain
    multiple business keywords.

    Example:
    "What is the revenue forecast?"
    contains both revenue and forecast,
    but the correct intent is forecast.
    """

    if question is None:
        return "unknown"

    question = str(question).lower().strip()

    if not question:
        return "unknown"


    # =====================================================
    # 1. DATA QUALITY
    # =====================================================

    if (
        "data quality" in question
        or "quality issue" in question
        or "quality issues" in question
        or "data issue" in question
        or "data issues" in question
        or "data problem" in question
        or "data problems" in question
        or "dataset quality" in question
        or "quality report" in question
    ):
        return "data_quality"


    # =====================================================
    # 2. FORECAST
    # =====================================================

    if (
        "forecast" in question
        or "predict" in question
        or "prediction" in question
        or "tomorrow" in question
        or "next day" in question
        or "future revenue" in question
    ):
        return "forecast"


    # =====================================================
    # 3. CUSTOMER
    # =====================================================

    if (
        "customer" in question
        or "customers" in question
        or "vip" in question
        or "retention" in question
        or "at risk" in question
        or "lost customer" in question
        or "lost customers" in question
        or "customer priority" in question
        or "prioritize customer" in question
        or "prioritize customers" in question
    ):
        return "customer"


    # =====================================================
    # 4. PRODUCT
    # =====================================================

    if (
        "product" in question
        or "products" in question
        or "business winner" in question
        or "business winners" in question
        or "high demand" in question
    ):
        return "product"


    # =====================================================
    # 5. CATEGORY
    # =====================================================

    if (
        "category" in question
        or "categories" in question
    ):
        return "category"


    # =====================================================
    # 6. SELLER
    # =====================================================

    if (
        "seller" in question
        or "sellers" in question
        or "vendor" in question
        or "vendors" in question
    ):
        return "seller"


    # =====================================================
    # 7. REVENUE
    # =====================================================

    if (
        "revenue" in question
        or "sales" in question
        or "income" in question
        or "earning" in question
    ):
        return "revenue"


    # =====================================================
    # 8. UNKNOWN
    # =====================================================

    return "unknown"