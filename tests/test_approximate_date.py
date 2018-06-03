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
from photogal import approximate_date


# noinspection PyShadowingBuiltins
def test_repr():
    for value, repr in [
        ("1992", "1992-00-00"),
        ("2014-06", "2014-06-00"),
        ("1917-12-14", "1917-12-14")
    ]:
        assert_that(approximate_date.repr(value)).is_equal_to(repr)
    for value in [
        "",
        "foo",
        "1992-",
        "1992-4",
        "1992-1-1"
    ]:
        with pytest.raises(ValueError, message=f"for value {value}"):
            approximate_date.repr(value)


# noinspection PyShadowingBuiltins
def test_str():
    for value, str in [
        ("1992-00-00", "1992"),
        ("2014-06-00", "2014-06"),
        ("1917-12-14", "1917-12-14")
    ]:
        assert_that(approximate_date.str(value)).is_equal_to(str)
    for value in [
        "",
        "foo"
    ]:
        with pytest.raises(ValueError):
            approximate_date.str(value)
