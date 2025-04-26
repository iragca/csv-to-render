import polars as pl
from sqlalchemy import inspect

from src.config import DATA_PATH, logger
from src.db import initdb
from src.dml import INSERT


def main():
    # Initialize the database engine with the corresponding configuration and
    # create the necessary tables.
    ENGINE = initdb()

    # Instantiate the necessary Data Manipulation Language (DML) classes for
    # database operations, both classes take the configured engine as an argument.
    insert = INSERT(ENGINE)

    # Define the conversion ratio from Canadian dollars to US dollars.
    CANADA_USD_RATIO = 0.76

    # Read the sales data from CSV files.
    logger.info("Reading sales data...")
    canada_sales = pl.read_csv(
        DATA_PATH / "canada_sales.csv", infer_schema_length=10000
    )
    usa_sales = pl.read_csv(DATA_PATH / "usa_sales.csv", infer_schema_length=10000)

    # Clean the Canada sales data.
    logger.info("Cleaning sales data...")
    canada_sales_fix = (
        canada_sales.drop_nulls()
        .filter(pl.col("Price Each") != "Price Each")
        .with_columns(
            [
                pl.col("Price Each").cast(pl.Float64),
            ]
        )
        .with_columns(
            [
                pl.col("Price Each") * CANADA_USD_RATIO,
                pl.col("Order ID").cast(pl.Int64),
                pl.col("Quantity Ordered").cast(pl.Int64),
                pl.col("Order Date").str.strptime(pl.Datetime, "%m/%d/%y %H:%M"),
            ]
        )
    )

    # Clean the USA sales data.
    usa_sales_fix = (
        usa_sales.drop_nulls()
        .filter(pl.col("Price Each") != "Price Each")
        .with_columns(
            [
                pl.col("Price Each").cast(pl.Float64),
                pl.col("Order ID").cast(pl.Int64),
                pl.col("Quantity Ordered").cast(pl.Int64),
                pl.col("Order Date").str.strptime(pl.Datetime, "%m/%d/%y %H:%M"),
            ]
        )
    )


    # Insert the cleaned data into the database.
    combined_sales = pl.concat([canada_sales_fix, usa_sales_fix], how="vertical")

    # Drop duplicates
    logger.info("Dropping duplicates...")
    combined_sales = combined_sales.unique(subset=["Order ID"])


    # Insert the combined sales data into the database.
    logger.info("Inserting data into the database...")
    insert.sales_to_database(combined_sales)

    inspector = inspect(ENGINE)
    logger.info(inspector.get_table_names())
    logger.info("Data inserted successfully.")


if __name__ == "__main__":
    main()
