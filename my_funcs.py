import os
import pandas as pd

import sqlHeaders as headers

### TEMP config
CONFIG = {
    "database_path": r"C:\Users\Administrator\Desktop\2026-06 - Python_Advanced\sql-server-samples\samples\databases\adventure-works\data-warehouse-install-script",
    "sales_csv": "FactInternetSales.csv",
}


def download_sales_data(
    file_name: str, folder_path: str = CONFIG["database_path"], delimiter: str = "|"
):
    """Fetch sales data and return as a dataframe"""

    file_path = os.path.join(folder_path, file_name)

    print(file_path)

    df = pd.read_csv(file_path, header=None, sep=delimiter)

    return df


def process_data(df: pd.DataFrame, cols: list[str] | None):
    """Clean sales data"""
    # Add headers
    df.columns = headers.fact_internet_sales

    # Extract columns if provided
    if cols:
        df = df[cols]

    return df


def email_report(df: pd.DataFrame):
    # Add total column
    df["TotalPrice"] = df["OrderQuantity"] * df["UnitPrice"]

    # Send the email with the summary
    print("Email summary:")

    print(f"{df['CustomerKey'].nunique()} unique customers bought items today.")
    print(f"The total sales for today were ${round(df['TotalPrice'].sum(), 2)}")
    return "Hello"


# Workflow orchestration
def run_daily_report():
    sales_df = download_sales_data(file_name=CONFIG["sales_csv"])
    customer_df = process_data(
        sales_df, cols=["CustomerKey", "OrderQuantity", "UnitPrice"]
    )
    print(customer_df)
    email_report(customer_df)


if __name__ == "__main__":
    run_daily_report()
    # print(download_sales_data())
