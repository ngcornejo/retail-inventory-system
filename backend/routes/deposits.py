from flask import Blueprint, jsonify, request
import sqlite3
from database import insert_into_table, expose_table, remove_value

from flask import Blueprint

deposits_bp = Blueprint("deposits", __name__)

def getDeposits():
    return [{
                     "id": item[0],
                     "name": item[1],
                     "location": item[2]
                    } for item in expose_table("deposits")]

@deposits_bp.route("/api/deposits", methods = ["GET", "POST"])
def get_products():
    if request.method == "POST":
        insert_into_table(request.get_json(), "deposits")
        return getDeposits(), 201
    return getDeposits(), 200


@deposits_bp.route("/api/deposits/<id>", methods = ["GET", "PUT", "DELETE"])
def id_products(id):
    match (request.method):
        case "GET":
            for i in getDeposits():
                if i["id"] == int(id):
                    return i, 200
            return {"error": "Value not found"}, 404
        case "PUT":
            db = sqlite3.connect("./data/inventory.db")
            cursor = db.cursor()
            data = request.get_json()
            set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
            values = list(data.values()) + [int(id)]
            cursor.execute(f"UPDATE deposits SET {set_clause} WHERE id = ?", values)
            db.commit()
            return getDeposits(), 200
        case "DELETE":
            remove_value(id, "deposits")
            return getDeposits(), 200
        case _:
            return {"error": "Method not allowed"}, 405