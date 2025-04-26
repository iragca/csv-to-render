import polars as pl
from sqlalchemy import text


class INSERT:
    """
    Class to handle INSERT requests to the database.
    """

    def __init__(self, engine):
        self.engine = engine

    def sales_to_database(self, df: pl.DataFrame):
        """
        Create a new database with the given name.
        """
        with self.engine.connect() as conn:
            df.write_database(
                table_name="Sales", connection=conn, if_table_exists="replace"
            )
