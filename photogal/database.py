from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

from photogal.application import app

db = SQLAlchemy(app)


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
