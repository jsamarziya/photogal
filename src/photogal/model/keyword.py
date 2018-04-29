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


class Keyword(db.Model):
    __tablename__ = 'keyword'

    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), primary_key=True)
    keyword = db.Column(db.String, nullable=False)
    position = db.Column(db.Integer, primary_key=True)

    image = db.relationship("Image", back_populates="keywords")
