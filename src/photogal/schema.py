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
from photogal.database import db
from photogal.model import Gallery as GalleryModel, Image as ImageModel


class Gallery(SQLAlchemyObjectType):
    class Meta:
        model = GalleryModel
        interfaces = (relay.Node,)


class Image(SQLAlchemyObjectType):
    class Meta:
        model = ImageModel
        interfaces = (relay.Node,)


class CreateGallery(graphene.Mutation):
    class Arguments:
        created = graphene.DateTime(required=False)
        last_modified = graphene.DateTime(required=False)
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        order_index = graphene.Int(required=False)
        public = graphene.Boolean(required=False)
        gallery_image_id = graphene.Int(required=False)

    ok = graphene.Boolean()
    gallery = graphene.Field(lambda: Gallery)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def mutate(self, info,
               created=None,
               last_modified=None,
               name=None,
               description=None,
               order_index=None,
               public=None,
               gallery_image_id=None):
        gallery = GalleryModel(
            created=created,
            last_modified=last_modified,
            name=name,
            description=description,
            order_index=order_index,
            public=public,
            gallery_image_id=gallery_image_id
        )
        db.session.add(gallery)
        db.session.commit()
        return CreateGallery(gallery=gallery)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    gallery = graphene.Field(Gallery, id=graphene.Int())
    image = graphene.Field(Image, id=graphene.Int())
    galleries = SQLAlchemyConnectionField(Gallery)
    images = SQLAlchemyConnectionField(Image)

    # noinspection PyMethodMayBeStatic,PyShadowingBuiltins,PyUnusedLocal
    def resolve_gallery(self, info, id=None):
        return GalleryModel.query.filter(GalleryModel.id == id).first()

    # noinspection PyMethodMayBeStatic,PyShadowingBuiltins,PyUnusedLocal
    def resolve_image(self, info, id=None):
        return ImageModel.query.filter(ImageModel.id == id).first()


class Mutations(graphene.ObjectType):
    create_gallery = CreateGallery.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
