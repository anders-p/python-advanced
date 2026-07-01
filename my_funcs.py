import os
import pandas as pd

import config
import sqlHeaders as headers


def download_data(
    file_name: str,
    folder_path: str,
    column_headers: list[str] | None = None,
    delimiter: str = "|",
) -> pd.DataFrame:
    """Fetch data and return as a dataframe"""

    # Join file path together and read data into dataframe
    file_path = os.path.join(folder_path, file_name)
    df = pd.read_csv(file_path, header=None, sep=delimiter)

    # Apply headers if provided
    if column_headers:
        df.columns = column_headers

    return df


def process_data(df: pd.DataFrame, cols: list[str] | None) -> pd.DataFrame:
    """Clean sales data"""

    # Extract columns if provided
    if cols:
        df = df[cols]

    return df


def email_report(df: pd.DataFrame) -> None:
    """Summarise data and send an email report"""
    # Add total column
    df["TotalPrice"] = df["OrderQuantity"] * df["UnitPrice"]

    # Send the email with the summary
    print("Email summary:")

    print(f"{df['CustomerKey'].nunique()} unique customers bought items today.")
    print(f"The total sales for today were ${round(df['TotalPrice'].sum(), 2)}")
    return


# Workflow orchestration
def run_daily_report():
    sales_df = download_data(
        file_name=config.SALES_CSV,
        folder_path=config.DATABASE_PATH,
        column_headers=headers.fact_internet_sales,
    )

    customer_df = download_data(
        file_name=config.CUSTOMER_CSV,
        folder_path=config.DATABASE_PATH,
        column_headers=headers.dim_customer,
    )

    product_df = download_data(
        file_name=config.PRODUCTS_CSV,
        folder_path=config.DATABASE_PATH,
        column_headers=headers.dim_product,
    )

    sales_df.to_csv(os.path.join(config.SAVE_DIRECTORY, "Sales.csv"), index=False)
    customer_df.to_csv(
        os.path.join(config.SAVE_DIRECTORY, "Customers.csv"), index=False
    )
    product_df.to_csv(os.path.join(config.SAVE_DIRECTORY, "Products.csv"), index=False)

    # customer_df = process_data(
    #     sales_df, cols=["CustomerKey", "OrderQuantity", "UnitPrice"]
    # )
    # email_report(customer_df)


if __name__ == "__main__":
    run_daily_report()
