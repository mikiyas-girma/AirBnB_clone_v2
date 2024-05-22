#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import Relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    cities = Relationship(
        "City",
        cascade="all,delete,delete-orphan",
        backref="state",
        single_parent=True
    )

    if getenv("HBNB_TYPE_STORAGE") != "db":

        @property
        def cities(self):
            """returns list of city instances with state_id"""
            from models import storage
            from models.city import City
            state_cities = []
            for val in storage.all(City).values():
                if val.state_id == self.id:
                    state_cities.append(val)
            return state_cities
