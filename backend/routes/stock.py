from flask import Blueprint, jsonify, request
import sqlite3
from database import insert_into_table, expose_table, remove_value

from flask import Blueprint

stock_bp = Blueprint("stock", __name__)

def getStock():
    return [{
        "id": item[0],
        "warehouse_id": item[1],
        "product_id": item[2],
        "quantity": item[3]
    } for item in expose_table("stock")]

@stock_bp.route("/api/stock", methods = ["GET", "POST"])
def get_products():
    if request.method == "POST":
        data = request.get_json()
        if isinstance(data, dict):
            data = [data]
        try:
            insert_into_table(data, "stock")
        except sqlite3.IntegrityError:
            return {"error": "El producto ya existe en ese depósito."}, 409
        return getStock(), 201
    return getStock(), 200


@stock_bp.route("/api/stock/<id>", methods = ["GET", "PUT", "DELETE"])
def id_products(id):
    match (request.method):
        case "GET":
            for i in getStock():
                if i["id"] == int(id):
                    return i, 200
            return {"error": "Value not found"}, 404
        case "PUT":
            db = sqlite3.connect("./data/inventory.db")
            cursor = db.cursor()
            data = request.get_json()
            data.pop("warehouse_id", None)
            data.pop("product_id", None)
            set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
            values = list(data.values()) + [int(id)]
            cursor.execute(f"UPDATE stock SET {set_clause} WHERE id = ?", values)
            db.commit()
            return getStock(), 200
        case "DELETE":
            remove_value(id, "stock")
            return getStock(), 200
        case _:
            return {"error": "Method not allowed"}, 405