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
from photogal.database.model import Image, Keyword, Gallery, GalleryImage

pytestmark = pytest.mark.usefixtures("db")


def test_repr():
    assert_that(repr(Image(id=31, name="my image"))).is_equal_to("<Image (id=31, name='my image')>")


def test_query_all_no_images():
    assert_that(Image.query.all()).is_empty()


def test_query_all_with_images(db: SQLAlchemy):
    image = Image(name="myImage")
    db.session.add(image)
    db.session.commit()
    assert_that(Image.query.all()).contains_only(image)


def test_add_sets_defaults(db: SQLAlchemy):
    image = Image(name="myImage")
    assert_that(image.created).is_none()
    assert_that(image.last_modified).is_none()

    db.session.add(image)
    db.session.commit()
    assert_that(image.created).is_not_none()
    assert_that(image.last_modified).is_equal_to(image.created)


def test_last_modified_trigger(db: SQLAlchemy):
    image = Image(name="myImage")
    db.session.add(image)
    db.session.commit()
    assert_that(image.last_modified).is_equal_to(image.created)

    time.sleep(1)

    image.description = "myDescription"
    db.session.commit()
    assert_that((image.last_modified - image.created).seconds).is_greater_than_or_equal_to(1)


def test_last_modified(db: SQLAlchemy):
    """
    Verifies that we can set a last_modified value when the object is created, but the trigger will still update it
    """
    last_modified = datetime.fromtimestamp(0)
    image = Image(last_modified=last_modified)
    db.session.add(image)
    db.session.commit()
    assert_that(image.last_modified).is_equal_to(last_modified)

    image.description = "myDescription"
    db.session.commit()
    assert_that(image.last_modified).is_not_equal_to(last_modified)


def test_public(db: SQLAlchemy):
    image = Image()
    db.session.add(image)
    db.session.commit()
    assert_that(image.public).is_false()

    gallery = Gallery(public=False)
    gallery.images.append(GalleryImage(image=image, position=0))
    db.session.add(gallery)
    db.session.commit()
    assert_that(image.public).is_false()

    gallery.public = True
    db.session.commit()
    assert_that(image.public).is_true()


def test_keywords(db: SQLAlchemy):
    image = Image()
    db.session.add(image)
    db.session.commit()
    assert_that(image.keywords).is_empty()

    image.keywords.append(Keyword(image=image, position=0, keyword="foo"))
    image.keywords.append(Keyword(image=image, position=2, keyword="baz"))
    image.keywords.append(Keyword(image=image, position=1, keyword="bar"))
    db.session.commit()
    assert_that([i.keyword for i in image.keywords]).contains_sequence("foo", "bar", "baz")

    image.keywords.remove(image.keywords[0])
    db.session.commit()
    assert_that([i.keyword for i in image.keywords]).contains_sequence("bar", "baz")


def test_set_keywords(db: SQLAlchemy):
    image = Image()
    db.session.add(image)
    db.session.commit()
    assert_that(image.keywords).is_empty()

    image.set_keywords(*"foo bar baz".split())
    db.session.commit()
    assert_that([i.keyword for i in image.keywords]).contains_sequence("foo", "bar", "baz")

    image.set_keywords(*"foo baz bar".split())
    db.session.commit()
    assert_that([i.keyword for i in image.keywords]).contains_sequence("foo", "baz", "bar")

    image.set_keywords(*"a b".split())
    db.session.commit()
    assert_that([i.keyword for i in image.keywords]).contains_sequence("a", "b")

    image.set_keywords("one")
    db.session.commit()
    assert_that([i.keyword for i in image.keywords]).contains_sequence("one")

    image.set_keywords()
    db.session.commit()
    assert_that(image.keywords).is_empty()
