from src.dml import INSERT, SELECT
from src.db import initdb

def main():
    # Initialize the database engine with the corresponding configuration and
    # create the necessary tables.
    ENGINE = initdb()

    # Instantiate the necessary Data Manipulation Language (DML) classes for
    # database operations, both classes take the configured engine as an argument.
    #
    # Example of inserting a user:
    #   insert = INSERT(ENGINE)
    #   insert.user("username", "password")
    # insert = INSERT(ENGINE)
    # select = SELECT(ENGINE)

if __name__ == "__main__":
    main()
