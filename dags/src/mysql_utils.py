from mysql import connector


def query_no_filter(database_name: str, table_name: str, columns):
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
        num_cols = 0
        if isinstance(columns, list):
            cols = ", ".join(columns)
            num_cols = len(columns)

        elif isinstance(columns, str):
            cols = columns
            num_cols = len(cols.split(','))

        query_row_sql = f"SELECT {cols} FROM {table_name} limit 10;"
        cursor.execute(query_row_sql)

        print(cols, num_cols)
        for row in cursor:
            print(row[0])

        cursor.close()
        conn.close()

    except connector.Error as e:
        print("ERROR - ", e)


if __name__ == "__main__":
    query_no_filter("pricecharting", "vg_price", "title_tag")
