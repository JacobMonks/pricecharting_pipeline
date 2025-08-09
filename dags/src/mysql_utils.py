from mysql import connector


def query_no_filter(database_name: str, table_name: str, columns):
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


if __name__ == "__main__":
    results = query_no_filter("pricecharting", "vg_price", "title_tag")
    print(results)
