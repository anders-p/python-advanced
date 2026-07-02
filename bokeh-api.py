import logging
from bokeh.embed import json_item
from bokeh.plotting import figure
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Literal

logging.basicConfig(
    level=logging.DEBUG,  # Capture INFO, WARNING, ERROR, and CRITICAL logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),  # Log to a file
        logging.StreamHandler(),  # Log to the console
    ],
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Bokeh Data Streamer")

# Configure CORS so your React/Next.js frontend can safely fetch the data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def log_step(
    df: pd.DataFrame,
    step_name: str | None = None,
    variant: Literal["info", "describe", "memory", "head", "verbose"] = "info",
) -> pd.DataFrame:
    """Print a dataframe during a chained method"""
    if step_name:
        logger.info(f"-----------------------{step_name}-----------------------")

    match variant:
        case "info":
            logger.info(df.info())
        case "describe":
            logger.info(df.describe())
        case "memory":
            logger.info(df.memory_usage(deep=True))
        case "head":
            logger.info(df.head())
        case "verbose":
            logger.info(df)
    return df


@app.get("/api/chart-data")
def get_bokeh_chart():
    """Generates an interactive Bokeh chart and exports it as a JSON payload."""
    # 1. Create a dummy Pandas DataFrame mimicking real application data
    data = {
        "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "sales": [100, 103, 50, 340, 100, 105, 69],
    }
    df = pd.DataFrame(data)

    # 2. Initialize a Bokeh canvas figure with standard user tools
    p = figure(
        title="Weekly Sales Analytics Overview",
        x_range=df["days"].tolist(),  # Sets categorical x-axis line items
        height=400,
        width=700,
        tools="pan,wheel_zoom,box_zoom,reset,save",
    )

    # 3. Plot the data line and circular pointer data markers
    p.line(
        x="days",
        y="sales",
        source=df,
        line_width=3,
        color="#3B82F6",  # Clean modern blue accent color
    )
    p.circle(x="days", y="sales", source=df, size=8, color="#1D4ED8")

    # 4. Standardize axis styling formats
    p.xaxis.axis_label = "Day of the Week"
    p.yaxis.axis_label = "Total Income ($)"

    # 5. Serialize into the specialized JSON format for BokehJS to read
    # Crucial: The ID target string must match your frontend HTML div container ID
    chart_json = json_item(p, target="bokeh-chart")

    return JSONResponse(content=chart_json)


if __name__ == "__main__":
    import uvicorn

    # Launch the server locally on port 8000
    uvicorn.run("bokeh-api:app", host="127.0.0.1", port=8000, reload=True)
