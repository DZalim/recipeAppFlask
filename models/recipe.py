from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models.enums import RecipeDifficultyLevel
from models.mixins import TimestampMixinModel


class RecipeModel(TimestampMixinModel):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    recipe_name: Mapped[str] = mapped_column(
        db.String(255),
        nullable=False,
        unique=True
    )

    recipe_photo_url: Mapped[str] = mapped_column(
        db.String(255),
        default="No photo",
    )

    difficulty_level: Mapped[RecipeDifficultyLevel] = mapped_column(
        db.Enum(RecipeDifficultyLevel),
        server_default=RecipeDifficultyLevel.easy.name,
        default=RecipeDifficultyLevel.easy.name,
        nullable=False
    )
    portions: Mapped[int] = mapped_column(
        db.Integer,
        nullable=False
    )
    preparing_time_in_minutes: Mapped[int] = mapped_column(
        db.Integer,
        nullable=False
    )
    cooking_time_in_minutes: Mapped[int] = mapped_column(
        db.Integer,
        nullable=False
    )
    ingredients: Mapped[str] = mapped_column(
        db.Text,
        nullable=False,
    )  # must be entered with a comma and a space for frontend
    description: Mapped[str] = mapped_column(
        db.Text,
        nullable=False,
    )

    category_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category: Mapped['CategoryModel'] = relationship(back_populates='recipes')

    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner: Mapped['UserModel'] = relationship(back_populates='recipes')

    comments: Mapped[list["CommentModel"]] = relationship(
        back_populates='recipe',
        cascade="all, delete-orphan"
    )
