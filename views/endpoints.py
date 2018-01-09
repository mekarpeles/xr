#!/usr/bin/env python
# -*-coding: utf-8 -*-

"""
    __init__.py
    ~~~~~~~~~~~
    XR API Endpoints

    :copyright: (c) 2015 by Mek Karpeles
    :license: see LICENSE for more details.
"""

from flask import request
from flask.views import MethodView
from views import rest_api, paginate
from api import xr as api


class Exercises(MethodView):

    @rest_api
    def get(self, xrz_id=None):
        return [e.dict() for e in api.Exercise.all()]


class Checkins(MethodView):

    @rest_api
    def get(self, checkin_id=None):
        return [c.dict() for c in api.Checkin.all()]


    @rest_api
    def post(self):
        i = request.json
        exercise = int(i.get('eid'))
        # c = Checkin(exercise_id=eid)
        # How do I specify a time other than created? (user account timezone? datepicker)
        # c.create()
        return request.json


class Users(MethodView):

    @rest_api
    def get(self, user_id=None):
        return [u.dict() for u in api.User.all()]

class Index(MethodView):
    @rest_api
    def get(self):
        return {"endpoints": api.core.models.keys()}


urls = (
    '/api/users', Users,
    '/api/exercises', Exercises,
    '/api/checkins', Checkins,
    '/', Index
)
