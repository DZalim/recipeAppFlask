from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models import ProfileStatus
from models.enums import UserRoles
from models.mixins import TimestampMixinModel


class UserModel(TimestampMixinModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    email: Mapped[str] = mapped_column(
        db.String(50),
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(
        db.String(255),
        nullable=False
    )
    username: Mapped[str] = mapped_column(
        db.String(30),
        nullable=False,
        unique=True
    )
    first_name: Mapped[str] = mapped_column(
        db.String(30),
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        db.String(30),
        nullable=False
    )
    phone: Mapped[str] = mapped_column(
        db.String(20),
        default='0000000000',
        server_default='000000000'
    )
    role: Mapped[UserRoles] = mapped_column(
        db.Enum(UserRoles),
        server_default=UserRoles.beginner.name,
        default=UserRoles.beginner.name,
        nullable=False
    )

    profile_status: Mapped[ProfileStatus] = mapped_column(
        db.Enum(ProfileStatus),
        server_default=ProfileStatus.active.name,
        default=ProfileStatus.active.name,
    )

    recipes: Mapped[list["RecipeModel"]] = relationship(
        back_populates='owner',
        cascade="all, delete-orphan"
    )

    comments: Mapped[list["CommentModel"]] = relationship(
        back_populates='user',
        cascade="all, delete-orphan"
    )
