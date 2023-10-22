#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage_type


class State(BaseModel, Base):
    """Represents the State class
    Class Attributes:
        name: sqlalchemy String Column: the state name
        cities: represent a relationship with the class City
    """
    __tablename__ = 'states'

    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete")
    else:
        name = ""

        @property
        def cities(self):
            """getter for the cities attribute
            * returns the list of City instances with state_id equals
            to the current State.id
            * It will be the FileStorage relationship between State and
            City
            """
            from models import storage

            all_cities = storage.all(City)
            return [city for city in all_cities.values()
                    if city.state_id == self.id]
