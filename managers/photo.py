import os

import uuid

from constant import RECIPE_PHOTOS, USER_PHOTOS
from db import db
from helpers.helpers import decode_photo
from models import RecipePhotosModel, UsersPhotoModel
from services.cloudinary import CloudinaryService

cloudinary = CloudinaryService()


class PhotoManager:
    PHOTO_INFO = {
        "recipe": {
            "path": RECIPE_PHOTOS,
            "model": RecipePhotosModel,
            "id_key": "recipe_id"
        },
        "user": {
            "path": USER_PHOTOS,
            "model": UsersPhotoModel,
            "id_key": "user_id"
        }
    }

    def create_photo_url(self, encoded_photo, extension, photo_type):
        file_name = uuid.uuid4()
        path = os.path.join(self.PHOTO_INFO[photo_type]["path"], f"{file_name}.{extension}")
        decode_photo(path, encoded_photo)
        photo_url = cloudinary.upload_photo(path, extension)

        if os.path.exists(path):
            os.remove(path)

        return photo_url

    def create_photo(self, photo_url, related_id, photo_type):
        photo_model_class = self.PHOTO_INFO[photo_type]["model"]
        id_key = self.PHOTO_INFO[photo_type]["id_key"]

        photo = photo_model_class(**{id_key: related_id, "photo_url": photo_url})

        db.session.add(photo)
        db.session.flush()

        return photo

    def get_photo(self, related_id, photo_type):
        photo_model_class = self.PHOTO_INFO[photo_type]["model"]
        id_key = self.PHOTO_INFO[photo_type]["id_key"]

        photo = (db.session.execute(db.select(photo_model_class)
                                    .filter_by(**{id_key: related_id})).scalars())

        return photo

    @staticmethod
    def get_photo_by_id(photo_id, recipe_id):
        photo = db.session.execute(
            db.select(RecipePhotosModel)
            .where(
                RecipePhotosModel.id == photo_id,
                RecipePhotosModel.recipe_id == recipe_id
            )
        ).scalars().first()

        return photo

    @staticmethod
    def delete_photo(related_id, photo_type, photo_id=None):
        if photo_type == "user":
            photo = PhotoManager().get_photo(related_id, photo_type).first()
        else:
            photo = PhotoManager.get_photo_by_id(photo_id, related_id)

        if not photo:
            return "No photo to delete"

        db.session.delete(photo)
        db.session.flush()
        cloudinary.delete_photo(photo.photo_url)

        return "The photo has been deleted"
