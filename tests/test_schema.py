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
    assert result == {
        'data': {
            'gallery': None
        }
    }


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
    assert result == {
        'data':
            OrderedDict([('gallery',
                          OrderedDict([('galleryId', 1),
                                       ('name', 'myGallery'),
                                       ('public', False)
                                       ])
                          )])
    }


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
    assert result == {
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
    }
    gallery = Gallery.query.get(1)
    assert gallery.id == 1
    assert gallery.name == 'galleryName'
    assert gallery.public is True
    assert gallery.position == 78


def test_query_nonexistent_image(graphene_client: Client):
    result = graphene_client.execute('''
    query {
        image(imageId: 1) {
            imageId
        }
    }
    ''')
    assert result == {
        'data': {
            'image': None
        }
    }


def test_query_image(db: SQLAlchemy, graphene_client: Client):
    image = Image(name="myImage")
    db.session.add(image)
    db.session.commit()
    result = graphene_client.execute('''
    query {
        image(imageId: 1) {
            imageId
            name
            public
        }
    }
    ''')
    assert result == {
        'data':
            OrderedDict([('image',
                          OrderedDict([('imageId', 1),
                                       ('name', 'myImage'),
                                       ('public', False)
                                       ])
                          )])
    }


def test_create_image(graphene_client: Client):
    result = graphene_client.execute('''
    mutation {
        createImage(name: "myImage") {
            image {
                imageId
                name
                public
            }
        }
    }
    ''')
    assert result == {
        'data':
            OrderedDict([('createImage',
                          OrderedDict([('image',
                                        OrderedDict([('imageId', 1),
                                                     ('name', 'myImage'),
                                                     ('public', False)
                                                     ])
                                        )])
                          )])
    }
    image = Image.query.get(1)
    assert image.id == 1
    assert image.name == 'myImage'
    assert image.public is False
