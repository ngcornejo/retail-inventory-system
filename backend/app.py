from flask import Flask
from flask_cors import CORS
import analytics.metrics, analytics.stock_threshold, analytics.proyections
import database

from routes.products import products_bp
from routes.deposits import deposits_bp
from routes.stock import stock_bp
from routes.sales import sales_bp

app = Flask(__name__)
app.register_blueprint(products_bp)
app.register_blueprint(deposits_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(sales_bp)
database.init_db()
CORS(app)

@app.route("/")
def hello_world():
    return {"status": "OK"}, 200

@app.route("/api/analytics/metrics")
def get_metrics():
    return analytics.metrics.get_rotation_metrics(), 200

@app.route("/api/analytics/stock")
def get_stock():
    return analytics.stock_threshold.get_understocks(), 200

@app.route("/api/analytics/forecast")
def get_proyections():
    return analytics.proyections.get_proyections(), 200