from flask import Flask
import database

from routes.products import products_bp

app = Flask(__name__)
app.register_blueprint(products_bp)

@app.route("/")
def hello_world():
    return f"""<meta charset=\"UTF-8\"> {database.expose_table('products')}"""