#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City",
                          backref="state", cascade="all, delete,delete-orphan")

    if getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            cities = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    cities.append(city)
            return cities
