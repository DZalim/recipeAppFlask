from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from db import db


class TimestampMixinModel(db.Model):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
