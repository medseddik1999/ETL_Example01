# config/configuration.py
from pathlib import Path


# config/configuration.py  →  parent = config/  →  parent = SpSe/
CONFIG_DIR  = Path(__file__).resolve().parent          # …/SpSe/config
PROJECT_DIR = CONFIG_DIR.parent                        # …/SpSe

INPUT_DATA  = PROJECT_DIR / "data" / "sales_data.csv"  # …/SpSe/data/sales_data.csv
OUTPUT_DATA_CITIES = PROJECT_DIR / "output" /"output_cities"     # …/SpSe/output
OUTPUT_DATA_RP = PROJECT_DIR /"output" /"output_region_products" 



EXPECTED_COLUMNS = [
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Region",
    "City",
    "Segment",
    "Channel",
    "Category",
    "Subcategory",
    "Product_ID",
    "Quantity",
    "Unit_Price_INR",
    "Discount",
    "Sales_INR",
    "Discount_Amount_INR",
    "Net_Sales_INR",
    "Cost_INR",
    "Profit_INR",
    "Shipping_Days",
    "Returned",
    "Customer_Satisfaction",
    "Payment_Method",
]





