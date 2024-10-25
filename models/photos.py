from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models import TimestampMixinModel


class PhotoModel(TimestampMixinModel):
    __abstract__ = True

    photo_url: Mapped[str] = mapped_column(
        db.String(),
        nullable=False
    )


class UsersPhotoModel(PhotoModel):
    __tablename__ = "users_photo"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False,
                                         unique=True)  # unique = True => One to one relation
    user: Mapped['UserModel'] = relationship(back_populates='photo')


class RecipePhotosModel(PhotoModel):
    __tablename__ = "recipe_photos"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    recipe_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipe: Mapped['RecipeModel'] = relationship(back_populates='photos')
