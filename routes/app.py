from flask import Blueprint, jsonify, request, Flask, render_template
from flask_cors import CORS
import json

app = Flask(__name__)

CORS(app, resouces={
    r"/*": {"origins": "*", 'Access-Control-Allow-Origin': '*'}
})

home_app = Blueprint('home_app', __name__)

BASE_ROUTE = 'home'


@home_app.route('/')
def root():
    return render_template('index.html')
