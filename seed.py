import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "./data/inventory.db"

# ── Datos base ─────────────────────────────────────────────────────────────────

DEPOSITS = [
    ("Depósito Central",          "Buenos Aires - CABA"),
    ("Depósito Lomas de Zamora",  "Buenos Aires - Lomas de Zamora"),
    ("Depósito Tigre",            "Buenos Aires - Tigre"),
    ("Depósito La Plata",         "Buenos Aires - La Plata"),
]

PRODUCTS = [
    # (name, category, price, stock_threshold)
    ("Leche Entera 1L",         "Lácteos",    950,  50),
    ("Yogur Natural 200g",      "Lácteos",    480,  30),
    ("Queso Cremoso 400g",      "Lácteos",   1800,  20),
    ("Pechuga de Pollo 1kg",    "Carnes",    3200,  15),
    ("Carne Molida 500g",       "Carnes",    2100,  15),
    ("Milanesa de Cerdo 1kg",   "Carnes",    2800,  10),
    ("Coca-Cola 2.25L",         "Bebidas",   1500,  40),
    ("Agua Mineral 1.5L",       "Bebidas",    600,  60),
    ("Jugo Tang Naranja",       "Bebidas",    350,  35),
    ("Arroz Largo Fino 1kg",    "Almacén",    700,  40),
    ("Fideos Spaghetti 500g",   "Almacén",    450,  40),
    ("Aceite de Girasol 1.5L",  "Almacén",   1900,  25),
    ("Pan Lactal 500g",         "Panadería",  750,  30),
    ("Detergente 750ml",        "Limpieza",   950,  20),
    ("Lavandina 1L",            "Limpieza",   550,  20),
]

# Demanda base por producto (unidades/día promedio)
DEMAND = {
    "Leche Entera 1L":        12,
    "Yogur Natural 200g":      6,
    "Queso Cremoso 400g":      4,
    "Pechuga de Pollo 1kg":    5,
    "Carne Molida 500g":       4,
    "Milanesa de Cerdo 1kg":   3,
    "Coca-Cola 2.25L":         9,
    "Agua Mineral 1.5L":      14,
    "Jugo Tang Naranja":       5,
    "Arroz Largo Fino 1kg":    7,
    "Fideos Spaghetti 500g":   6,
    "Aceite de Girasol 1.5L":  3,
    "Pan Lactal 500g":         8,
    "Detergente 750ml":        3,
    "Lavandina 1L":            2,
}

# Multiplicador por día de la semana (0=lunes ... 6=domingo)
DAY_MULTIPLIER = {
    0: 1.1,   # lunes
    1: 0.9,   # martes
    2: 0.9,   # miércoles
    3: 1.2,   # jueves
    4: 1.4,   # viernes
    5: 1.5,   # sábado
    6: 0.7,   # domingo
}

# Algunos productos con stock bajo intencional para testear alertas
LOW_STOCK_PRODUCTS = {"Queso Cremoso 400g", "Milanesa de Cerdo 1kg", "Lavandina 1L"}

# ── Helpers ────────────────────────────────────────────────────────────────────

def clear_tables(cur):
    cur.execute("DELETE FROM sales")
    cur.execute("DELETE FROM stock")
    cur.execute("DELETE FROM products")
    cur.execute("DELETE FROM deposits")
    cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('sales','stock','products','deposits')")
    print("✓ Tablas limpiadas")

def seed_deposits(cur):
    cur.executemany("INSERT INTO deposits(name, location) VALUES (?, ?)", DEPOSITS)
    print(f"✓ {len(DEPOSITS)} depósitos insertados")

def seed_products(cur):
    cur.executemany(
        "INSERT INTO products(name, category, price, stock_threshold) VALUES (?, ?, ?, ?)",
        PRODUCTS
    )
    print(f"✓ {len(PRODUCTS)} productos insertados")

def seed_stock(cur, product_ids, deposit_ids):
    stock_rows = []
    for pid, (name, *_) in zip(product_ids, PRODUCTS):
        for did in deposit_ids:
            if name in LOW_STOCK_PRODUCTS:
                quantity = random.randint(2, 8)   # intencionalmente bajo
            else:
                quantity = random.randint(80, 300)
            stock_rows.append((did, pid, quantity))
    cur.executemany("INSERT INTO stock(warehouse_id, product_id, quantity) VALUES (?, ?, ?)", stock_rows)
    print(f"✓ {len(stock_rows)} registros de stock insertados")

def seed_sales(cur, product_ids, deposit_ids):
    sales_rows = []
    today = datetime.now()
    days_back = 60

    for day_offset in range(days_back, 0, -1):
        sale_date = today - timedelta(days=day_offset)
        weekday = sale_date.weekday()
        multiplier = DAY_MULTIPLIER[weekday]

        for pid, (name, *_) in zip(product_ids, PRODUCTS):
            base = DEMAND[name]
            quantity = max(1, int(base * multiplier * random.uniform(0.7, 1.3)))
            did = random.choice(deposit_ids)
            sale_date_str = sale_date.replace(
                hour=random.randint(8, 20),
                minute=random.randint(0, 59)
            ).isoformat(sep=" ")
            sales_rows.append((pid, did, quantity, sale_date_str))

    cur.executemany(
        "INSERT INTO sales(product_id, warehouse_id, quantity, date) VALUES (?, ?, ?, ?)",
        sales_rows
    )
    print(f"✓ {len(sales_rows)} ventas insertadas ({days_back} días × {len(PRODUCTS)} productos)")

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("\n── Iniciando seed ──────────────────────────────")
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("PRAGMA foreign_keys = OFF")

        clear_tables(cur)
        seed_deposits(cur)
        seed_products(cur)

        deposit_ids = [row[0] for row in cur.execute("SELECT id FROM deposits").fetchall()]
        product_ids = [row[0] for row in cur.execute("SELECT id FROM products").fetchall()]

        seed_stock(cur, product_ids, deposit_ids)
        seed_sales(cur, product_ids, deposit_ids)

        cur.execute("PRAGMA foreign_keys = ON")
        db.commit()

    print("── Seed completado ─────────────────────────────\n")

if __name__ == "__main__":
    main()