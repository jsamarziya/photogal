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
import pytest
from assertpy import assert_that
from photogal.image import validate_image_file


def test_validate_image_file(shared_datadir):
    for file in ['x.gif', 'einstein.jpg', 'nosferatu.png', 'liberty.bmp']:
        validate_image_file(shared_datadir / file)


def test_validate_image_file_invalid(shared_datadir):
    with pytest.raises(OSError) as excinfo:
        validate_image_file(shared_datadir / 'test.txt')
    assert_that(str(excinfo.value)).matches("cannot identify image file")
