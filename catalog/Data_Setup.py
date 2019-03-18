import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    picture = Column(String(300))


class RifleModelName(Base):
    __tablename__ = 'riflemodelname'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="riflemodelname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class RifleName(Base):
    __tablename__ = 'riflename'
    id = Column(Integer, primary_key=True)
    name = Column(String(350), nullable=False)
    ammo = Column(String(150))
    capacity = Column(String(150))
    power = Column(String(150))
    range = Column(String(10))
    stability = Column(String(250))
    rlink = Column(String(500))
    date = Column(DateTime, nullable=False)
    riflemodelnameid = Column(Integer, ForeignKey('riflemodelname.id'))
    riflemodelname = relationship(
        RifleModelName, backref=backref('riflename', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="riflename")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self. name,
            'ammo': self. ammo,
            'capacity': self. capacity,
            'power': self. power,
            'range': self. range,
            'stability': self. stability,
            'rlink': self.rlink,
            'date': self. date,
            'id': self. id
        }

engin = create_engine('sqlite:///rifles.db')
Base.metadata.create_all(engin)
