#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:52:04 2026

@author: hakim
"""
import pyspark.sql.functions as F 



def transform (df): 
    df_1= df.groupby('city').agg(
    F.count(F.col('Order_ID')).alias('total orders'), 
    F.round(F.sum(F.col('Sales_INR')),2).alias('Brut sales'), 
    F.round(F.sum(F.col('Net_Sales_INR')),2).alias('Net Sales'), 
    F.round(F.sum(F.col('Profit_INR')),2).alias('Profit')  
).orderBy(F.desc(F.col('Profit')))  
    df_2= df.groupby('city').agg(
    F.count_distinct('Product_ID').alias('Num de produit'),
    F.round(F.avg(F.col('Unit_Price_INR')),2).alias('Avg unit price'))  
    
    df_1=df_1.join(df_2, how='left' ,on = 'city' )   
    
    return df_2 


