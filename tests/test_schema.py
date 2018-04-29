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

from collections import OrderedDict

from assertpy import assert_that
from flask_sqlalchemy import SQLAlchemy
from graphene.test import Client
from photogal.database.model import Gallery, Image


def test_query_nonexistent_gallery(graphene_client: Client):
    result = graphene_client.execute('''
    query {
        gallery(galleryId: 1) {
            galleryId
        }
    }
    ''')
    assert_that(result).is_equal_to({
        'data': {
            'gallery': None
        }
    })


def test_query_gallery(db: SQLAlchemy, graphene_client: Client):
    gallery = Gallery(name="myGallery", public=False)
    db.session.add(gallery)
    db.session.commit()
    result = graphene_client.execute('''
    query {
        gallery(galleryId: 1) {
            galleryId
            name
            public
        }
    }
    ''')
    assert_that(result).is_equal_to({
        'data':
            OrderedDict([('gallery',
                          OrderedDict([('galleryId', 1),
                                       ('name', 'myGallery'),
                                       ('public', False)
                                       ])
                          )])
    })


def test_create_gallery(graphene_client: Client):
    result = graphene_client.execute('''
    mutation {
        createGallery(name: "galleryName", public: true, position: 78) {
            gallery {
                galleryId
                name
                public
                position
            }
        }
    }
    ''')
    assert_that(result).is_equal_to({
        'data':
            OrderedDict([('createGallery',
                          OrderedDict([('gallery',
                                        OrderedDict([('galleryId', 1),
                                                     ('name', 'galleryName'),
                                                     ('public', True),
                                                     ('position', 78)
                                                     ])
                                        )])
                          )])
    })
    gallery = Gallery.query.get(1)
    assert_that(gallery.id).is_equal_to(1)
    assert_that(gallery.name).is_equal_to('galleryName')
    assert_that(gallery.public).is_true()
    assert_that(gallery.position).is_equal_to(78)


def test_query_nonexistent_image(graphene_client: Client):
    result = graphene_client.execute('''
    query {
        image(imageId: 1) {
            imageId
        }
    }
    ''')
    assert_that(result).is_equal_to({
        'data': {
            'image': None
        }
    })


def test_query_image(db: SQLAlchemy, graphene_client: Client):
    image = Image(name="myImage")
    image.set_keywords("keyword1", "keyword2")
    db.session.add(image)
    db.session.commit()
    result = graphene_client.execute('''
    query {
        image(imageId: 1) {
            imageId
            name
            public
            keywords
        }
    }
    ''')
    assert_that(result).is_equal_to({
        'data':
            OrderedDict([('image',
                          OrderedDict([('imageId', 1),
                                       ('name', 'myImage'),
                                       ('public', False),
                                       ('keywords', ["keyword1", "keyword2"])
                                       ])
                          )])
    })


def test_create_image(graphene_client: Client):
    result = graphene_client.execute('''
    mutation {
        createImage(name: "myImage") {
            image {
                imageId
                name
                public
                keywords
            }
        }
    }
    ''')
    assert_that(result).is_equal_to({
        'data':
            OrderedDict([('createImage',
                          OrderedDict([('image',
                                        OrderedDict([('imageId', 1),
                                                     ('name', 'myImage'),
                                                     ('public', False),
                                                     ('keywords', [])
                                                     ])
                                        )])
                          )])
    })
    image = Image.query.get(1)
    assert_that(image.id).is_equal_to(1)
    assert_that(image.name).is_equal_to('myImage')
    assert_that(image.public).is_false()
    assert_that(image.keywords).is_empty()


def test_create_image_with_keywords(graphene_client: Client):
    result = graphene_client.execute('''
    mutation {
        createImage(name: "myImage", keywords: ["foo", "bar", "baz"]) {
            image {
                keywords
            }
        }
    }
    ''')
    assert_that(result).is_equal_to({
        'data':
            OrderedDict([('createImage',
                          OrderedDict([('image',
                                        OrderedDict([('keywords',
                                                      ['foo', 'bar', 'baz'])])
                                        )])
                          )])
    })
    image = Image.query.get(1)
    assert_that([keyword.keyword for keyword in image.keywords]).contains_sequence("foo", "bar", "baz")
