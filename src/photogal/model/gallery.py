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

from photogal.database import db, register_last_modified_trigger_listener
from sqlalchemy import text


class Gallery(db.Model):
    __tablename__ = "galleries"

    gallery_id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_modified = db.Column(db.DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    order_index = db.Column(db.Integer)
    public = db.Column(db.Boolean)
    gallery_image_id = db.Column(db.Integer, db.ForeignKey("images.id"))

    # TODO: images collection

    def __repr__(self):
        return "<Gallery (id={}, name='{}')>".format(self.id, self.name)


register_last_modified_trigger_listener(Gallery.__table__)
