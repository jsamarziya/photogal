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

import time
from datetime import datetime

import pytest
from assertpy import assert_that
from flask_sqlalchemy import SQLAlchemy
from photogal.model.gallery import Gallery

pytestmark = pytest.mark.usefixtures("db")


def test_query_all_no_galleries():
    assert_that(Gallery.query.all()).is_empty()


def test_query_all_with_gallery(db: SQLAlchemy):
    gallery = Gallery(name="myGallery")
    db.session.add(gallery)
    db.session.commit()
    assert_that(Gallery.query.all()).contains_only(gallery)


def test_add_sets_defaults(db: SQLAlchemy):
    gallery = Gallery(name="myGallery")
    assert_that(gallery.created).is_none()
    assert_that(gallery.last_modified).is_none()
    db.session.add(gallery)
    db.session.commit()
    assert_that(gallery.created).is_not_none()
    assert_that(gallery.last_modified).is_equal_to(gallery.created)


def test_last_modified_trigger(db: SQLAlchemy):
    gallery = Gallery(name="myGallery")
    db.session.add(gallery)
    db.session.commit()
    assert_that(gallery.last_modified).is_equal_to(gallery.created)
    time.sleep(1)
    gallery.description = "myDescription"
    db.session.commit()
    assert_that((gallery.last_modified - gallery.created).seconds).is_greater_than_or_equal_to(1)


def test_last_modified(db: SQLAlchemy):
    """
    Verifies that we can set a last_modified value when the object is created, but the trigger will still update it
    """
    last_modified = datetime.fromtimestamp(0)
    gallery = Gallery(last_modified=last_modified)
    db.session.add(gallery)
    db.session.commit()
    assert_that(gallery.last_modified).is_equal_to(last_modified)
    gallery.description = "myDescription"
    db.session.commit()
    assert_that(gallery.last_modified).is_not_equal_to(last_modified)
