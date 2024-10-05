from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class CourseInfo(Base):
    __tablename__ = "course_info"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(), nullable=False)

    created_by: Mapped[int] = mapped_column(Integer(), nullable=False)

    active: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())

    __table_args__ = (UniqueConstraint("name", name="course_info_name_uc"),)
