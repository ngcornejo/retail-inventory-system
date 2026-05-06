import sqlite3, pandas

def insert_into_table(contents: list | dict, table_name: str) -> None:
    with sqlite3.connect("./data/inventory.db") as connection:
        cur = connection.cursor()
        if len(contents) == 0: return
        parsed_columns = parse_columns(table_name)
        columns_list = [f":{col}" for col in read_columns(table_name)]
        inserted_columns = ""
        for col in columns_list:
            inserted_columns += f"{col}, "
        inserted_columns = f"{inserted_columns[:-2]}"
        query = f"INSERT INTO {table_name}{parsed_columns} VALUES ({inserted_columns})"
        print(contents)
        if isinstance(contents, dict):
            contents = [contents]
        cur.executemany(query, contents)
        connection.commit()

def expose_table(table_name: str):
    with sqlite3.connect("./data/inventory.db") as connection:
        cur = connection.cursor()
        return cur.execute(f"SELECT * from {table_name}").fetchall()

def remove_value(value, table_name) -> None:
    with sqlite3.connect("./data/inventory.db") as connection:
        cur = connection.cursor()
        cur.execute(f"DELETE from {table_name} WHERE id = ?",value)
        connection.commit()

def read_columns(table_name: str) -> list:
    with sqlite3.connect("./data/inventory.db") as db:
        query = pandas.read_sql_query(f"SELECT * from {table_name}",db)
        protected_list = [col for col in query if col != "id"]
        return list(protected_list)
    
def parse_columns(table_name: str) -> str:
    with sqlite3.connect("./data/inventory.db") as db:
        parsed_output = "("
        for col in read_columns(table_name):
            parsed_output += f"{col}, "
        parsed_output = parsed_output[:-2] + ")"
        return parsed_output

if __name__ == '__main__':
    with sqlite3.connect("./data/inventory.db") as db:
        cur = db.cursor()

        cur.execute("""
                    CREATE TABLE products(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name varchar(255),
                        category varchar(255),
                        price decimal(6,2),
                    stock_threshold INTEGER
                    )
                    """)
        db.commit()

        cur.execute("""
                    CREATE TABLE deposits(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name varchar(255),
                        location varchar(255)
                    )
                    """)
        db.commit()

        cur.execute("""
                    CREATE TABLE stock(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        warehouse_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                            FOREIGN KEY (warehouse_id) REFERENCES deposits(id)
                            FOREIGN KEY (product_id) REFERENCES products(id)
                            UNIQUE(warehouse_id, product_id)
                    )
                    """)
        db.commit()

        cur.execute("""
                    CREATE TABLE sales(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        warehouse_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        date DATETIME,
                            FOREIGN KEY (warehouse_id) REFERENCES deposits(id)
                            FOREIGN KEY (product_id) REFERENCES products(id)
                    )
                    """)
        db.commit()