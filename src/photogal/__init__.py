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
import os

from flask import Flask
from flask import current_app as app
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy


def create_app(config=None) -> Flask:
    """
    Creates the Flask app.
    """
    # noinspection PyShadowingNames
    app = Flask(__name__, instance_path=os.getenv('FLASK_INSTANCE_PATH'), instance_relative_config=True)
    with app.app_context():
        load_config(config)
        init_database()
        init_views()
    return app


def load_config(config=None):
    """
    Loads the application configuration.
    """
    from photogal import config as default_config
    app.logger.debug("Instance path is %s", app.instance_path)
    app.config.from_object(default_config)
    app.config.from_pyfile('photogal.cfg', silent=True)
    if config is not None:
        app.config.from_object(config)
    app.config.from_envvar('PHOTOGAL_CONFIG', silent=True)
    app.logger.debug("Configuration:\n%s", json.dumps(app.config, indent=4, sort_keys=True, default=str))


def init_database() -> SQLAlchemy:
    """
    Initializes the database.
    """
    from photogal.database import db, register_listeners
    db.init_app(app)
    register_listeners()
    db.create_all()
    return db


def init_views():
    from photogal.graphql import schema
    enable_graphiql = app.env == 'development'
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=enable_graphiql))
    app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view('graphql-batch', schema=schema, batch=True))
