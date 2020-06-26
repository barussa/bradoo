import sqlalchemy
from base import session

from model.vendors import Vendor


class VendorServices():

    def __init__(self):
        self.session = session

    def listing(self):
        return [vendor.to__dict__() for vendor in self.session.query(Vendor).all()]

    def locate(self, id):
        vendor = self.session.query(Vendor).get(id)
        if vendor is None:
            return None
        return vendor

    def create(self, data):
        vendor = Vendor(data['name'], data['CNPJ'], data['city'])
        self.session.add(vendor)
        self.session.commit()
        return vendor

    def remove(self, id):
        info = self.locate(id)
        if info is None:
            return 0
        self.session.query(Vendor).filter(Vendor.id == id).delete()
        self.session.commit()
        return 1

    def update(self, modify):
        vendor = self.locate(modify['id'])
        vendor.name = modify['name']
        vendor.cnpj = modify['CNPJ']
        vendor.city = modify['city']
        self.session.commit()
        return self.locate(vendor.id)
