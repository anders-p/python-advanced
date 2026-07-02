"""
Tests for the main api
"""

from fastapi.testclient import TestClient
import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from app.main import app


### FIXTURES
# Mock the sales dataframe returned by database.py
@pytest.fixture
def mock_sales_df():
    """Generates a fake pandas dataframe to mimic what DataManager returns."""
    return pd.DataFrame(
        {
            "OrderDate": pd.date_range(start="2026-01-01", periods=5, freq="W"),
            "SalesAmount": [100, 150, 200, 250, 300],
        }
    )


# Create a TestClient to trigger lifespan events in the API
@pytest.fixture
def client(mock_sales_df):
    """
    Creates a FastAPI TestClient that cleanly triggers the lifespan
    events and replaces the real DataManager with a mock version.
    """

    # Mock DataManager class before entering lifespan
    with patch("app.main.DataManager") as MockDataManagerClass:
        # Create instance
        mock_instance = MagicMock()

        # Force the mock's get_sales_data method to return the fake values
        mock_instance.get_sales_data.return_value = mock_sales_df

        # Return this mock instance when main.py calls DataManager()
        MockDataManagerClass.return_value = mock_instance

        # Open TestClient (using 'with' block forces FastAPI to execute lifespan)
        with TestClient(app) as test_client:
            yield test_client


### TEST CASES
def test_get_sales_chart_default_period(client):
    """Test endpoint returns valid Bokeh JSON with default parameters"""
    # Send GET request
    response = client.get("/chart/sales")

    # Assert HTTP response
    assert response.status_code == 200

    # Parse json response
    json_data = response.json()

    # Assert JSON structure is output
    assert "target_id" in json_data
    assert json_data["target_id"] == "bokeh-chart"
    assert "doc" in json_data
    assert "roots" in json_data["doc"]


def test_get_sales_chart_query_parameters(client):
    """Test passing different valid periods"""
    valid_periods = ["D", "W", "ME", "QE", "YE"]

    for period in valid_periods:
        # Send request with explicit query
        response = client.get(f"/chart/sales?period={period}")

        assert response.status_code == 200

        # Parse json response
        json_data = response.json()

        # Check that JSON response is valid Bokeh graph
        assert "target_id" in json_data
        assert json_data["target_id"] == "bokeh-chart"
        assert "doc" in json_data
        assert "roots" in json_data["doc"]


def test_invalid_period_fails_validation(client):
    """Test response from invalid query parameters"""
    # Pass an invalid query
    response = client.get("/chart/sales?period=INVALID")

    # Assert 422 error code (unprocessable content)
    assert response.status_code == 422


def test_invalid_query_parameters(client):
    """Test response from invalid query parameters"""
    invalid_queries = [
        "period=INVALID_STR",
        "period=7",
    ]

    for query in invalid_queries:
        # Pass an invalid query
        response = client.get(f"/chart/sales?{query}")

        # Assert 422 error code (unprocessable content)
        assert response.status_code == 422


def test_invalid_endpoint(client):
    """Test response from an undefined endpoint"""
    response = client.get("/undefined")

    # Assert 404 returned
    assert response.status_code == 404
