import os
from pathlib import Path

# Automatically calculates the exact root directory of your project
ROOT_DIR = Path(__file__).resolve().parent

# Application Configuration
DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    (
        Path("C:/")
        / "Users"
        / "Administrator"
        / "Desktop"
        / "2026-06 - Python_Advanced"
        / "sql-server-samples"
        / "samples"
        / "databases"
        / "adventure-works"
        / "data-warehouse-install-script"
    ),
)
SALES_CSV = os.getenv("SALES_CSV", "FactInternetSales.csv")
CUSTOMER_CSV = os.getenv("CUSTOMER_CSV", "DimCustomer.csv")
PRODUCTS_CSV = os.getenv("PRODUCTS_CSV", "DimProduct.csv")

SAVE_DIRECTORY = os.path.join(ROOT_DIR, "data")


# def load_config(config_path: str = 'config.json'):
#     with open(config_path, 'r', encoding='utf-8') as file:
#         # Load data from JSON file
#         config = dict(json.load(file))

#         # Convert path strings to os-specific path variables
#         config['database_path'] = Path(config['database_path'])

#         return config

# if __name__ == "__main__":
#     print(load_config())
