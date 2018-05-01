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

import json

from flask import Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy

from . import config as default_config


def create_app(config=None) -> Flask:
    """
    Creates the Flask app.
    """
    app = Flask('photogal', instance_relative_config=True)
    load_config(app, config)
    init_database(app)
    init_views(app)
    return app


def load_config(app, config=None):
    """
    Loads the application configuration.
    """
    app.logger.debug("Instance path is %s", app.instance_path)
    app.config.from_object(default_config)
    app.config.from_pyfile('photogal.cfg', silent=True)
    if config is not None:
        app.config.from_object(config)
    app.config.from_envvar('PHOTOGAL_CONFIG', silent=True)
    app.logger.debug("Configuration:\n%s", json.dumps(app.config, indent=4, sort_keys=True, default=str))


def init_database(app: Flask) -> SQLAlchemy:
    """
    Initializes the database.
    """
    from photogal.database import db, register_listeners
    db.init_app(app)
    with app.app_context():
        register_listeners()
        db.create_all()
    return db


def init_views(app: Flask):
    from .graphql import schema
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view('graphql-batch', schema=schema, batch=True))
