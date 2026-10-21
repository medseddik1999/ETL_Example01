from pyspark.sql import functions as F
from pyspark.sql.window import Window


def calculate_monthly_kpi(df):

    # Création de la colonne mois
    df = df.withColumn(
        "month",
        F.date_format("Order_Date", "yyyy-MM")
    )

    # regrouper les ventes par mois
    monthly_df = (
        df.groupBy("month")
          .agg(
              F.round(F.sum("Sales_INR"), 2).alias("revenue"),
              F.round(F.sum("Discount_Amount_INR"), 2).alias("discounts"),
              F.round(F.sum("Cost_INR"), 2).alias("costs"),
              F.round(F.sum("Profit_INR"), 2).alias("profits"),
              F.countDistinct("Order_ID").alias("orders")
          )
    )

    # calcul de la marge (%) = profit / CA
    monthly_df = monthly_df.withColumn(
        "margin(%)",
        F.when(
            F.col("revenue") != 0,
            F.round(
                (F.col("profits") / F.col("revenue")) * 100,
                2
            )
        ).otherwise(0)
    )

    # Panier moyen = CA / nombre de commandes
    monthly_df = monthly_df.withColumn(
        "avg_basket",
        F.when(
            F.col("orders") != 0,
            F.round(
                F.col("revenue") / F.col("orders"),
                2
            )
        ).otherwise(0)
    )

    # comparaison avec le mois précédent
    window_spec = Window.orderBy("month")

    monthly_df = monthly_df.withColumn(
        "previous_revenue",
        F.lag("revenue").over(window_spec)
    )

    # Evolution du CA (%)
    monthly_df = monthly_df.withColumn(
        "revenue_growth(%)",
        F.when(
            (F.col("previous_revenue").isNotNull()) &
            (F.col("previous_revenue") != 0),
            F.round(
                (
                    (F.col("revenue") - F.col("previous_revenue"))
                    / F.col("previous_revenue")
                ) * 100,
                2
            )
        ).otherwise(None)
    )

    # Suppression de la colonne intermédiaire
    monthly_df = monthly_df.drop("previous_revenue")

    # Tri chronologique
    monthly_df = monthly_df.orderBy("month")

    return monthly_df