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

import photogal.application
import photogal.database
import pytest
from assertpy.assertpy import AssertionBuilder
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from graphene.test import Client
from photogal.graphql import schema


@pytest.fixture
def app() -> Flask:
    from . import config
    return photogal.application.create_app(config)


# noinspection PyUnusedLocal
@pytest.fixture
def db(app) -> SQLAlchemy:
    return photogal.database.db


# noinspection PyUnusedLocal
@pytest.fixture
def graphene_client(db) -> Client:
    return Client(schema)


def remove_whitespace(s):
    import string
    return s.translate({ord(c): None for c in string.whitespace})


def is_equal_to_ignoring_whitespace(self, other):
    from assertpy.assertpy import str_types
    if not isinstance(self.val, str_types):
        raise TypeError('val is not a string')
    if not isinstance(other, str_types):
        raise TypeError('given arg must be a string')
    if remove_whitespace(self.val) != remove_whitespace(other):
        self._err('Expected <%s> to be equal (ignoring whitespace) to <%s>, but was not.' % (self.val, other))
    return self


AssertionBuilder.is_equal_to_ignoring_whitespace = is_equal_to_ignoring_whitespace
