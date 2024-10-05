import logging
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import insert, update
from sqlalchemy.orm import Session

from backend.db.orm import InstructorInfo

logger = logging.getLogger(__name__)


def insert_instructorinfo(db: Session, obj_in: Dict[str, str]) -> Optional[InstructorInfo]:
    query_stmt = insert(InstructorInfo).values(**obj_in).returning(InstructorInfo)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while adding InstructorInfo, Error - {e}")
        data = None
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully inserted InstructorInfo")
    finally:
        return data


def update_instructorinfo(db: Session, user_id: int, obj_in: Dict[str, Any]) -> Optional[InstructorInfo]:
    obj_in["updated_at"] = datetime.now()
    update_stmt = update(InstructorInfo).values(**obj_in).where(InstructorInfo.id == user_id).returning(InstructorInfo)
    status, data = None, None
    try:
        # status = db.execute(ModelDetails.i)
        status = db.execute(update_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while InstructorInfo, Error - {e}")
        data = None
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully Updateed InstructorInfo")
    finally:
        return data
