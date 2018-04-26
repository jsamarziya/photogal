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
        exclude_fields = ['gallery_id']

    gallery_id = graphene.Int()

    # noinspection PyUnusedLocal
    def resolve_gallery_id(self, info):
        return self.gallery_id


class Image(SQLAlchemyObjectType):
    class Meta:
        model = ImageModel
        interfaces = (relay.Node,)
        exclude_fields = ['gallery_id']

    image_id = graphene.Int()

    # noinspection PyUnusedLocal
    def resolve_image_id(self, info):
        return self.image_id

class CreateGallery(graphene.Mutation):
    class Arguments:
        created = graphene.DateTime(description="The time at which the gallery was created.", required=False)
        last_modified = graphene.DateTime(description="The time at which the gallery was last modified.",
                                          required=False)
        name = graphene.String(description="The name of the gallery.", required=False)
        description = graphene.String(description="The description of the gallery.", required=False)
        order_index = graphene.Int(description="The ordering index.", required=False)
        public = graphene.Boolean(
            description="The public flag. Non-public galleries are not visible to unauthenticated users.",
            required=False)
        gallery_image_id = graphene.Int(description="The id of the gallery image.", required=False)

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


class DeleteGallery(graphene.Mutation):
    class Arguments:
        gallery_id = graphene.Int(required=True)

    gallery = graphene.Field(lambda: Gallery)
    ok = graphene.Boolean(description="True if the gallery was deleted, False otherwise.")

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def mutate(self, info, gallery_id):
        gallery = GalleryModel.query.get(gallery_id)
        if gallery:
            db.session.delete(gallery)
            db.session.commit()
            ok = True
        else:
            ok = False
        return DeleteGallery(gallery=gallery, ok=ok)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    gallery = graphene.Field(Gallery, gallery_id=graphene.Int())
    image = graphene.Field(Image, image_id=graphene.Int())
    galleries = SQLAlchemyConnectionField(Gallery)
    images = SQLAlchemyConnectionField(Image)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def resolve_gallery(self, info, gallery_id=None):
        return GalleryModel.query.get(gallery_id)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def resolve_image(self, info, image_id=None):
        return ImageModel.query.get(image_id)


class Mutations(graphene.ObjectType):
    create_gallery = CreateGallery.Field(description="Creates a new gallery.")
    delete_gallery = DeleteGallery.Field(description="Deletes the specified gallery.")


schema = graphene.Schema(query=Query, mutation=Mutations)
