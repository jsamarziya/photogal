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
from graphene.test import Client
from photogal.database.model import Image


def test_create_image(graphene_client: Client):
    result = graphene_client.execute('''
    mutation {
        createImage(name: "myImage") {
            image {
                imageId
                name
                public
                keywords
`                imageDate
            }
        }
    }
    ''')
    assert_that(json.dumps(result)).is_equal_to_ignoring_whitespace('''
    {
        "data": {
            "createImage": {
                "image": {
                    "imageId": 1,
                    "name": "myImage",
                    "public": false,
                    "keywords": [],
                    "imageDate": null
                }
            }
        }
    }
    ''')
    image = Image.query.get(1)
    assert_that(image.id).is_equal_to(1)
    assert_that(image.name).is_equal_to('myImage')
    assert_that(image.public).is_false()
    assert_that(image.keywords).is_empty()
    assert_that(image.image_date).is_none()


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
    assert_that(json.dumps(result)).is_equal_to_ignoring_whitespace('''
    {
        "data": {
            "createImage": {
                "image": {
                    "keywords": [
                        "foo",
                        "bar",
                        "baz"
                    ]
                }
            }
        }
    }
    ''')
    image = Image.query.get(1)
    assert_that([keyword.keyword for keyword in image.keywords]).contains_sequence("foo", "bar", "baz")


def test_create_image_with_image_date(graphene_client: Client):
    result = graphene_client.execute('''
    mutation {
        createImage(imageDate: "2017-01-12") {
            image {
                imageDate
            }
        }
    }
    ''')
    assert_that(json.dumps(result)).is_equal_to_ignoring_whitespace('''
    {
        "data": {
            "createImage": {
                "image": {
                    "imageDate": "2017-01-12"
                }
            }
        }
    }
    ''')
    image = Image.query.get(1)
    assert_that(image.image_date).is_equal_to("2017-01-12")


def test_create_image_with_invalid_image_date(graphene_client: Client):
    result = graphene_client.execute('''
    mutation {
        createImage(imageDate: "2017-1-12") {
            image {
                imageDate
            }
        }
    }
    ''')
    assert_that(result['errors'][0]['message']).is_equal_to("'2017-1-12' is not a valid imageDate")
