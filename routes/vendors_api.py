from flask import Blueprint, jsonify, request, Flask, render_template
from flask_cors import CORS
from services.vendors_services import VendorServices
from services.products_services import ProductServices
import json
import math

app = Flask(__name__)

CORS(app, resouces={
    r"/*": {"origins": "*", 'Access-Control-Allow-Origin': '*'}
})

vendors_app = Blueprint('vendors_app', __name__)

BASE_ROUTE = 'vendors'


@vendors_app.route(f"/{BASE_ROUTE}/listing")
def listing_vendors():
    vendors = VendorServices().listing()
    if not vendors:
        return jsonify({'error': 'No vendors found'}), 204
    return jsonify(vendors)


@vendors_app.route(f"/{BASE_ROUTE}/register", methods=['POST'])
def register_vendor():
    if request.is_json:
        new_vendor = request.get_json()
        if new_vendor is None:
            return jsonify({'error': 'Invalid vendor'})
        if 'name' not in new_vendor:
            return jsonify({'error': 'Vendor without name'})
        if 'CNPJ' not in new_vendor:
            return jsonify({'error': 'Vendor without CNPJ'})
        if 'city' not in new_vendor:
            return jsonify({'error': 'Vendo without city'})
        if not new_vendor['name']:
            return jsonify({'error': 'Fill name'})
        if not new_vendor['CNPJ']:
            return jsonify({'error': 'Fillt CNPJ'})
        if not new_vendor['city']:
            return jsonify({'error': 'Fill city'})
        if VendorServices().search(new_vendor['CNPJ']):
            return jsonify({'error': 'Vendor already exists'})
        names = map(lambda x: x['name'].strip().upper(), new_vendor['products'])
        print(type(names))
        if ProductServices().list_by_multiple_names(names):
            return jsonify({'error': 'Product already exist'})
        vendor = VendorServices().create(new_vendor)
        for product_data in new_vendor['products']:
            product_data['vendor_id'] = vendor.id
            product = ProductServices().create(product_data)
        return jsonify(vendor.to__dict__()), 200
    else:
        return jsonify({'error': 'Invalid Json format'})


@vendors_app.route(f"/{BASE_ROUTE}/update/<int:id>", methods=['PUT'])
def modify_vendor(id):
    if request.is_json:
        data = request.get_json()
        if request.method == 'PUT':
            if ('name' not in data):
                return jsonify({"error": "vendor with out name"})
            elif ('CNPJ' not in data):
                return jsonify({"error": "vendor with out cnpj"})
            elif ('city' not in data):
                return jsonify({"error": "vendor with out city"})
            updated = VendorServices().update(data)
            if updated is not None:
                return jsonify(updated.to__dict__()), 200
            return jsonify({"error": "vendor not found"})
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
                    return jsonify({"error": "vendor with out name"})
                elif ('cnpj' not in vendor):
                    return jsonify({"error": "vendor with out cnpj"})
                elif ('city' not in vendor):
                    return jsonify({"error": "vendor with out city"})
                updated = VendorServices().update(
                    id, vendor['name'], vendor['cnpj'], vendor['city']
                )
                if updated is not None:
                    vendor = VendorServices().listing()
                    return render_template('lista.html', vendors=vendors)
                return jsonify({'error': 'vendor not found'})
            return render_template('atualizar.html', vendor=vendor)
        return jsonify({'error': 'vendor not found'})


@vendors_app.route(f"/{BASE_ROUTE}search/<int:id>", methods=['GET'])
def locate_vendor(id):
    vendor = VendorServices().locate(id)
    if vendor is not None:
        return jsonify(vendor)
    return jsonify({'error': 'vendor not found'})


@vendors_app.route(f"/{BASE_ROUTE}/delete/<int:id>", methods=['DELETE'])
def remove_vendor(id):
    removed_products = ProductServices().remove_by_vendor_id(id)
    removed = VendorServices().remove(id)
    if removed == 1:
        return jsonify({'success': 'vendor removed'}), 200
    return jsonify({'error': 'vendor not found'})
