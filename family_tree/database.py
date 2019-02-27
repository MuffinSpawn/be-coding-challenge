import os

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from graphlite import V, connect

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    middle_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    phone_number = Column(String(10), nullable=False)
    email = Column(String(30), nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship('Child', back_populates='residents')
    birth_date = Column(String(10), nullable=False)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    number = Column(String(10), nullable=False)
    street = Column(String(20), nullable=False)
    city = Column(String(20), nullable=False)
    zipcode = Column(Integer, nullable=False)
    country = Column(String(10), nullable=False)
    residents = relationship('Person', back_populates='address')

class Database():
    def __init__(self, path=None):
        self.path = path
        if not self.path:
            self.path = 'people.db'

    def create(self):
        engine = create_engine('sqlite:///{}'.format(self.path))
        Base.metadata.create_all(engine)

        connect(self.path, graphs=['begat'])

    def delete(self):
        os.remove(self.path)
