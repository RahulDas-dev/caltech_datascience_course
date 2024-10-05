from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class LernerInfo(Base):
    __tablename__ = "lerner_info"

    id: Mapped[int] = mapped_column(primary_key=True)

    enrolments: Mapped[List[Tuple[int, int]]] = mapped_column(type_=JSON, default=list([]), nullable=False)

    created_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())
