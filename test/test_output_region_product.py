# test/test_output_types.py
from pathlib import Path

import pytest
from pyspark.sql.types import (
    StringType,
    LongType,
    DoubleType,
    DecimalType, 
    IntegerType
)


OUTPUT_DIR = Path(__file__).parent.parent / "output" / "output_region_products"


@pytest.fixture(scope="module")
def output_df(spark):
    """Charge le dataset de sortie existant."""
    files = list(OUTPUT_DIR.glob("*.csv"))
    assert files, f"Aucun CSV trouvé dans {OUTPUT_DIR}"

    return (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(str(OUTPUT_DIR))
    )
@pytest.fixture(scope="module")
def fields(output_df):
    """Dictionnaire {nom_colonne: StructField} pour accès direct au dataType."""
    return {f.name: f for f in output_df.schema.fields}


# ---------- Tests avec isinstance() ----------

def test_region_is_string(fields):
    assert isinstance(fields["Region"].dataType, StringType)


def test_category_is_string(fields):
    assert isinstance(fields["Category"].dataType, StringType)


def test_subcategory_is_string(fields):
    assert isinstance(fields["Subcategory"].dataType, StringType)


def test_total_sales_is_numeric(fields):
    assert isinstance(fields["Total Sales"].dataType, (DoubleType, DecimalType))


def test_total_profit_is_numeric(fields):
    assert isinstance(fields["Total Profit"].dataType, (DoubleType, DecimalType))


def test_total_return_is_long(fields):
    assert isinstance(fields["Total return"].dataType, IntegerType)


def test_return_rate_is_double(fields):
    assert isinstance(fields["Return rate"].dataType, DoubleType)