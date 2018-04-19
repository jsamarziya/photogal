# Copyright (C) 2018 The Photogal Team.
#
# This file is part of Photogal.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

db = SQLAlchemy()


def register_listeners():
    """
    Registers SQLAlchemy event listeners.
    """

    # noinspection PyUnusedLocal
    @event.listens_for(db.engine, "connect")
    def do_connect(dbapi_connection, connection_record):
        # Disable pysqlite's emitting of the BEGIN statement entirely.
        # Also stops it from emitting COMMIT before any DDL.
        # See http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
        dbapi_connection.isolation_level = None

    @event.listens_for(db.engine, "begin")
    def do_begin(conn):
        # See http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
        conn.execute("BEGIN")


# noinspection PyUnresolvedReferences
from photogal.model.gallery import Gallery
# noinspection PyUnresolvedReferences
from photogal.model.image import Image
