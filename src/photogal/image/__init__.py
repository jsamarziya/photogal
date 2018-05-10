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
import contextlib
import os
import tempfile

from PIL import Image as PIL_Image
from flask import current_app as app
from werkzeug.datastructures import FileStorage


def validate_image_file(image_file):
    """Validates that the specified file contains a valid image."""
    PIL_Image.open(image_file)


def save_image_file(image_file: FileStorage) -> str:
    """Saves the specified image to the filesystem."""
    fd, filename = tempfile.mkstemp(dir=app.image_directory)
    try:
        app.logger.debug(f"Saving image file {image_file} as {filename}")
        with open(fd, 'wb') as f:
            image_file.save(f)
        validate_image_file(filename)
    except Exception as e:
        with contextlib.suppress(OSError):
            os.remove(filename)
        raise e
    return filename
