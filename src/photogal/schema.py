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

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from photogal.model import Gallery as GalleryModel, Image as ImageModel


class Gallery(SQLAlchemyObjectType):
    class Meta:
        model = GalleryModel
        interfaces = (relay.Node,)


class Image(SQLAlchemyObjectType):
    class Meta:
        model = ImageModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    gallery = graphene.Field(Gallery, id=graphene.Int())
    image = graphene.Field(Image, id=graphene.Int())
    galleries = SQLAlchemyConnectionField(Gallery)
    images = SQLAlchemyConnectionField(Image)

    # noinspection PyMethodMayBeStatic
    def resolve_gallery(self, info, **args):
        query = Gallery.get_query(info)
        gallery_id = args.get('id')
        return query.filter(GalleryModel.id == gallery_id).first()

    # noinspection PyMethodMayBeStatic
    def resolve_image(self, info, **args):
        query = Image.get_query(info)
        image_id = args.get('id')
        return query.filter(ImageModel.id == image_id).first()


schema = graphene.Schema(query=Query, types=[Gallery, Image])
