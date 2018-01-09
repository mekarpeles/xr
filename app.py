#!/usr/bin/env python
# -*-coding: utf-8 -*-

"""
    app.py
    ~~~~~~

    :copyright: (c) 2015 by Mek
    :license: see LICENSE for more details.
"""

from flask import Flask
from flask.ext.routing import router
from flask.ext.cors import CORS

import views
from views import endpoints
from configs import options, SECRET_KEY


urls = ('/favicon.ico', views.Favicon,
        '', endpoints
        )

app = router(Flask(__name__), urls)
app.secret_key = SECRET_KEY
CORS(app, resources=r'*', allow_headers='Content-Type')

if __name__ == "__main__":
    app.run(**options)
