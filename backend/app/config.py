import os
from pathlib import Path

# Automatically calculates the exact root directory of your project
ROOT_DIR = Path(__file__).resolve().parent

# Application Configuration
DATA_DIR = os.path.join(ROOT_DIR, "data")

SALES_CSV = os.path.join(DATA_DIR, "Sales.csv")
CUSTOMER_CSV = os.path.join(DATA_DIR, "Customers.csv")
PRODUCTS_CSV = os.path.join(DATA_DIR, "Products.csv")
