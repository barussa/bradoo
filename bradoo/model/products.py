from sqlalchemy import Column, String, Integer, Date, Numeric, ForeignKey
from base import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    code = Column('code', Integer)
    price = Column('price', Numeric)
    vendor_id = Column(Integer, ForeignKey('vendors.id'))

    def __init__(self, name, code, price,):
        self.name = name
        self.code = code
        self.price = price

    def to__dict__(self):
        d = dict()
        d['id'] = self.id
        d['name'] = self.name
        d['code'] = self.code
        d['price'] = str(self.price)
        return d
