#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    api/xr.py
    ~~~~~~~~~

    XR API

    :copyright: (c) 2015 by mek.
    :license: see LICENSE for more details.
"""

from random import randint
from datetime import datetime
from sqlalchemy import Column, Unicode, BigInteger, Integer, \
    DateTime, ForeignKey, Table, exists, func
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import relationship
from api import db, engine, core, auth



BETA_USERS = ["Max", "Kim", "Mek", "Austin", "Missie", "Sam"]

EXERCISES = [
    "Pinch Blocks", "Handstands", "Hangboards", "Rock Climbing",
    "Pullups", "Pushup", "Running", "Cycling", "Hiking", "Angels",
    "Ab Roller", "Planks", "Deadlifts", "Curls", "Legups",
    "Brushoffs", "Yoga", "Tennis", "Swimming"
]


checkin_to_exercise = \
    Table('checkin_exercises', core.Base.metadata,
          Column('id', BigInteger, primary_key=True),
          Column('exercise_id', BigInteger,
                 ForeignKey('exercises.id', use_alter=True),
                 nullable=False),
          Column('checkin_id', BigInteger,
                 ForeignKey('checkins.id', use_alter=True),
                 nullable=False)
          )


class User(core.Base):

    __tablename__ = "users"
    TBL = __tablename__

    id = Column(BigInteger, primary_key=True)
    email = Column(Unicode, unique=True, nullable=False)
    username = Column(Unicode, unique=True, nullable=False)
    salt = Column(Unicode, nullable=False)
    phash = Column(Unicode, nullable=False)
    created = Column(DateTime(timezone=False), default=datetime.utcnow,
                     nullable=False)

    @classmethod
    def authenticate(cls, email, password):
        u = cls.get(email=email)
        return auth.Account._roast(password, u.salt, u.phash)

    @classmethod
    def register(cls, email, username, password):
        kwargs = auth.Account.register(email, username, password)
        u = cls(**kwargs)
        u.create()

    def dict(self, artists=False):
        user = super(User, self).dict()
        user.pop('salt')
        user.pop('phash')
        return user

class Checkin(core.Base):

    __tablename__ = "checkins"
    TBL = __tablename__

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    exercise_id = Column(BigInteger, ForeignKey('exercises.id'))
    duration = Column(Integer, nullable=False)  # seconds
    weight = Column(Integer, default=0)  # lbs
    distance = Column(Integer, default=0)  # miles
    reps = Column(Integer, default=1)
    sets = Column(Integer, default=1)
    cycles = Column(Integer, default=1)
    notes = Column(Unicode, nullable=True)
    date = Column(DateTime(timezone=False), default=datetime.utcnow,
                     nullable=False)

    exercise = relationship('Exercise', backref='checkins')


class Exercise(core.Base):

    __tablename__ = "exercises"
    TBL = __tablename__

    id = Column(BigInteger, primary_key=True)
    name = Column(Unicode, unique=True, nullable=False)
    created = Column(DateTime(timezone=False), default=datetime.utcnow,
                     nullable=False)

# class ExerciseVariation(core.Base):

#     __tablename__ = "exercise_variations"
#     TBL = __tablename__

#     id = Column(BigInteger, primary_key=True)
#     exercise_id = Column(BigInteger, ForeignKey('exercises.id'))
#     name = Column(Unicode, unique=True, nullable=False)
#     created = Column(DateTime(timezone=False), default=datetime.utcnow,
#                      nullable=False)

#     exercise = relationship('Exercise', backref='checkins')


def build_tables():
    """Builds database postgres schema"""
    from sqlalchemy import MetaData
    MetaData().create_all(engine)


def report():
    """Generates a statistical report of database coverage compared to
    available data
    """
    return {
        #"artists": Artist.query.count(),
        #"concerts": concerts,
        #"trackless_concerts": trackless,
        #"complete_concerts": concerts - trackless,
        #"tracks": Track.query.count()
        }


for model in core.Base._decl_class_registry:
    m = core.Base._decl_class_registry.get(model)
    try:
        core.models[m.__tablename__] = m
    except:
        pass
