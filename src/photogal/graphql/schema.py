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
from flask import request
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql_relay import from_global_id
from photogal.database import db
from photogal.database.model import Gallery as GalleryModel, Image as ImageModel

from photogal.image import save_image_file, validate_image_file


# noinspection PyShadowingBuiltins
def resolve_gallery_id(id: int = None, gallery_id: str = None) -> int:
    if gallery_id is None:
        if id is None:
            raise ValueError("Either id or gallery_id must be specified")
        type, gallery_id = from_global_id(id)
        if type != "Gallery":
            raise ValueError(f"Wrong id type (expected 'Gallery', got '{type}'")
    return gallery_id


def fetch_gallery(gallery_id: int) -> GalleryModel:
    return GalleryModel.query.get(gallery_id)


# noinspection PyShadowingBuiltins
def resolve_image_id(id: int = None, image_id: str = None) -> int:
    if image_id is None:
        if id is None:
            raise ValueError("Either id or image_id must be specified")
        type, image_id = from_global_id(id)
        if type != "Image":
            raise ValueError(f"Wrong id type (expected 'Image', got '{type}'")
    return image_id


def fetch_image(image_id: int) -> ImageModel:
    return ImageModel.query.get(image_id)


def get_image_file():
    image_files = request.files.getlist("image")
    image_count = len(image_files)
    if image_count == 0:
        return None
    elif image_count != 1:
        raise ValueError(f"Expected one image file, got {image_count}")
    image_file = image_files[0]
    return image_file


class Gallery(SQLAlchemyObjectType):
    class Meta:
        model = GalleryModel
        interfaces = (relay.Node,)

    gallery_id = graphene.Int()

    # noinspection PyUnusedLocal
    def resolve_gallery_id(self, info):
        # noinspection PyUnresolvedReferences
        return self.id


class Image(SQLAlchemyObjectType):
    class Meta:
        model = ImageModel
        interfaces = (relay.Node,)

    image_id = graphene.Int()
    keywords = graphene.List(graphene.String)

    # noinspection PyUnusedLocal
    def resolve_image_id(self, info):
        # noinspection PyUnresolvedReferences
        return self.id

    # noinspection PyUnusedLocal
    def resolve_keywords(self, info):
        # noinspection PyTypeChecker
        return [keyword.keyword for keyword in self.keywords]


class CreateGallery(graphene.Mutation):
    class Arguments:
        created = graphene.DateTime(description="The time at which the gallery was created.", required=False)
        last_modified = graphene.DateTime(description="The time at which the gallery was last modified.",
                                          required=False)
        name = graphene.String(description="The name of the gallery.", required=False)
        description = graphene.String(description="The description of the gallery.", required=False)
        position = graphene.Int(description="The ordering position.", required=False)
        public = graphene.Boolean(
            description="The public flag. Non-public galleries are not visible to unauthenticated users.",
            required=False)
        gallery_image_id = graphene.Int(description="The id of the gallery image.", required=False)

    gallery = graphene.Field(Gallery)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def mutate(self, info,
               created=None,
               last_modified=None,
               name=None,
               description=None,
               position=None,
               public=None,
               gallery_image_id=None):
        gallery = GalleryModel(
            created=created,
            last_modified=last_modified,
            name=name,
            description=description,
            position=position,
            public=public,
            gallery_image_id=gallery_image_id
        )
        db.session.add(gallery)
        db.session.commit()
        return CreateGallery(gallery=gallery)


class DeleteGallery(graphene.Mutation):
    class Arguments:
        id = graphene.ID(description="The id.")
        gallery_id = graphene.Int(description="The gallery id.")

    gallery = graphene.Field(Gallery)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal,PyShadowingBuiltins
    def mutate(self, info, id=None, gallery_id=None):
        resolved_id = resolve_gallery_id(id, gallery_id)
        gallery = fetch_gallery(resolved_id)
        if gallery:
            db.session.delete(gallery)
            db.session.commit()
        return DeleteGallery(gallery=gallery)


class CreateImage(graphene.Mutation):
    class Arguments:
        created = graphene.DateTime(description="The time at which the image was created.", required=False)
        last_modified = graphene.DateTime(description="The time at which the image was last modified.",
                                          required=False)
        name = graphene.String(description="The name of the image.", required=False)
        description = graphene.String(description="The description of the image.", required=False)
        creation_date = graphene.String(description="The time at which the image was taken.", required=False)
        keywords = graphene.List(graphene.String, description="The keywords.", required=False)

    image = graphene.Field(Image)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def mutate(self, info,
               created=None,
               last_modified=None,
               name=None,
               description=None,
               creation_date=None,
               keywords=None):
        def create_image():
            # noinspection PyShadowingNames
            image = ImageModel(
                created=created,
                last_modified=last_modified,
                name=name,
                description=description
            )
            image.set_creation_date(creation_date)
            image.set_keywords(*([] if keywords is None else keywords))
            return image

        image = create_image()
        image_file = get_image_file()
        if image_file:
            image.filename = image_file.filename
            file = save_image_file(image_file)
            validate_image_file(file)
            # TODO: if not valid, delete file
        db.session.add(image)
        db.session.commit()
        # TODO: rename image file :-P
        return CreateImage(image=image)


class DeleteImage(graphene.Mutation):
    class Arguments:
        id = graphene.ID(description="The id.")
        image_id = graphene.Int(description="The image id.")

    image = graphene.Field(Image)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal,PyShadowingBuiltins
    def mutate(self, info, id=None, image_id=None):
        resolved_id = resolve_image_id(id, image_id)
        image = fetch_image(resolved_id)
        if image:
            db.session.delete(image)
            db.session.commit()
        return DeleteImage(image=image)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    gallery = graphene.Field(Gallery, id=graphene.ID(), gallery_id=graphene.Int(), description="Fetches a gallery.")
    image = graphene.Field(Image, id=graphene.ID(), image_id=graphene.Int(), description="Fetches an image.")
    galleries = SQLAlchemyConnectionField(Gallery, description="A Gallery connection.")
    images = SQLAlchemyConnectionField(Image, description="An Image connection.")

    # noinspection PyMethodMayBeStatic,PyUnusedLocal,PyShadowingBuiltins
    def resolve_gallery(self, info, id=None, gallery_id=None):
        resolved_id = resolve_gallery_id(id, gallery_id)
        return fetch_gallery(resolved_id)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal,PyShadowingBuiltins
    def resolve_image(self, info, id=None, image_id=None):
        resolved_id = resolve_image_id(id, image_id)
        return fetch_image(resolved_id)


class Mutations(graphene.ObjectType):
    create_gallery = CreateGallery.Field(description="Creates a new gallery.")
    delete_gallery = DeleteGallery.Field(description="Deletes the specified gallery.")

    create_image = CreateImage.Field(description="Creates a new image.")
    delete_image = DeleteImage.Field(description="Deletes the specified image.")


schema = graphene.Schema(query=Query, mutation=Mutations)
