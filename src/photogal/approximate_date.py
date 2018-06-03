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
import re

repr_pattern = re.compile(r'^(\d+)(-\d\d)?(-\d\d)?$')
str_pattern = re.compile(r'(\d+)-(\d\d)-(\d\d)')


# noinspection PyShadowingBuiltins
def repr(value):
    """Normalizes an approximate_date"""
    match = repr_pattern.match(value)
    if match is None:
        raise ValueError
    year, month, day = match.group(1, 2, 3)
    if month is None:
        month = "-00"
    if day is None:
        day = "-00"
    return f"{year}{month}{day}"


# noinspection PyShadowingBuiltins,PyShadowingNames
def str(value):
    """Formats an approximate_date in a human-readable format"""
    match = str_pattern.match(value)
    if match is None:
        raise ValueError
    year, month, day = match.group(1, 2, 3)
    str = year
    if month != '00':
        str += f"-{month}"
        if day != '00':
            str += f"-{day}"
    return str
