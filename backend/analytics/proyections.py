import sqlite3, pandas

def get_proyections() -> dict:
    with sqlite3.connect("./data/inventory.db") as db:
        table = pandas.read_sql_query("SELECT * from sales",db)
        table["date"] = pandas.to_datetime(table["date"]).dt.day_of_week
        table = table.rename(columns={"date": "weekday"})
        proyections = table.groupby(["product_id", "weekday"])["quantity"].mean().reset_index().rename(columns={"quantity": "average"})
        proyections["average"] = round(proyections["average"],2)
        DAYS = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
        proyections["weekday"] = proyections["weekday"].map(DAYS)
        return proyections.to_dict(orient="records")