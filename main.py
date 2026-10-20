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
from configration.conf import INPUT_DATA, OUTPUT_DATA


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

        df = clean_data(df, na_policy="avg_")
        df = transform(df)
        log.info("data is cleaned and transformed")

        final_path = write_single_csv(df, OUTPUT_DATA, filename="sales_per_city.csv")
        log.info("data written to %s", final_path)

    except Exception:
        log.exception("ETL failed")
        return 1
    finally:
        spark.stop()

    return 0


if __name__ == "__main__":
    sys.exit(main()) 
    
    
    
  
    