#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:43:06 2026

@author: hakim
"""

# test/conftest.py
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("pytest-spse")
        .config("spark.sql.shuffle.partitions", "2")   # accélère les tests
        .config("spark.ui.enabled", "false")           # pas d'UI web
        .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse")
        .getOrCreate()
    )
    yield spark
    spark.stop()