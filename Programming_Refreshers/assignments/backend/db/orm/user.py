from datetime import datetime
from typing import Optional

from sqlalchemy import Enum, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from backend.types import UserType

from ..base import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType), nullable=False)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    email_id: Mapped[str] = mapped_column(String(), nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)

    created_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())

    __table_args__ = (UniqueConstraint("email_id", name="user_info_email_id_uc"),)
