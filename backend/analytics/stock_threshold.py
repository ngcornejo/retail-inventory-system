import sqlite3, pandas

def get_understocks() -> dict:
    with sqlite3.connect("./data/inventory.db") as db:
        table = pandas.read_sql_query("""
                                      SELECT product_id, stock.warehouse_id, stock.quantity, products.stock_threshold
                                      from stock
                                      INNER JOIN products
                                      ON stock.product_id = products.id
                                      """, db)
        table = table[table["quantity"] <= table["stock_threshold"]].sort_values("quantity")
        return table.to_dict(orient="records")
