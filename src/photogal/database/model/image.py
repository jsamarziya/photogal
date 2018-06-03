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
from photogal import approximate_date
from photogal.database import db, register_last_modified_trigger_listener

from photogal.database.model.keyword import Keyword
from sqlalchemy.ext.hybrid import hybrid_property


class Image(db.Model):
    """A photographic image."""

    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
    last_modified = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    # The filename that was specified when the image was uploaded
    filename = db.Column(db.String)
    # TODO: not sure if we need width + height. What do we use it for?
    # TODO: width and height were formerly non-null...
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    _image_date = db.Column("image_date", db.String)

    galleries = db.relationship("GalleryImage",
                                back_populates="image",
                                cascade="save-update, merge, delete, delete-orphan")
    keywords = db.relationship("Keyword",
                               back_populates="image",
                               order_by="Keyword.position",
                               cascade="save-update, merge, delete, delete-orphan")

    def __repr__(self):
        return f"<Image (id={self.id}, name='{self.name}')>"

    @hybrid_property
    def image_date(self):
        return None if self._image_date is None else approximate_date.str(self._image_date)

    @image_date.setter
    def image_date(self, value):
        self._image_date = None if value is None else approximate_date.repr(value)

    # TODO do we want hybrid read-only properties for year/month/date?

    def set_keywords(self, *keywords):
        self.keywords = [Keyword(image=self, keyword=keyword, position=index) for index, keyword in enumerate(keywords)]


register_last_modified_trigger_listener(Image.__table__)
