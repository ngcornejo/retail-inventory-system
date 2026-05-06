from flask import Flask
import database, analytics.metrics

from routes.products import products_bp
from routes.deposits import deposits_bp
from routes.stock import stock_bp
from routes.sales import sales_bp

app = Flask(__name__)
app.register_blueprint(products_bp)
app.register_blueprint(deposits_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(sales_bp)



@app.route("/")
def hello_world():
    return f"""<meta charset=\"UTF-8\"> {database.expose_table('products')}"""