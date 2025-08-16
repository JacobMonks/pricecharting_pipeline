from mysql import connector
from sqlalchemy import create_engine
import pandas as pd


def query_no_filter(database_name: str, table_name: str, columns):
    """
    Queries all rows from a local database table.

    Args
    - database_name: The name of the database.
    - table_name: The name of the table (single or joined with condition).
    - columns: The columns to query (a list of strings or a single string with comma-separated names).

    Returns
    A list of dictionaries containing the row data.
    """
    results = []
    try:
        conn = connector.connect(
            host="127.0.0.1",
            port=3306,
            database=database_name,
            user="root",
            password=""
        )
        cursor = conn.cursor()

        cols = None
        cols_list = None
        if isinstance(columns, list):
            cols_list = columns
            cols = ", ".join(columns)

        elif isinstance(columns, str):
            cols_list = columns.split(',')
            cols = columns

        query_row_sql = f"SELECT {cols} FROM {table_name};"
        cursor.execute(query_row_sql)

        num_cols = len(cols_list)
        for row in cursor:
            results.append({cols_list[num]: row[num] for num in range(num_cols)})

        cursor.close()
        conn.close()

    except connector.Error as e:
        print("ERROR - ", e)

    return results


def report_failures(input_data: list):
    """
    Overwrites invalid_url MySQL table with currently failing URLs.

    Args:
    - input_data: a list of dictionaries.
    """
    report_df = pd.DataFrame(input_data)

    db_url = "mysql+pymysql://{user}:{password}@{host}/{database}"

    db_url = db_url.format(
        user="root",
        password="",
        host="127.0.0.1:3306",
        database="pricecharting"
    )

    sql_engine = create_engine(db_url, pool_recycle=3600)
    conn = sql_engine.connect()

    try:
        report_df.to_sql(name="invalid_url", con=conn, if_exists="replace")

    except ValueError as e:
        print(e)

    except Exception as e:
        print(f"Ran into a problem - {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    results = query_no_filter("pricecharting", "vg_price", "title_tag")
    print(results)
