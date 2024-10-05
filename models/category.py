from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models.mixins import TimestampMixinModel


class CategoryModel(TimestampMixinModel):

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    category_name: Mapped[str] = mapped_column(
        db.String(255),
        nullable=False,
        unique=True
    )

    recipes: Mapped[list["RecipeModel"]] = relationship(
        back_populates='category',
        cascade="all, delete-orphan"
    )