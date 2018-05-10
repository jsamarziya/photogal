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
import filecmp

import pytest
from assertpy import assert_that
from photogal import Photogal
from photogal.image import validate_image_file, save_image_file
from werkzeug.datastructures import FileStorage


def test_validate_image_file(shared_datadir):
    for file in ['x.gif', 'einstein.jpg', 'nosferatu.png', 'liberty.bmp']:
        validate_image_file(shared_datadir / file)


def test_validate_image_file_invalid(shared_datadir):
    with pytest.raises(OSError) as ex:
        validate_image_file(shared_datadir / 'test.txt')
    assert_that(str(ex.value)).matches("cannot identify image file")


def test_save_image_file(app: Photogal, shared_datadir):
    image_file = shared_datadir / 'einstein.jpg'
    with open(image_file, 'rb') as stream:
        file_storage = FileStorage(stream=stream)
        filename = save_image_file(file_storage)
    assert_that(filename).is_file()
    assert_that(filename).is_child_of(app.image_directory)
    assert_that(filecmp.cmp(image_file, filename)).is_true()
