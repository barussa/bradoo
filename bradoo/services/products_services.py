import sqlalchemy
from base import session
from model.products import Product


class ProductServices():

    def __init__(self):
        self.session = session

    def listing(self):
        return [product.to__dict__() for product in self.session.query(Product).all()]

    def locate(self, id):
        product = self.session.query(Product).get(id)
        if product is None:
            return None
        return product

    def create(self, data):
        product = Product(data['name'], data['code'], data['price'])
        self.session.add(product)
        self.session.commit()
        #session.close()
        return product

    def remove(self, id):
        info = self.locate(id)
        if info is None:
            return 0
        self.session.query(Product).filter(Product.id == id).delete()
        self.session.commit()
        return 1

    def update(self, modify):
        product = self.locate(modify['id'])
        product.name = modify['name']
        product.code = modify['code']
        product.price = modify['price']
        self.session.commit()
        return self.locate(product.id)
