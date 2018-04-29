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

from assertpy import assert_that
from photogal.model import Image, GalleryImage
from photogal.model.gallery import Gallery


def test_gallery_images(db):
    gallery = Gallery(name="myGallery")
    image1 = Image(name="image1")
    image2 = Image(name="image2")
    image3 = Image(name="image3")
    gallery.images.append(GalleryImage(image=image3, position=2))
    gallery.images.append(GalleryImage(image=image2, position=1))
    gallery.images.append(GalleryImage(image=image1, position=0))
    db.session.add(gallery)
    db.session.commit()
    assert_that([i.image for i in gallery.images]).contains_sequence(image1, image2, image3)

    gallery.images[1].position = 2
    gallery.images[2].position = 1
    db.session.commit()
    assert_that([i.image for i in gallery.images]).contains_sequence(image1, image3, image2)

    db.session.delete(gallery)
    db.session.commit()
    assert_that(db.session.query(Image).count()).is_equal_to(3)


def test_image_galleries(db):
    image = Image(name="myImage")
    gallery1 = Gallery(name="gallery1")
    gallery1.images.append(GalleryImage(image=image, position=0))
    db.session.add(gallery1)
    db.session.commit()
    assert_that([i.gallery for i in image.galleries]).contains_only(gallery1)

    gallery2 = Gallery(name="gallery2")
    gallery2.images.append(GalleryImage(image=image, position=0))
    db.session.add(gallery2)
    db.session.commit()
    assert_that([i.gallery for i in image.galleries]).contains_only(gallery1, gallery2)

    gallery1.images.remove(gallery1.images[0])
    db.session.commit()
    assert_that([i.gallery for i in image.galleries]).contains_only(gallery2)
    assert_that(gallery1.images).is_empty()
    assert_that([i.image for i in gallery2.images]).contains_only(image)

    db.session.delete(image)
    db.session.commit()
    assert_that(db.session.query(Gallery).count()).is_equal_to(2)
    assert_that(gallery2.images).is_empty()
