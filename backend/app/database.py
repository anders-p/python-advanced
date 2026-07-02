"""
Functions for manipulating the CSV database
"""

import logging
import pandas as pd
from typing import Literal

from app import config

logger = logging.getLogger(__name__)


def log_step(
    df: pd.DataFrame,
    step_name: str | None = None,
    variant: Literal["info", "describe", "memory", "head", "verbose"] = "info",
) -> pd.DataFrame:
    """Print a dataframe during a chained method"""
    if step_name:
        logger.debug(f"-----------------------{step_name}-----------------------")

    match variant:
        case "info":
            logger.debug(df.info())
        case "describe":
            logger.debug(df.describe())
        case "memory":
            logger.debug(df.memory_usage(deep=True))
        case "head":
            logger.debug(df.head())
        case "verbose":
            logger.debug(df)
    return df


class DataManager:
    def __init__(self):
        """
        Load the data from memory
        """
        logger.info("Loading CSVs...")

        self.sales_df = pd.read_csv(config.SALES_CSV)
        self.customer_df = pd.read_csv(config.CUSTOMER_CSV)
        self.product_df = pd.read_csv(config.PRODUCTS_CSV)

        logger.info("Merging tables...")

        # Merge dataframes with sales on the left
        self.merged_df = (
            self.sales_df.copy()
            .merge(self.customer_df, how="left", on="CustomerKey")
            .merge(self.product_df, how="left", on="ProductKey")
        )

        logger.info("Data successfully loaded")

    def get_sales_data(
        self,
        period: Literal["D", "W", "ME", "QE", "YE"] = "W",
    ):
        """
        Get sales data over a period of time selected by the user
        """

        logger.info("Getting sales data...")

        # Extract sales data
        sales_df = self.merged_df.copy().filter(items=["OrderDate", "SalesAmount"])

        # Convert date to datetime
        sales_df["OrderDate"] = pd.to_datetime(
            sales_df["OrderDate"], format="%Y-%m-%d %H:%M:%S.%f"
        )

        # Set index to datetime, and group by time period
        ### TODO: Let user select time-period
        sales_df = (
            sales_df.set_index("OrderDate")
            .resample(period)["SalesAmount"]
            .sum()
            .reset_index()
        )

        logger.info("Sales data retrieved")

        return sales_df
