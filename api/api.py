#!/usr/bin/env python3
# Copyright 2020 - David Todd (c0de@c0defox.es)
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

"""
    This file contains the API for a simple bookmarking application
"""

import json
import datetime
from pprint import pprint
from uuid import UUID
from bottle import response, abort
from .db import Database

class API:
    """
        This class contains various methods for a simple bookmarking application API

        As of right now, these are mostly just to pass data through to the database.
        Stuff should be sanitized here though
    """

    def __init__(self):
        """
            Setup some internal variables, such as various constants
            and the database connection
        """
        self.database = Database('bookmarks.db')
        self.dt_fmt = "%H:%M:%S on %B %d %Y"
        self.response_type = 'application/json'
        self.format_date = datetime.datetime.strftime

    def _get_bookmark_object(self, bookmark):
        """
            Shortcut to return the `bookmark_object` that several methods return
        """
        # Maybe I need to use `sqlite3.Cursor.description` or `sqlite3.Row.keys()`
        return {
            'uuid': bookmark[0].hex,
            'uri': bookmark[1],
            'title': bookmark[2],
            'date_created': self.format_date(bookmark[3], self.dt_fmt),
            'date_updated': self.format_date(bookmark[4], self.dt_fmt) if bookmark[4] != None else '',
        }

    def save_bookmark(self, title, uri):
        """
            Save the bookmark with `title` and `uri`

            Returns a JSON object containing
            the UUID of the saved bookmark
        """
        response.content_type = self.response_type
        bookmark = self.database.save_bookmark(uri, title)

        return json.dumps({
            'uuid': bookmark.hex
        })

    def get_bookmark(self, bookmark_id):
        """
            Get the bookmark with the provided `bookmark_id`

            `bookmark_id` is of type string
            Returns a JSON object containing
            everything about the bookmark
        """
        response.content_type = self.response_type
        bookmark = self.database.get_bookmark(UUID(bookmark_id))

        if bookmark == None:
            return abort(404, "Provided bookmark doesn't exist or has been deleted")

        return json.dumps(self._get_bookmark_object(bookmark))

    def get_all_bookmarks(self):
        """
            Gets all of the bookmarks that are currently saved

            Returns a JSON object containing
            everything about each bookmark
        """
        response.content_type = self.response_type
        bookmarks = self.database.get_all_bookmarks()

        if len(bookmarks) == 0:
            return abort(404, "There are no bookmarks saved")

        bookmark_object = [
            {
                'uuid': bookmark[0].hex,
                'uri': bookmark[1],
                'title': bookmark[2],
                'date_created': self.format_date(bookmark[3], self.dt_fmt),
                'date_updated': self.format_date(bookmark[4], self.dt_fmt) if bookmark[4] != None else '',
            } for bookmark in bookmarks
        ]

        return json.dumps(bookmark_object)

    def delete_bookmark(self, bookmark_id):
        """
            Deletes the bookmark that is associated with `bookmark_id`

            Returns a JSON object containing the bookmark's UUID,
            and the status as to whether or not it was successfully deleted
        """
        response.content_type = self.response_type
        return json.dumps({
            'uuid': bookmark_id,
            'bookmark_deleted': self.database.delete_bookmark(UUID(bookmark_id)),
        })

    def update_bookmark_title(self, bookmark_id, title):
        """
            Updates the bookmark that is associated
            with `bookmark_id` with the provided `title`

            Returns a JSON object containing
            everything about the bookmark
        """
        response.content_type = self.response_type
        bookmark = self.database.update_bookmark_title(bookmark_id, title)

        if bookmark == None:
            return abort(404, "Provided bookmark doesn't exist or has been deleted")

        return json.dumps(self._get_bookmark_object(bookmark))

    def update_bookmark_uri(self, bookmark_id, uri):
        """
            Updates the bookmark that is associated
            with `bookmark_id` with the provided `uri`

            This action will change the `bookmark_id`

            Returns a JSON object containing
            everything about the bookmark
        """
        response.content_type = self.response_type
        bookmark = self.database.update_bookmark_uri(bookmark_id, uri)

        if bookmark == None:
            return abort(404, "Provided bookmark doesn't exist or has been deleted")

        return json.dumps(self._get_bookmark_object(bookmark))
