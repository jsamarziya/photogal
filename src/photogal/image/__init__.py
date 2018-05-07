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

from PIL import Image as PIL_Image
from flask import current_app as app


def validate_image_file(image_file):
    """Validates that the specified file contains a valid image."""
    PIL_Image.open(image_file)


def save_image_file(image_file, filename):
    """Saves the specified image to the filesystem."""
    app.logger.debug(f"saving image file {image_file} as {filename}")
    # TODO: save the image. (we need a directory, get from app config)
