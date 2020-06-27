from flask import Blueprint, jsonify, request, Flask, render_template
from flask_cors import CORS
from services.vendors_services import VendorServices
from services.products_services import ProductServices
import json

app = Flask(__name__)

CORS(app, resouces={r"/*": {"origins": "*", 'Access-Control-Allow-Origin': '*'}})

vendors_app = Blueprint('vendors_app', __name__)

BASE_ROUTE = 'vendors'


@vendors_app.route(f"/{BASE_ROUTE}/listing")
def listing_vendors():
    vendors = VendorServices().listing()
    return jsonify(vendors)


@vendors_app.route(f"/{BASE_ROUTE}/register", methods=['POST'])
def register_vendor():
    if request.is_json:
        new_vendor = request.get_json()
        vendor = VendorServices().create(new_vendor)
        for product_data in new_vendor['products']:
            product = ProductServices().create(product_data)
        vendor.products.append(product)
        if vendor is None:
            return jsonify({'error': 'Vendor already exist'}), 400
        return jsonify(vendor.to__dict__()), 200
    else:
        new_vendor = {}
        new_vendor['id'] = request.form.get('id')
        new_vendor['name'] = request.form.get('name')
        new_vendor['CNPJ'] = request.form.get('cnpj')
        new_vendor['city'] = request.form.get('city')
        vendor = VendorServices().create(new_vendor)
        if vendor is None:
            return jsonify({'error': 'Vendor already exist'}), 400
        vendor = VendorServices().listing()
        return jsonify(vendor)


@vendors_app.route(f"/{BASE_ROUTE}/update/<int:id>", methods=['PUT'])
def modify_vendor(id):
    if request.is_json:
        data = request.get_json()
        if request.method == 'PUT':
            if ('name' not in data):
                return jsonify({"error": "vendor with out name"}), 400
            elif ('CNPJ' not in data):
                return jsonify({"error": "vendor with out cnpj"}), 400
            elif ('city' not in data):
                return jsonify({"error": "vendor with out city"}), 400
            updated = VendorServices().update(data)
            if updated is not None:
                return jsonify(updated.to__dict__()), 200
            return jsonify({"error": "vendor not found"}), 400
    else:
        vendor = VendorServices().locate(id)
        if vendor is not None:
            if request.method == 'PUT':
                vendor = {}
                vendor['id'] = request.form.get('id')
                vendor['name'] = request.form.get('name')
                vendor['cnpj'] = request.form.get('cnpj')
                vendor['city'] = request.form.get('city')
                if ('name' not in vendor):
                    return jsonify({"error": "vendor with out name"}), 400
                elif ('cnpj' not in vendor):
                    return jsonify({"error": "vendor with out cnpj"}), 400
                elif ('city' not in vendor):
                    return jsonify({"error": "vendor with out city"}), 400
                updated = VendorServices().update(id, vendor['name'], vendor['cnpj'], vendor['city'])
                if updated is not None:
                    vendor = VendorServices().listing()
                    return render_template('lista.html', vendors=vendors)
                return jsonify({'error': 'vendor not found'}), 400
            return render_template('atualizar.html', vendor=vendor)
        return jsonify({'error': 'vendor not found'}), 400


@vendors_app.route(f"/{BASE_ROUTE}search/<int:id>", methods=['GET'])
def locate_vendor(id):
    vendor = VendorServices().locate(id)
    if vendor is not None:
        return jsonify(vendor)
    return jsonify({'error': 'vendor not found'}), 400


@vendors_app.route(f"/{BASE_ROUTE}/delete/<int:id>", methods=['DELETE'])
def remove_vendor(id):
    removed = VendorServices().remove(id)
    if removed == 1:
        return jsonify({'success': 'vendor removed'}), 200
    return jsonify({'error': 'vendor not found'}), 400
