#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import logging
import os
import shutil
import sys

from pyspark.sql import SparkSession
from extract import read_data
from clean import clean_data
from transform import transform
from configration.conf import INPUT_DATA, OUTPUT_DATA_FINANCE
from monthly_kpi import calculate_monthly_kpi

log = logging.getLogger(__name__)


def write_single_csv(df, out_dir: str, filename: str = "sales_per_city.csv") -> str:
    """Write df as one CSV at out_dir/filename. Returns final file path."""
    out_dir = str(out_dir)

    # One partition -> one part file
    (df.coalesce(1)
       .write
       .mode("overwrite")
       .option("header", True)
       .csv(out_dir))

    parts = glob.glob(os.path.join(out_dir, "part-*.csv"))
    if len(parts) != 1:
        raise RuntimeError(f"expected 1 part file, got {len(parts)} in {out_dir}")

    final_path = os.path.join(out_dir, filename)
    shutil.move(parts[0], final_path)

    success = os.path.join(out_dir, "_SUCCESS")
    if os.path.exists(success):
        os.remove(success)

    return final_path


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    spark = SparkSession.builder.appName("sales").getOrCreate()
    try:
        log.info("ETL process is starting")
        df = read_data(INPUT_DATA, spk=spark)
        log.info("extraction is done")
        print("--raw data")
        #df.show(20, truncate=False)

        df = clean_data(df, na_policy="avg_")
        print("--cleaned data")
        #df.show(20, truncate=False)
        #df.printSchema()

        print("--Monthly financial KPI")
        monthly_df = calculate_monthly_kpi(df)
        monthly_df.show(20, truncate=False)
        final_path3 = write_single_csv(monthly_df, OUTPUT_DATA_FINANCE, filename="monthly_financial_kpi.csv")
        log.info("Fichier généré : %s", final_path3)

        #df = transform(df)
        #log.info("data is cleaned and transformed")

    except Exception:
        log.exception("ETL failed")
        return 1
    finally:
        spark.stop()

    return 0


if __name__ == "__main__":
    sys.exit(main()) 