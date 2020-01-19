#!/usr/bin/env python3
# Copyright 2020 - David Todd (c0de@c0defox.es)
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

"""
    This file contains the database for authorizing users
    of the simple bookmark application
"""

import datetime
import sqlite3
import uuid

class TelethonDatabase(Database):
    """
        This class contains various methods for interacting
        with the database for the Telethon Authenticator
    """

    def __init__(self, database):
        """
            Sets up the database connection + cursor
            as well as creates a new table if it doesn't
            exist in the database that is provided via the
            instantiation of this class
        """
        super(TelethonDatabase, self).__init__(database)

        # Automatically create the table if it doesn't
        # already exist in the selected database
        self._create_table()

    def _create_table(self):
        """
            Creates a table called `telethon`
            that uses UUID as the primary key.

            The UUID is a randomly generated UUID4

            `client_ip` is the IP address that the server
            recognized when the request was made

            `auth_key` is the key that the user will use when
            making API requests

            `active` is a boolean value for whether or not to
            authorize uses of `auth_key`

            `create_date` and `update_date` are the datetimes
            that the entry was created and updated, respectively.
        """
        query = """
            CREATE TABLE IF NOT EXISTS telethon (
                uuid GUID PRIMARY KEY,
                client_ip TEXT NOT NULL,
                auth_key TEXT NOT NULL,
                active BOOLEAN NOT NULL,
                create_date TIMESTAMP NOT NULL,
                update_date TIMESTAMP
            )
        """
        self.cursor.execute(query)
        self.connection.commit()
