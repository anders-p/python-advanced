import pytest
import pandas as pd
from unittest.mock import patch
from logging import DEBUG
from typing import Literal

# Adjust this import to match where your database code lives
# e.g., from app.database import log_step, DataManager
from app.database import log_step, DataManager


# ==============================================================================
# 1. Tests for log_step (Testing Chained Logger Utilities)
# ==============================================================================


@pytest.mark.parametrize("variant", ["info", "describe", "memory", "head", "verbose"])
def test_log_step_variants_run_without_error(
    variant: Literal["info", "describe", "memory", "head", "verbose"],
):
    """Ensure every variant logs and returns the exact same DataFrame (passthrough testing)."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

    # Asserting passthrough integrity
    result_df = log_step(df, step_name="Test Step", variant=variant)
    pd.testing.assert_frame_equal(result_df, df)


def test_log_step_logs_debug_messages(caplog):
    """Verify that log_step fires debug logs when a step_name is provided."""
    df = pd.DataFrame({"A": [1]})

    # caplog is a built-in pytest fixture that intercepts log capture
    with caplog.at_level(DEBUG):
        log_step(df, step_name="Data Cleansing", variant="verbose")

        # Check that our step header was captured by the logger
        assert (
            "-----------------------Data Cleansing-----------------------"
            in caplog.text
        )


# ==============================================================================
# 2. Tests for DataManager (Testing Merges & Aggregations)
# ==============================================================================


@pytest.fixture
def mock_csv_data():
    """Generates small, controlled dataframes mirroring the production schemas."""
    sales = pd.DataFrame(
        {
            "CustomerKey": [1, 2],
            "ProductKey": [10, 20],
            "OrderDate": ["2026-01-01 00:00:00.000", "2026-01-08 00:00:00.000"],
            "SalesAmount": [100.0, 250.0],
        }
    )
    customers = pd.DataFrame({"CustomerKey": [1, 2], "CustomerName": ["Alice", "Bob"]})
    products = pd.DataFrame(
        {"ProductKey": [10, 20], "ProductName": ["Widget A", "Widget B"]}
    )
    return sales, customers, products


@pytest.fixture
def initialised_manager(mock_csv_data):
    """
    Initialises DataManager by patching pandas.read_csv
    and app.config to use isolated mock test parameters.
    """
    sales_df, customer_df, product_df = mock_csv_data

    # Patch config paths so they don't look for missing files
    with (
        patch("app.config.SALES_CSV", "fake_sales.csv"),
        patch("app.config.CUSTOMER_CSV", "fake_customers.csv"),
        patch("app.config.PRODUCTS_CSV", "fake_products.csv"),
    ):
        # Patch pd.read_csv to return our static mock dataframes sequentially
        with patch("pandas.read_csv") as mock_read:
            mock_read.side_effect = [sales_df, customer_df, product_df]

            manager = DataManager()
            return manager


def test_data_manager_initialisation_merges_correctly(initialised_manager):
    """Verify that tables are correctly merged during class instantiation."""
    dm = initialised_manager

    # Verify the merged dataframe contains columns from all three sources
    assert "CustomerName" in dm.merged_df.columns
    assert "ProductName" in dm.merged_df.columns
    assert "SalesAmount" in dm.merged_df.columns

    # Check shape equality matching the original sales dataframe length
    assert len(dm.merged_df) == 2


@pytest.mark.parametrize(
    "period, expected_rows",
    [
        ("D", 8),  # Split across two different days, 0 in between
        ("W", 2),  # 2026-01-01 and 2026-01-08 fall into separate weekly buckets
        ("ME", 1),  # Both dates fall inside January 2026, combining values
    ],
)
def test_get_sales_data_resampling(
    initialised_manager, period: Literal["D", "W", "ME", "QE", "YE"], expected_rows: int
):
    """Verify that resampling correctly buckets dates and sums the SalesAmount."""
    dm = initialised_manager

    result_df = dm.get_sales_data(period=period)

    # Check that columns conform back to the Bokeh format requirements
    assert list(result_df.columns) == ["OrderDate", "SalesAmount"]
    assert pd.api.types.is_datetime64_any_dtype(result_df["OrderDate"])

    # Verify the count of rows match expected time bucket boundaries
    assert len(result_df) == expected_rows

    # If grouped into a single month (ME), ensure values were summed together ($100 + $250 = $350)
    if period == "ME":
        assert result_df.loc[0, "SalesAmount"] == 350.0
