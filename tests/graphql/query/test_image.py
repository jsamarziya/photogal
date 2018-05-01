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
from photogal.database.model import Image


def test_query_image_no_id(graphene_client: Client):
    result = graphene_client.execute('''
    query {
        image {
            imageId
        }
    }
    ''')
    assert_that(result['errors'][0]['message']).is_equal_to('Either id or image_id must be specified')


def test_query_nonexistent_image(graphene_client: Client):
    result = graphene_client.execute('''
    query {
        image(imageId: 1) {
            imageId
        }
    }
    ''')
    assert_that(json.dumps(result)).is_equal_to_ignoring_whitespace('''
    {
        "data": {
            "image": null
        }
    }
    ''')


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
    assert_that(json.dumps(result)).is_equal_to_ignoring_whitespace('''
    { 
        "data": {
            "image": {
                 "imageId": 1,
                  "name": "myImage",
                   "public": false,
                   "keywords": [
                       "keyword1", 
                       "keyword2"
                   ]
            }
        }
    }
    ''')


def test_query_image_by_id(db: SQLAlchemy, graphene_client: Client):
    image = Image()
    db.session.add(image)
    db.session.commit()

    result = graphene_client.execute(f'''
    query {{
        image(id: "{to_global_id("Image", 1)}") {{
            imageId
        }}
    }}
    ''')
    assert_that(json.dumps(result)).is_equal_to_ignoring_whitespace('''
    {
        "data": {
            "image": {
                "imageId": 1
            }
        }
    }
    ''')


def test_query_image_by_id_wrong_type(graphene_client: Client):
    result = graphene_client.execute(f'''
    query {{
        image(id: "{to_global_id("Gallery", 1)}") {{
            imageId
        }}
    }}
    ''')
    assert_that(result['errors'][0]['message']).is_equal_to("Wrong id type (expected 'Image', got 'Gallery'")
