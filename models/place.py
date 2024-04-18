#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

if getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'), nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'), nullable=False)
                          )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"),  nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review",
            cascade="all, delete-orphan",
            backref="place"
        )

        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False,
            back_populates="place_amenities"
        )

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            from models import storage
            from models.review import Review
            review_list = []
            for val in storage.all(Review).values():
                if val.place_id == self.id:
                    review_list.append(val)
            return review_list

        @property
        def amenities(self):
            """returns list of Amenity instances based on
            the attribute amenity_ids"""
            from models import storage
            from models.amenity import Amenity
            amenities_list = []
            for val in storage.all(Amenity).values():
                if val.id in self.amenity_ids:
                    amenities_list.append(val)
            return amenities_list

        @amenities.setter
        def amenities(self, obj):
            """appends an Amenity.id to the attribute amenity_ids"""
            if (obj.__class__.__name__ == "Amenity" and
                    obj.id not in self.amenity_ids):
                self.amenity_ids.append(obj.id)
