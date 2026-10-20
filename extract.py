#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 10:41:06 2026

@author: abdelhakim
"""
from configration.conf import INPUT_DATA, EXPECTED_COLUMNS


def read_data(source=INPUT_DATA, spk=None, colls=EXPECTED_COLUMNS):
    if spk is None:
        raise ValueError("A SparkSession 'spk' must be provided.")

    df = spk.read.csv(str(source), header=True, inferSchema=True)

    # Columns missing from the DataFrame (expected but not present)
    missing = [c for c in colls if c not in df.columns]
    if missing:
        raise KeyError(
            f"Missing expected column(s): {missing}. "
            f"DataFrame has: {df.columns}"
        )

    # (Optional) unexpected extra columns in the DataFrame
    unexpected = [c for c in df.columns if c not in colls]
    if unexpected:
        print(f"Warning: unexpected extra columns: {unexpected}")

    print("Data Loaded")
    return df 



