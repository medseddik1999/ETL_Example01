#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:09:26 2026

@author: hakim
"""

from pyspark.sql.types import StringType , IntegerType ,DoubleType
import pyspark.sql.functions as F 


def clean_data(df=None, na_policy='avg_'):
    if df is None:
        raise ValueError('data is not loaded in the cleaning function')

    for field in df.schema.fields:
        col = field.name

        if isinstance(field.dataType, StringType):
            df = df.withColumn(
                col,
                F.when(
                    F.trim(F.col(col)).isNull() | (F.trim(F.col(col)) == ''),
                    'No Value'
                ).otherwise(F.trim(F.col(col)))
            )

        elif isinstance(field.dataType, DoubleType) and na_policy == 'avg_':
            # compute mean once
            mean_val = df.select(F.avg(F.col(col))).collect()[0][0]
            if mean_val is not None:
                df = df.withColumn(
                    col,
                    F.when(F.col(col).isNull(), F.lit(mean_val))
                     .otherwise(F.col(col))
                )
            else:
                # whole column null -> fall back to 0 or 'No Value'
                df = df.withColumn(
                    col,
                    F.when(F.col(col).isNull(), F.lit(0.0))
                     .otherwise(F.col(col))
                )

        elif isinstance(field.dataType, DoubleType) and na_policy == 'delet_':
            df = df.filter(F.col(col).isNotNull())

    df = df.dropDuplicates()
    return df
        
           
            
            
        