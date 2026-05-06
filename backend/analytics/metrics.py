import sqlite3
import pandas

db = sqlite3.connect("./data/inventory.db")
table : pandas.DataFrame = pandas.read_sql_query("SELECT * from sales", db)
table["date"] = pandas.to_datetime(table["date"]).dt.date

analytics = pandas.DataFrame(columns=["product_id", "quantity"])
analytics["product_id"] = table["product_id"].unique()
analytics["quantity"] = 0

for i in table.index:
    for j in analytics["product_id"].index:
        if table["product_id"][i] == analytics["product_id"][j]:
            analytics.loc[j, "quantity"] += table["quantity"][i]
            break

print(analytics)