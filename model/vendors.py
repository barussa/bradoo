
from sqlalchemy import Column, String, Integer, Date, Numeric
from sqlalchemy.orm import relationship

from base import Base


class Vendor(Base):
    __tablename__ = 'vendors'

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    cnpj = Column('cnpj', Numeric)
    city = Column('city', String)
    products = relationship('Product')

    def __init__(self, name, cnpj, city):
        self.name = name
        self.cnpj = cnpj
        self.city = city

    def to__dict__(self):
        d = dict()
        d['id'] = self.id
        d['name'] = self.name
        d['cnpj'] = str(self.cnpj)
        d['city'] = self.city
        d['products'] = [product.to__dict__() for product in self.products]
        return d
