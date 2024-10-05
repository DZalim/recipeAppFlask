from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db import db
from models.enums import UserRoles


class UserModel(db.Model):
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
        db.String(20)
    )
    role: Mapped[UserRoles] = mapped_column(
        db.Enum(UserRoles),
        server_default=UserRoles.beginner.name,
        default=UserRoles.beginner.name,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime,
        server_default=func.now(),
        default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime,
        server_default=func.now(),
        default=func.now(),
        onupdate=func.now()
    )

