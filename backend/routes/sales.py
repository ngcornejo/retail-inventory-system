from flask import Blueprint, jsonify, request
import sqlite3
from datetime import datetime
from database import insert_into_table, expose_table, remove_value

from flask import Blueprint

sales_bp = Blueprint("sales", __name__)

def getSales():
    return [{
        "id": item[0],
        "warehouse_id": item[1],
        "product_id": item[2],
        "quantity": item[3],
        "date": item[4],
    } for item in expose_table("sales")]

@sales_bp.route("/api/sales", methods = ["GET", "POST"])
def get_products():
    if request.method == "POST":
        data = request.get_json()
        if isinstance(data, dict):
            data = [data]
        for args in data:
            args["date"] = datetime.now().isoformat(" ")
            with sqlite3.connect("./data/inventory.db") as db:
                cursor = db.cursor()
                cursor.execute(f"UPDATE stock SET quantity = quantity - ? WHERE quantity >= ? AND product_id = ? AND warehouse_id = ?", (args["quantity"], args["quantity"], args["product_id"], args["warehouse_id"]))
                db.commit()
        insert_into_table(data, "sales")
        return getSales(), 201
    return getSales(), 200


@sales_bp.route("/api/sales/<id>", methods = ["GET", "DELETE"])
def id_products(id):
    match (request.method):
        case "GET":
            for i in getSales():
                if i["id"] == int(id):
                    return i, 200
            return {"error": "Value not found"}, 404
        case "DELETE":
            remove_value(id, "sales")
            return getSales(), 200
        case _:
            return {"error": "Method not allowed"}, 405