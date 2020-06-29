from flask import Blueprint, jsonify, request, Flask, render_template
from flask_cors import CORS
from services.products_services import ProductServices
import json

app = Flask(__name__)

CORS(app, resouces={
    r"/*": {"origins": "*", 'Access-Control-Allow-Origin': '*'}
})

products_app = Blueprint('products_app', __name__)

BASE_ROUTE = 'products'


@products_app.route(f"/{BASE_ROUTE}/listing")
def listing_products():
    products = ProductServices().listing()
    return jsonify(products)


@products_app.route(f"/{BASE_ROUTE}/register", methods=['POST'])
def register_product():
    if request.is_json:
        new_product = request.get_json()
        if new_product is None:
            return jsonify({'error': 'Fill the requests'}), 400
        if 'name' not in new_product:
            return jsonify({'error': 'Fill name'})
        if 'code' not in new_product:
            return jsonify({'error': 'Fill code'})
        product = ProductServices().create(new_product)
        return jsonify(product.to__dict__()), 200
    else:
        return jsonify({'error': 'Invalid Json format'}), 400


@products_app.route(f"/{BASE_ROUTE}/update/<int:id>", methods=['PUT'])
def modify_product(id):
    if request.is_json:
        data = request.get_json()
        if request.method == 'PUT':
            if ('name' not in data):
                return jsonify({"error": "product with out name"}), 400
            elif ('code' not in data):
                return jsonify({"error": "product with out code"}), 400
            elif ('price' not in data):
                return jsonify({"error": "product with out price"}), 400
            updated = ProductServices().update(data)
            if updated is not None:
                return jsonify(updated.to__dict__()), 200
            return jsonify({"error": "product not found"}), 400
    else:
        product = ProductServices().locate(id)
        if product is not None:
            if request.method == 'PUT':
                product = {}
                product['id'] = request.form.get('id')
                product['name'] = request.form.get('name')
                product['code'] = request.form.get('code')
                product['price'] = request.form.get('price')
                if ('name' not in product):
                    return jsonify({"error": "product with out name"}), 400
                elif ('code' not in product):
                    return jsonify({"error": "product with out code"}), 400
                elif ('price' not in product):
                    return jsonify({"error": "product with out price"}), 400
                updated = service_update(
                    id, product['name'], product['code'], product['price']
                )
                if updated is not None:
                    product = ProductServices().listing()
                    return render_template('lista.html', products=products)
                return jsonify({'error': 'product not found'}), 400
            return render_template('atualizar.html', product=product)
        return jsonify({'error': 'product not found'}), 400


@products_app.route(f"/{BASE_ROUTE}search/<int:id>", methods=['GET'])
def locate_product(id):
    product = ProductServices().locate(id)
    if product is not None:
        return jsonify(product)
    return jsonify({'error': 'product not found'}), 400


@products_app.route(f"/{BASE_ROUTE}/delete/<int:id>", methods=['DELETE'])
def remove_product(id):
    removed = ProductServices().remove(id)
    if removed == 1:
        return jsonify({'success': 'product removed'}), 200
    return jsonify({'error': 'product not found'}), 400
