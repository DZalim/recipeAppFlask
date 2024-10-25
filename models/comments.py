from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models import TimestampMixinModel


class CommentModel(TimestampMixinModel):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    description: Mapped[str] = mapped_column(
        db.String(255),
    )

    recipe_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipe: Mapped['RecipeModel'] = relationship(back_populates='comments')

    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user: Mapped['UserModel'] = relationship(back_populates='comments')
