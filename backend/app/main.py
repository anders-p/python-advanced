from bokeh.embed import json_item
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from typing import Literal

from database import DataManager

logging.basicConfig(
    level=logging.DEBUG,  # Capture INFO, WARNING, ERROR, and CRITICAL logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),  # Log to a file
        logging.StreamHandler(),  # Log to the console
    ],
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs EXACTLY ONCE when the server starts up
    logger.info("Initializing DataManager and loading CSVs...")

    # Attach data_manager to the app's state dictionary
    app.state.data_manager = DataManager()

    yield  # The application runs while paused here

    # This code runs EXACTLY ONCE when the server shuts down
    logger.info("Shutting down application...")
    del app.state.data_manager


app = FastAPI(title="Bokeh Data Streamer", lifespan=lifespan)

# Configure CORS so your React/Next.js frontend can safely fetch the data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/chart/sales")
def get_sales_chart(
    period: Literal["D", "W", "ME", "QE", "YE"] = "W",
):
    """Generates a chart of sales data and exports it as a JSON payload"""
    logger.info(f"Getting chart of sales with {period} frequency")

    ### TEMP dict for readable periods
    period_dict = {
        "D": "Day",
        "W": "Week",
        "ME": "Month",
        "QE": "Quarter",
        "YE": "Year",
    }

    period_seconds = {
        "D": 86400000,
        "W": 604800000,
        "ME": 2.628e9,
        "QE": 7.884e9,
        "YE": 3.154e10,
    }

    sales_df = app.state.data_manager.get_sales_data(period=period)

    logger.debug(sales_df)

    logger.info("Converting data into bokeh plot")

    plot_source = ColumnDataSource(sales_df)

    p = figure(
        title=f"Sales per {period_dict[period]}",
        x_axis_type="datetime",
        x_axis_label=f"{period_dict[period]}",
        y_axis_label="Total Sales Amount",
        width=600,
        height=400,
    )

    # Convert to histogram
    p.vbar(
        x="OrderDate",
        top="SalesAmount",
        source=plot_source,
        width=period_seconds[period],
        fill_color="navy",
        # line_color="green",
    )

    # Serialise into JSON format
    chart_json = json_item(p, target="bokeh-chart")

    # Return data
    logger.info("Returning chart to user")
    return JSONResponse(content=chart_json)


# @app.get("/api/chart-data")
# def get_bokeh_chart():
#     """Generates an interactive Bokeh chart and exports it as a JSON payload."""
#     # 1. Create a dummy Pandas DataFrame mimicking real application data
#     data = {
#         "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
#         "sales": [100, 103, 50, 340, 100, 105, 69],
#     }
#     df = pd.DataFrame(data)

#     # 2. Initialize a Bokeh canvas figure with standard user tools
#     p = figure(
#         title="Weekly Sales Analytics Overview",
#         x_range=df["days"].tolist(),  # Sets categorical x-axis line items
#         height=400,
#         width=700,
#         tools="pan,wheel_zoom,box_zoom,reset,save",
#     )

#     # 3. Plot the data line and circular pointer data markers
#     p.line(
#         x="days",
#         y="sales",
#         source=df,
#         line_width=3,
#         color="#3B82F6",  # Clean modern blue accent color
#     )
#     p.circle(x="days", y="sales", source=df, size=8, color="#1D4ED8")

#     # 4. Standardize axis styling formats
#     p.xaxis.axis_label = "Day of the Week"
#     p.yaxis.axis_label = "Total Income ($)"

#     # 5. Serialize into the specialized JSON format for BokehJS to read
#     # Crucial: The ID target string must match your frontend HTML div container ID
#     chart_json = json_item(p, target="bokeh-chart")

#     return JSONResponse(content=chart_json)

if __name__ == "__main__":
    import uvicorn

    # Launch the server locally on port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
