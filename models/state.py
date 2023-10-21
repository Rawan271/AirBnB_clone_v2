#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship(
                "City",
                backref="state",
                cascade="all, delete-orphan"
                )
    else:
        @property
        def cities(self):
            """Getter attribute that returns the list of City instances
            with state_id equals to the current State.id (FileStorage)
            """
            from models import storage
            result = []
            for city in storage.all("City").values():
                if city.state_id == self.id:
                    result.append(city)
            return result
