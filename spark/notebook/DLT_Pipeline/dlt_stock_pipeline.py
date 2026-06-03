from pyspark import pipelines as dp
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window

raw_path = "/Volumes/jarvis_training/default/stock_api"

daily_schema = StructType([
    StructField("symbol", StringType()),
    StructField("trade_date", StringType()),
    StructField("open", StringType()),
    StructField("high", StringType()),
    StructField("low", StringType()),
    StructField("close", StringType()),
    StructField("volume", StringType())
])

@dp.table(
    comment="Raw daily stock data from Alpha Vantage API."
)
def daily_stock_bronze():
    return (
        spark.readStream
        .format("cloudFiles")
        .schema(daily_schema)
        .option("cloudFiles.format", "json")
        .load(f"{raw_path}/daily")
    )

@dp.table(
    comment="Raw latest quote data from Alpha Vantage API."
)
def quote_bronze():
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load(f"{raw_path}/quote")
    )

@dp.table(
    comment="Raw company information from Alpha Vantage API."
)
def company_info_bronze():
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load(f"{raw_path}/company")
    )

@dp.materialized_view(
    comment="Cleaned daily stock data."
)
def daily_stock_silver():
    return (
        spark.read.table("daily_stock_bronze")
        .select(
            col("symbol"),
            to_date("trade_date").alias("trade_date"),
            col("open").cast("double").alias("open_price"),
            col("high").cast("double").alias("high_price"),
            col("low").cast("double").alias("low_price"),
            col("close").cast("double").alias("close_price"),
            col("volume").cast("long").alias("volume")
        )
    )

@dp.materialized_view(
    comment="Cleaned latest quote data."
)
def quote_silver():
    return (
        spark.read.table("quote_bronze")
       .select(
            col("symbol"),
            col("price").cast("double").alias("latest_price"),
            col("volume").cast("long").alias("latest_volume"),
            to_date(col("latest_trading_day")).alias("latest_trading_day"),
            col("previous_close").cast("double").alias("previous_close"),
            col("price_change").cast("double").alias("price_change"),
            regexp_replace(col("change_percent"), "%", "").cast("double").alias("change_percent")
       )
    )

@dp.materialized_view(
    comment="Cleaned company information."
)
def company_info_silver():
    return (
        spark.read.table("company_info_bronze")
         .select(
            col("symbol"),
            col("company_name"),
            col("sector"),
            col("industry"),
            col("market_cap").cast("long").alias("market_cap"),
            col("country"),
            col("exchange")
        )
    )

@dp.materialized_view(
    comment="Daily stock data enriched with company information."
)
def stock_enriched_silver():
    return (
        spark.read.table("daily_stock_silver")
        .join(spark.read.table("company_info_silver"), "symbol", "left")
    )

@dp.materialized_view(
    comment="Price trend analysis over 7, 30, and 90 days."
)
def price_trend_gold():
    df = spark.read.table("stock_enriched_silver")
    w = Window.partitionBy("symbol").orderBy("trade_date")

    return (
        df
        .withColumn("price_7d_ago", lag("close_price", 7).over(w))
        .withColumn("price_30d_ago", lag("close_price", 30).over(w))
        .withColumn("price_90d_ago", lag("close_price", 90).over(w))
        .withColumn("price_change_7d", col("close_price") - col("price_7d_ago"))
        .withColumn("price_change_30d", col("close_price") - col("price_30d_ago"))
        .withColumn("price_change_90d", col("close_price") - col("price_90d_ago"))
        .withColumn("price_pct_change_7d", round(col("price_change_7d") / col("price_7d_ago") * 100, 2))
        .withColumn("price_pct_change_30d", round(col("price_change_30d") / col("price_30d_ago") * 100, 2))
        .withColumn("price_pct_change_90d", round(col("price_change_90d") / col("price_90d_ago") * 100, 2))
    )

@dp.materialized_view(
    comment="Volume trend analysis over 7, 30, and 90 days."
)
def volume_trend_gold():
    df = spark.read.table("stock_enriched_silver")

    w7 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-6, 0)
    w30 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-29, 0)
    w90 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-89, 0)

    return (
        df
        .withColumn("avg_volume_7d", avg("volume").over(w7))
        .withColumn("avg_volume_30d", avg("volume").over(w30))
        .withColumn("avg_volume_90d", avg("volume").over(w90))
    )