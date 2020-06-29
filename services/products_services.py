import sqlalchemy
from base import session
from model.products import Product


class ProductServices():

    def __init__(self):
        self.session = session

    def listing(self):
        return [
            product.to__dict__() for product in self
            .session
            .query(Product)
            .all()
        ]

    def locate(self, id):
        product = self.session.query(Product).get(id)
        if product is None:
            return None
        return product

    def create(self, data):
        price = None
        if 'price' in data:
            price = data['price']
        product = Product(data['name'], data['code'], data['vendor_id'], price)
        self.session.add(product)
        self.session.commit()
        return product

    def remove(self, id):
        info = self.locate(id)
        if info is None:
            return 0
        self.session.query(Product).filter(Product.id == id).delete()
        self.session.commit()
        return 1

    def update(self, modify):
        product = None
        if modify['id'] is not None:
            product = self.locate(modify['id'])
            product.name = modify['name']
            product.code = modify['code']
            product.price = modify['price']
            self.session.commit()
            return self.locate(product.id)
        else:
            self.create(modify)

    def remove_by_vendor_id(self, id):
        self.list_by_vendor_id(id).delete()
        self.session.commit()
        return 1

    def list_by_vendor_id(self, vendor_id):
        listing = self.session.query(Product).filter(
            Product.vendor_id == vendor_id
        ).all()
        return listing

    def list_by_multiple_names(self, names):
        listing = self.session.query(Product).filter(
            Product.name.in_(names)
        ).all()
        print(listing)
        return listing
