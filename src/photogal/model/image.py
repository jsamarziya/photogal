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

from photogal.database import db


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False)
    # TODO: "title"?
    name = db.Column(db.String)
    description = db.Column(db.String)
    # TODO: "path"? "filename"? "file"?
    location = db.Column(db.String)
    # TODO: not sure if we need width + height
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    creation_day = db.Column(db.Integer)
    creation_month = db.Column(db.Integer)
    creation_year = db.Column(db.Integer)

    # TODO galleries collection
    # TODO keywords collection

    def __repr__(self):
        return "<Image (id={}, name='{}')>".format(self.id, self.name)