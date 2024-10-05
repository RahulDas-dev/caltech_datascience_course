from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class EnrollmentInfo(Base):
    __tablename__ = "enrollment_info"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    course_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    instructor_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean(), default=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "course_id", "instructor_id", name="Enrollment_info_user_id_course_id_uc"),
    )
