import logging

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import graphlite

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    phone = Column(String(10), nullable=False)
    email = Column(String(30), nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship('Address', back_populates='residents')
    birth_date = Column(String(10), nullable=False)

    @property
    def json(self):
        return dict(first_name=self.first_name, last_name=self.last_name, birth_date=self.birth_date,
                    phone=self.phone, email=self.email, address_id=self.address_id)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    number = Column(String(10), nullable=False)
    street = Column(String(20), nullable=False)
    city = Column(String(20), nullable=False)
    zipcode = Column(String(5), nullable=False)
    country = Column(String(10), nullable=False)
    residents = relationship('Person', back_populates='address')

    @property
    def json(self):
        return dict(number=self.number, street=self.street, city=self.city,
                    zipcode=self.zipcode, country=self.country)

class Database():
    session_singleton = None

    def __init__(self, path=None):
        self.path = path
        if not self.path:
            self.path = 'people.db'
        self._engine = create_engine('sqlite:///{}'.format(self.path))
        self._session = None
        self._graph = graphlite.connect(self.path, graphs=['begat'])

    def create(self):
        Base.metadata.create_all(self._engine)
    
    def close(self):
        if self._session:
            self._session.close()
        self._engine.dispose()
        self._graph.close()

    @property
    def session(self):
        if not self._session:
            DBSession = sessionmaker(bind = self._engine)
            self._session = DBSession()
        return self._session
    
    @property
    def graph(self):
        return self._graph