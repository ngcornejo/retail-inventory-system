import sqlite3

def insert_into_table(contents: list, table_name: str):
    with sqlite3.connect("./data/inventory.db") as connection:
        cur = connection.cursor()
        if len(contents) == 0: return
        
        value_amount: int = len(contents[0]) - 1
        
        if len(contents) == 1:
            cur.execute(f"INSERT INTO {table_name} VALUES (?{', ?' * value_amount})",contents[0])
            connection.commit
            return
        
        cur.executemany(f"INSERT INTO {table_name} VALUES (?{', ?' * value_amount})",contents)
        connection.commit

def expose_table(table_name: str):
    with sqlite3.connect("./data/inventory.db") as connection:
        cur = connection.cursor()
        return cur.execute(f"SELECT * from {table_name}").fetchall()

def remove_value(value, table_name):
    with sqlite3.connect("./data/inventory.db") as connection:
        cur = connection.cursor()
        cur.execute(f"DELETE from {table_name} WHERE id = ?",value)
        connection.commit()

if __name__ == '__main__':
    db = sqlite3.connect("./data/inventory.db")
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
                        FOREIGN KEY (warehouse_id) REFERENCES deposits(id)
                        FOREIGN KEY (product_id) REFERENCES products(id)
                )
                """)
    db.commit()