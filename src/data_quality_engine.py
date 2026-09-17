import pandas as pd


def check_data_quality(df, dataset_name):
    """
    Check basic data quality metrics for a dataset.
    """

    total_rows = len(df)
    total_columns = len(df.columns)

    missing_values = int(df.isnull().sum().sum())

    duplicate_rows = int(df.duplicated().sum())

    missing_percentage = (
        (missing_values / (total_rows * total_columns)) * 100
        if total_rows > 0 and total_columns > 0
        else 0
    )

    if missing_values == 0 and duplicate_rows == 0:
        status = "GOOD"

    elif missing_percentage <= 5:
        status = "WARNING"

    else:
        status = "CRITICAL"

    return {
        "dataset": dataset_name,
        "rows": total_rows,
        "columns": total_columns,
        "missing_values": missing_values,
        "missing_percentage": missing_percentage,
        "duplicate_rows": duplicate_rows,
        "status": status
    }


def generate_data_quality_report(datasets):
    """
    Generate data quality report for multiple datasets.
    """

    results = []

    for dataset_name, df in datasets.items():

        result = check_data_quality(
            df,
            dataset_name
        )

        results.append(result)

    return pd.DataFrame(results)


def get_overall_data_quality_status(report):
    """
    Generate overall data quality status.
    """

    if report.empty:
        return "No data quality information available."

    if (report["status"] == "CRITICAL").any():
        return "CRITICAL"

    elif (report["status"] == "WARNING").any():
        return "WARNING"

    else:
        return "GOOD"


def generate_data_quality_insight(report):
    """
    Generate human-readable data quality insight.
    """

    if report.empty:
        return "No data quality information available."

    overall_status = get_overall_data_quality_status(
        report
    )

    total_missing = int(
        report["missing_values"].sum()
    )

    total_duplicates = int(
        report["duplicate_rows"].sum()
    )

    result = []

    result.append(
        f"🛡️ Overall Data Quality Status: {overall_status}"
    )

    result.append(
        f"Total Missing Values: {total_missing:,}"
    )

    result.append(
        f"Total Duplicate Rows: {total_duplicates:,}"
    )

    result.append("")
    result.append("Dataset Details:")

    for _, row in report.iterrows():

        result.append(
            f"\n{row['dataset']}"
        )

        result.append(
            f"Rows: {row['rows']:,}"
        )

        result.append(
            f"Columns: {row['columns']:,}"
        )

        result.append(
            f"Missing Values: "
            f"{row['missing_values']:,}"
        )

        result.append(
            f"Duplicate Rows: "
            f"{row['duplicate_rows']:,}"
        )

        result.append(
            f"Status: {row['status']}"
        )

    result.append("")

    if overall_status == "GOOD":

        result.append(
            "Recommendation: Data quality is good. "
            "Continue monitoring before dashboard refresh."
        )

    elif overall_status == "WARNING":

        result.append(
            "Recommendation: Review datasets with "
            "missing values or duplicates before using "
            "the data for business analysis."
        )

    else:

        result.append(
            "Recommendation: Fix critical data quality "
            "issues before using the data for business decisions."
        )

    return "\n".join(result)

def get_column_quality_report(df, dataset_name):
    """
    Show missing values and duplicate information
    at column level.
    """

    results = []

    for column in df.columns:

        missing = int(df[column].isnull().sum())

        missing_percentage = (
            (missing / len(df)) * 100
            if len(df) > 0
            else 0
        )

        results.append({
            "dataset": dataset_name,
            "column": column,
            "missing_values": missing,
            "missing_percentage": missing_percentage
        })

    return pd.DataFrame(results)

def interpret_missing_values(df, dataset_name):
    """
    Explain whether missing values are concentrated
    in important or optional columns.
    """

    results = []

    for column in df.columns:

        missing = int(df[column].isnull().sum())

        if missing == 0:
            continue

        percentage = (missing / len(df)) * 100

        results.append({
            "dataset": dataset_name,
            "column": column,
            "missing_values": missing,
            "missing_percentage": percentage,
            "interpretation": (
                "High missing values - review column importance"
                if percentage >= 50
                else "Moderate missing values - review before analysis"
            )
        })

    if not results:
        return pd.DataFrame(
            columns=[
                "dataset",
                "column",
                "missing_values",
                "missing_percentage",
                "interpretation"
            ]
        )

    return pd.DataFrame(results)

def check_duplicate_keys(df, dataset_name, key_columns):
    """
    Check duplicate records based on business key columns.
    """

    results = []

    for key in key_columns:

        if key not in df.columns:
            results.append({
                "dataset": dataset_name,
                "key": key,
                "total_rows": len(df),
                "duplicate_rows": 0,
                "duplicate_percentage": 0,
                "status": "KEY NOT FOUND"
            })
            continue

        duplicate_rows = int(
            df[key].duplicated(keep=False).sum()
        )

        duplicate_percentage = (
            duplicate_rows / len(df) * 100
            if len(df) > 0
            else 0
        )

        if duplicate_rows == 0:
            status = "GOOD"
        elif duplicate_percentage <= 5:
            status = "WARNING"
        else:
            status = "CRITICAL"

        results.append({
            "dataset": dataset_name,
            "key": key,
            "total_rows": len(df),
            "duplicate_rows": duplicate_rows,
            "duplicate_percentage": duplicate_percentage,
            "status": status
        })

    return pd.DataFrame(results)


def generate_duplicate_key_report(dataset_keys):
    """
    Generate duplicate/business-key report
    for multiple datasets.
    """

    results = []

    for dataset_name, df, key_columns in dataset_keys:

        report = check_duplicate_keys(
            df,
            dataset_name,
            key_columns
        )

        results.append(report)

    if not results:
        return pd.DataFrame()

    return pd.concat(
        results,
        ignore_index=True
    )
def check_column_datatypes(df, dataset_name, expected_types):
    """
    Validate important columns against expected data types.

    expected_types example:
    {
        "price": "numeric",
        "order_purchase_timestamp": "datetime",
        "order_id": "string"
    }
    """

    results = []

    for column, expected_type in expected_types.items():

        if column not in df.columns:

            results.append({
                "dataset": dataset_name,
                "column": column,
                "expected_type": expected_type,
                "actual_type": "COLUMN NOT FOUND",
                "invalid_values": 0,
                "status": "KEY NOT FOUND"
            })

            continue

        series = df[column]

        if expected_type == "numeric":

            converted = pd.to_numeric(
                series,
                errors="coerce"
            )

            invalid_values = int(
                converted.isna().sum()
                - series.isna().sum()
            )

        elif expected_type == "datetime":

            converted = pd.to_datetime(
                series,
                errors="coerce"
            )

            invalid_values = int(
                converted.isna().sum()
                - series.isna().sum()
            )

        elif expected_type == "string":

            invalid_values = 0

        else:

            invalid_values = 0

        if invalid_values == 0:
            status = "GOOD"

        elif invalid_values <= 5:
            status = "WARNING"

        else:
            status = "CRITICAL"

        results.append({
            "dataset": dataset_name,
            "column": column,
            "expected_type": expected_type,
            "actual_type": str(series.dtype),
            "invalid_values": invalid_values,
            "status": status
        })

    return pd.DataFrame(results)


def check_date_logic(
    df,
    dataset_name,
    start_column,
    end_column
):
    """
    Check whether end dates occur before start dates.
    """

    if (
        start_column not in df.columns
        or end_column not in df.columns
    ):

        return {
            "dataset": dataset_name,
            "start_column": start_column,
            "end_column": end_column,
            "invalid_date_rows": 0,
            "status": "KEY NOT FOUND"
        }

    start_date = pd.to_datetime(
        df[start_column],
        errors="coerce"
    )

    end_date = pd.to_datetime(
        df[end_column],
        errors="coerce"
    )

    invalid_rows = int(
        (end_date < start_date).sum()
    )

    if invalid_rows == 0:
        status = "GOOD"

    elif invalid_rows <= 5:
        status = "WARNING"

    else:
        status = "CRITICAL"

    return {
        "dataset": dataset_name,
        "start_column": start_column,
        "end_column": end_column,
        "invalid_date_rows": invalid_rows,
        "status": status
    }

def detect_iqr_outliers(df, dataset_name, column):
    """
    Detect outliers in a numeric column using the IQR method.
    """

    if column not in df.columns:
        return {
            "dataset": dataset_name,
            "column": column,
            "q1": None,
            "q3": None,
            "iqr": None,
            "lower_bound": None,
            "upper_bound": None,
            "outlier_count": 0,
            "outlier_percentage": 0,
            "status": "COLUMN NOT FOUND"
        }

    numeric_data = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if numeric_data.empty:
        return {
            "dataset": dataset_name,
            "column": column,
            "q1": None,
            "q3": None,
            "iqr": None,
            "lower_bound": None,
            "upper_bound": None,
            "outlier_count": 0,
            "outlier_percentage": 0,
            "status": "NO NUMERIC DATA"
        }

    q1 = numeric_data.quantile(0.25)
    q3 = numeric_data.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    outliers = numeric_data[
        (numeric_data < lower_bound)
        | (numeric_data > upper_bound)
    ]

    outlier_count = len(outliers)

    outlier_percentage = (
        outlier_count / len(numeric_data) * 100
    )

    if outlier_count == 0:
        status = "GOOD"

    elif outlier_percentage <= 5:
        status = "WARNING"

    else:
        status = "CRITICAL"

    return {
        "dataset": dataset_name,
        "column": column,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outlier_count": outlier_count,
        "outlier_percentage": outlier_percentage,
        "status": status
    }

def generate_master_quality_report(
    datasets,
    datatype_checks=None,
    duplicate_key_checks=None,
    outlier_checks=None,
    date_logic_checks=None
):
    """
    Combine all data quality checks into one master report.
    """

    results = []

    # ---------------------------------------------------------
    # 1. Dataset-level quality
    # ---------------------------------------------------------

    basic_report = generate_data_quality_report(datasets)

    for _, row in basic_report.iterrows():

        results.append({
            "dataset": row["dataset"],
            "check_type": "Basic Quality",
            "check_name": "Missing & Duplicate Rows",
            "issue_count": (
                int(row["missing_values"])
                + int(row["duplicate_rows"])
            ),
            "status": row["status"]
        })

    # ---------------------------------------------------------
    # 2. Datatype checks
    # ---------------------------------------------------------

    if datatype_checks is not None:

        for report in datatype_checks:

            for _, row in report.iterrows():

                results.append({
                    "dataset": row["dataset"],
                    "check_type": "Datatype",
                    "check_name": row["column"],
                    "issue_count": int(
                        row["invalid_values"]
                    ),
                    "status": row["status"]
                })

    # ---------------------------------------------------------
    # 3. Duplicate key checks
    # ---------------------------------------------------------

    if duplicate_key_checks is not None:

        for report in duplicate_key_checks:

            for _, row in report.iterrows():

                results.append({
                    "dataset": row["dataset"],
                    "check_type": "Business Key",
                    "check_name": row["key"],
                    "issue_count": int(
                        row["duplicate_rows"]
                    ),
                    "status": row["status"]
                })

    # ---------------------------------------------------------
    # 4. Outlier checks
    # ---------------------------------------------------------

    if outlier_checks is not None:

        for report in outlier_checks:

            results.append({
                "dataset": report["dataset"],
                "check_type": "Outlier",
                "check_name": report["column"],
                "issue_count": int(
                    report["outlier_count"]
                ),
                "status": report["status"]
            })

    # ---------------------------------------------------------
    # 5. Date logic checks
    # ---------------------------------------------------------

    if date_logic_checks is not None:

        for result in date_logic_checks:

            results.append({
                "dataset": result["dataset"],
                "check_type": "Date Logic",
                "check_name": (
                    f"{result['start_column']} → "
                    f"{result['end_column']}"
                ),
                "issue_count": int(
                    result["invalid_date_rows"]
                ),
                "status": result["status"]
            })

    if not results:
        return pd.DataFrame()

    return pd.DataFrame(results)

def interpret_business_key_issue(
    dataset_name,
    key,
    duplicate_count
):
    """
    Interpret duplicate business keys according
    to the business meaning of each dataset.
    """

    if duplicate_count == 0:
        return {
            "classification": "VALID",
            "severity": "GOOD",
            "explanation": "No duplicate values found."
        }

    # Customers
    if (
        dataset_name == "Customers"
        and key == "customer_unique_id"
    ):
        return {
            "classification": "EXPECTED",
            "severity": "INFO",
            "explanation": (
                "Repeated customer_unique_id values can be "
                "legitimate because the same real customer "
                "may be associated with multiple customer records."
            )
        }

    # Order Items
    if (
        dataset_name == "Order Items"
        and key == "order_id"
    ):
        return {
            "classification": "EXPECTED",
            "severity": "INFO",
            "explanation": (
                "An order can contain multiple items, so "
                "the same order_id can legitimately appear "
                "multiple times."
            )
        }

    # Order item sequence number
    if (
        dataset_name == "Order Items"
        and key == "order_item_id"
    ):
        return {
            "classification": "EXPECTED",
            "severity": "INFO",
            "explanation": (
                "order_item_id is an item sequence within "
                "an order and should not be treated as a "
                "globally unique identifier."
            )
        }

    # Everything else
    return {
        "classification": "INVESTIGATE",
        "severity": "WARNING",
        "explanation": (
            "Duplicate values were found in a business key "
            "and should be investigated."
        )
    }

def add_business_interpretation(master_quality_report):
    """
    Add business interpretation to business-key quality findings.
    Expected repetitions are separated from issues requiring investigation.
    """

    report = master_quality_report.copy()

    report["business_interpretation"] = "VALID"

    for index, row in report.iterrows():

        if row["check_type"] != "Business Key":
            continue

        interpretation = interpret_business_key_issue(
            row["dataset"],
            row["check_name"],
            row["issue_count"]
        )

        report.at[
            index,
            "business_interpretation"
        ] = interpretation["classification"]

    return report