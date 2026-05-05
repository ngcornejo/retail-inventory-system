from flask import Blueprint, jsonify, request
import sqlite3
from database import insert_into_table, expose_table, remove_value

from flask import Blueprint

products_bp = Blueprint("products", __name__)

def getProducts():
    return [{
                     "id": item[0],
                     "name": item[1],
                     "category": item[2],
                     "price": item[3],
                     "stock_threshold": item[4]
                    } for item in expose_table("products")]

@products_bp.route("/api/products", methods = ["GET", "POST"])
def get_products():
    if request.method == "POST":
        db = sqlite3.connect("./data/inventory.db")
        cursor = db.cursor()
        cursor.execute("""
                       INSERT INTO products(name, category, price, stock_threshold)
                       VALUES (?, ?, ?, ?)
                       """, (
                             request.get_json()["name"],
                             request.get_json()["category"],
                             request.get_json()["price"],
                             request.get_json()["threshold"],
                            ))
        db.commit()
    return getProducts(), 201


@products_bp.route("/api/products/<id>")
def get_product(id):
    for i in getProducts():
        if i["id"] == int(id):
            return i, 201
    return {"error": "Value not found"}, 401

@products_bp.route("/api/products/<id>", methods = ["DELETE"])
def remove_product(id):
    remove_value(id, "products")
    return getProducts(), 200

@products_bp.route("/api/products/<id>", methods = ["PUT"])
def update_product(id):
    db = sqlite3.connect("./data/inventory.db")
    cursor = db.cursor()
    data = request.get_json()
    cursor.execute(f"""
                   UPDATE products
                   SET {data["column"]} = ?
                   WHERE id = ?
                   """,
                   (data["value"],
                   int(id))
                   )
    db.commit()
    return getProducts(), 201