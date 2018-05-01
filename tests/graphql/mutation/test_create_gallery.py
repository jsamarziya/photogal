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
from photogal.database.model import Gallery


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
    assert_that(json.dumps(result)).is_equal_to_ignoring_whitespace('''
    {
        "data": {
            "createGallery": {
                "gallery": {
                    "galleryId": 1,
                    "name": "galleryName",
                    "public": true,
                    "position": 78
                }
            }
        }
    }''')
    gallery = Gallery.query.get(1)
    assert_that(gallery.id).is_equal_to(1)
    assert_that(gallery.name).is_equal_to('galleryName')
    assert_that(gallery.public).is_true()
    assert_that(gallery.position).is_equal_to(78)
