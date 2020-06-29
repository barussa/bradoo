from sqlalchemy import Column, String, Integer, Date, Numeric, ForeignKey
from base import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    code = Column('code', Integer)
    price = Column('price', Numeric)
    vendor_id = Column(Integer, ForeignKey('vendors.id'))

    def __init__(self, name, code, vendor_id, price=None):
        self.name = name
        self.code = code
        self.vendor_id = vendor_id
        if not price:
            self.price = None
        else:
            self.price = price

    def to__dict__(self):
        d = dict()
        d['id'] = self.id
        d['name'] = self.name
        d['code'] = self.code
        d['vendor_id'] = self.vendor_id
        if self.price:
            d['price'] = str(self.price)
        else:
            d['price'] = None
        return d
