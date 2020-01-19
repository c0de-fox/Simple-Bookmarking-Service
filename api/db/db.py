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
        Base database class that is shared by the bookmark
        engine and the Telethon authenticator
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
