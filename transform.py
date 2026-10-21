#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:52:04 2026

@author: hakim
"""
import pyspark.sql.functions as F 
import pyspark.sql.types as T


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


#["Order_ID", "Order_Date", "Customer_ID", "Region", "City", 
#"Segment", "Channel", "Category", "Subcategory"]
#["Product_ID", "Quantity", "Unit_Price_INR", "Discount",
# "Sales_INR", "Discount_Amount_INR", "Net_Sales_INR"]
#["Cost_INR", "Profit_INR", "Shipping_Days", "Returned", 
#"Customer_Satisfaction", "Payment_Method"]


def transform_by_region_product (df): 
    
     df=df.withColumn("Returned",F.when(F.col("Returned") == "Yes" ,1).otherwise(0)) 
    
     df_g = df.groupby("Region","Category",
                      "Subcategory").agg(
                          F.count(F.col("Order_ID")).alias("total Orders"),
                          F.round(F.sum(
                          F.col("Net_Sales_INR")),3).alias("Total Sales"), 
                          F.round(F.sum(
                          F.col("Profit_INR")),3).alias("Total Profit") , 
                          F.sum(F.col("Returned")).alias('Total return'))
   
     df_g=df_g.withColumn("Return rate" , F.round(F.col('Total return')/F.col("total Orders"),4))   
     df_g = df_g.select(
          F.col("Region").cast(T.StringType()),
          F.col("Category").cast(T.StringType()),
          F.col("Subcategory").cast(T.StringType()),
          F.col("Total Sales").cast(T.DecimalType(18, 3)),
          F.col("Total Profit").cast(T.DecimalType(18, 3)),
          F.col("Total return").cast(T.LongType()),
          F.col("Return rate").cast(T.IntegerType()),
)     
     return df_g          
                          
    