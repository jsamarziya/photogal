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

from assertpy import assert_that
from flask_sqlalchemy import SQLAlchemy
from graphene.test import Client
from graphql_relay import to_global_id
from photogal.database.model import Gallery


def test_delete_nonexistent_gallery(graphene_client: Client):
    result = graphene_client.execute('''
    mutation {
        deleteGallery(galleryId: 1) {
            gallery {
                galleryId,
                name
            }
        }
    }
    ''')
    assert_that(json.dumps(result)).is_equal_to_ignoring_whitespace('''
    {
        "data": {
            "deleteGallery": {
                "gallery": null
            }
        }
    }''')


def test_delete_gallery_by_id(db: SQLAlchemy, graphene_client: Client):
    gallery = Gallery(name="myGallery")
    db.session.add(gallery)
    db.session.commit()
    assert_that(Gallery.query.get(1)).is_not_none()

    result = graphene_client.execute(f'''
    mutation {{
        deleteGallery(id: "{to_global_id("Gallery", 1)}") {{
            gallery {{
                galleryId,
                name                
            }}
        }}
    }}
    ''')
    assert_that(json.dumps(result)).is_equal_to_ignoring_whitespace('''
    {
        "data": {
            "deleteGallery": {
                "gallery": {
                    "galleryId": 1,
                    "name": "myGallery"
                }
            }
        }
    }''')
    assert_that(Gallery.query.get(1)).is_none()


def test_delete_gallery_by_gallery_id(db: SQLAlchemy, graphene_client: Client):
    gallery = Gallery(name="myGallery")
    db.session.add(gallery)
    db.session.commit()
    assert_that(Gallery.query.get(1)).is_not_none()

    result = graphene_client.execute('''
    mutation {
        deleteGallery(galleryId: 1) {
            gallery {
                galleryId,
                name
            }
        }
    }
    ''')
    assert_that(json.dumps(result)).is_equal_to_ignoring_whitespace('''
    {
        "data": {
            "deleteGallery": {
                "gallery": {
                    "galleryId": 1,
                    "name": "myGallery"
                }
            }
        }
    }''')
    assert_that(Gallery.query.get(1)).is_none()
