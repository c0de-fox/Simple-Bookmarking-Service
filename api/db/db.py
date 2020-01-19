#!/usr/bin/env python3
# Copyright 2020 - David Todd (c0de@c0defox.es)
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

"""
    This file contains the database for a simple bookmarking application
"""

import datetime
import sqlite3
import uuid

class Database:
    """
        This class contains various methods for interacting
        with the database for the bookmarking engine.
    """

    def __init__(self, database):
        """
            Sets up the database connection + cursor
            as well as creates a new table if it doesn't
            exist in the database that is provided via the
            instantiation of this class
        """

        # Convert UUIDs to bytestring representation when INSERTing
        sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)
        # Convert UUID bytestring back to UUID object when SELECTing
        sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))

        # Used to convert datetime objects (and others in the future)
        detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES

        # Automatically connect to the database when instanced
        self.connection = sqlite3.connect(database, detect_types=detect_types)
        with self.connection:
            self.cursor = self.connection.cursor()

        # Automatically create the table if it doesn't
        # already exist in the selected database
        self._create_table()

    def _create_table(self):
        """
            Creates a table called `bookmarks`
            that uses UUID as the primary key.

            The UUID is generated from the `uri`,
            which will be updated in the case that
            a bookmark's uri gets updated.

            `title` is a short, human readable/recognizable
            string.

            `create_date` and `update_date` are the datetimes
            that the entry was create and updated, respectively.
        """
        query = """
            CREATE TABLE IF NOT EXISTS bookmarks (
                bookmark_id GUID PRIMARY KEY,
                uri TEXT NOT NULL,
                title TEXT NOT NULL,
                create_date TIMESTAMP NOT NULL,
                update_date TIMESTAMP
            )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def get_all_bookmarks(self):
        """
            Returns all bookmarks in the database as a list.
        """
        query = "SELECT * FROM bookmarks"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_bookmark(self, bookmark_id):
        """
            With the provided `bookmark_id`, the database will be
            searched for a matching entry, with the row returned
            if there is a match. If there is no match, None will
            be returned.

            `bookmark_id` is of type uuid.UUID()
        """
        query = "SELECT * FROM bookmarks WHERE bookmark_id = ?"
        self.cursor.execute(query, (bookmark_id, ))
        return self.cursor.fetchone()

    def save_bookmark(self, uri, title):
        """
            Determines if the provided `uri` doesn't already
            exist in the database adding a new entry if that
            is the case. If the `uri` is already stored
            (based on the generated UUID), the existing
            entry's UUID will be returned instead.
        """
        uri_uuid = uuid.uuid5(uuid.NAMESPACE_URL, uri)

        bookmark_exists = self.get_bookmark(uri_uuid)
        if bookmark_exists != None:
            return bookmark_exists[0]

        query = """
            INSERT INTO bookmarks (
                bookmark_id, uri, title, create_date
            ) VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (uri_uuid, uri, title, datetime.datetime.now()))
        self.connection.commit()
        return uri_uuid

    def delete_bookmark(self, bookmark_id):
        """
            Removes the bookmark entry if it exists

            `bookmark_id` is of type uuid.UUID()

            Returns True upon successful removal.
            Returns False upon unsuccessful removal.
        """
        if self.get_bookmark(bookmark_id) != None:
            query = "DELETE FROM bookmarks WHERE bookmark_id = ?"
            self.cursor.execute(query, (bookmark_id, ))

        if self.get_bookmark(bookmark_id) == None:
            return True
        return False

    def update_bookmark_title(self, bookmark_id, new_title):
        """
            Takes the provided `bookmark_id`, searches the
            database for the matching record, and if found
            the title will be replaced with `new_title`.

            `bookmark_id` is of type uuid.UUID()

            Returns None if there is no matching bookmark.
        """
        bookmark = self.get_bookmark(bookmark_id)
        if bookmark != None:
            query = """
                UPDATE bookmarks
                SET title = ?, update_date = ?
                WHERE bookmark_id = ?
            """
            self.cursor.execute(query, (new_title, datetime.datetime.now(), bookmark_id, ))
            self.connection.commit()
            return self.get_bookmark(bookmark_id)
        return None

    def update_bookmark_uri(self, bookmark_id, new_uri):
        """
            Takes the provided `bookmark_id`, searches the
            database for the matching record, and if found
            the URI will be replaced with `new_uri`.

            `bookmark_id` is of type uuid.UUID()

            A new `bookmark_id` will be generated if the
            `new_uri` is different than what was previously
            stored. If the newly generated `bookmark_id` matches
            an existing entry, this method will return False.
            You may want to delete the old bookmark in this case.

            Returns None if there is no matching bookmark.
        """
        bookmark = self.get_bookmark(bookmark_id)
        if bookmark != None:
            query = """
                UPDATE bookmarks
                SET bookmark_id = ?, uri = ?, update_date = ?
                WHERE bookmark_id = ?
            """
            new_bookmark_id = uuid.uuid5(uuid.NAMESPACE_URL, new_uri)
            if self.get_bookmark(new_bookmark_id) == None:
                self.cursor.execute(query, (new_bookmark_id, new_uri, datetime.datetime.now(), bookmark_id, ))
                self.connection.commit()
                return self.get_bookmark(new_bookmark_id)
            return False
        return None


