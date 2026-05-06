import sqlite3
import pandas

def get_rotation_metrics() -> dict:
    with sqlite3.connect("./data/inventory.db") as db:
        table: pandas.DataFrame = pandas.read_sql_query("SELECT * from sales", db)

        analytics = table.groupby("product_id")["quantity"].sum().reset_index()
        days = table.groupby("product_id")["date"].nunique().reset_index().rename(columns={"date": "days"})

        analytics = analytics.merge(days, on="product_id")
        analytics["average"] = round(analytics["quantity"] / analytics["days"],2)
        return analytics.to_dict(orient="records")