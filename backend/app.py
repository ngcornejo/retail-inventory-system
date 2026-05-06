from flask import Flask
from flask_cors import CORS
import database
import analytics.metrics, analytics.stock_threshold, analytics.proyections

from routes.products import products_bp
from routes.deposits import deposits_bp
from routes.stock import stock_bp
from routes.sales import sales_bp

app = Flask(__name__)
app.register_blueprint(products_bp)
app.register_blueprint(deposits_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(sales_bp)

CORS(app)

@app.route("/")
def hello_world():
    return f"""<meta charset=\"UTF-8\"> {database.expose_table('products')}"""

@app.route("/api/analytics/metrics")
def get_metrics():
    return analytics.metrics.get_rotation_metrics(), 200

@app.route("/api/analytics/stock")
def get_stock():
    return analytics.stock_threshold.get_understocks(), 200

@app.route("/api/analytics/forecast")
def get_proyections():
    return analytics.proyections.get_proyections(), 200