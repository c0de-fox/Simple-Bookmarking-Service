#!/usr/bin/env python3
# Copyright 2020 - David Todd (c0de@c0defox.es)
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

"""
    This file contains the web server for a simple bookmarking application
"""

from bottle import Bottle, run, response, route, template
from api import API

_api = API()

@route('/')
def index():
    return template("This is the index")

# I haven't figured out how to get these routes inside the API yet...
@route('/save/<title>/<uri:path>')
def save_bookmark(title, uri):
    return _api.save_bookmark(title, uri)

@route('/getall')
@route('/get/all')
def get_all_bookmarks():
    return _api.get_all_bookmarks()

@route('/get/<bookmark_id>')
def get_bookmark(bookmark_id):
    return _api.get_bookmark(bookmark_id)

@route('/delete/<bookmark_id>')
def delete_bookmark(bookmark_id):
    return _api.delete_bookmark(bookmark_id)

@route('/update/title/<bookmark_id>/<title>')
def update_bookmark_title(bookmark_id, title):
    return _api.update_bookmark_title(bookmark_id, title)

@route('/update/uri/<bookmark_id>/<uri:path>')
def update_bookmark_uri(bookmark_id, uri):
    return _api.update_bookmark_uri(bookmark_id, uri)

if __name__ == '__main__':
    run(host='localhost', port=8080)
