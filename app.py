from flask import Flask, jsonify, request, render_template, Blueprint
from routes.vendors_api import vendors_app
from routes.products_api import products_app
from flask_cors import CORS
import request as Req
from base import engine, Base

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'


CORS(app)

app.register_blueprint(vendors_app)
app.register_blueprint(products_app)

Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(port=5004, debug=True)
