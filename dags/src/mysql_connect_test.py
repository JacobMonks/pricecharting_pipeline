from mysql import connector


def mysql_test_connect(table_name: str, test_input: str):
    try:
        conn = connector.connect(
            host="127.0.0.1",
            port=3306,
            database="sys",
            user="root",
            password=""
        )
        cursor = conn.cursor()

        new_table_sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                                id int(11) NOT NULL AUTO_INCREMENT,
                                name VARCHAR(255) NOT NULL,
                                PRIMARY KEY (id)
                            );"""
        cursor.execute(new_table_sql)

        new_row_sql = f"INSERT INTO test_table (name) VALUES ('{test_input}');"
        cursor.execute(new_row_sql)

        query_row_sql = "SELECT * FROM test_table;"
        cursor.execute(query_row_sql)

        for (id, name) in cursor:
            print(f"""
                ID: {id}
                Name: {name}
            """)

        delete_query = f"DROP TABLE IF EXISTS {table_name};"
        cursor.execute(delete_query)

        cursor.close()
        conn.close()

    except connector.Error as e:
        print("ERROR - ", e)


if __name__ == "__main__":
    mysql_test_connect("test_table", "test")
