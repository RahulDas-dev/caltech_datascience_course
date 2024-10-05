import logging
from datetime import datetime
from typing import Any, Dict, Optional, Sequence

from sqlalchemy import and_, insert, select, update
from sqlalchemy.orm import Session

from backend.db.orm import EnrollmentInfo

logger = logging.getLogger(__name__)


def insert_enrollmentinfo(db: Session, obj_in: Dict[str, str]) -> Optional[EnrollmentInfo]:
    query_stmt = insert(EnrollmentInfo).values(**obj_in).returning(EnrollmentInfo)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while adding EnrollmentInfo, Error - {e}")
        data = None
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully inserted EnrollmentInfo")
    finally:
        return data


def get_enrollment_by_user_ins_course(
    db: Session, user_id: int, instructor_id: int, course_id: int
) -> Optional[EnrollmentInfo]:
    query_stmt = select(EnrollmentInfo).where(
        and_(
            EnrollmentInfo.user_id == user_id,
            EnrollmentInfo.instructor_id == instructor_id,
            EnrollmentInfo.course_id == course_id,
        )
    )
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while adding EnrollmentInfo, Error - {e}")
        data = None
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully inserted EnrollmentInfo")
    finally:
        return data


def get_enrollment_by_user(db: Session, user_id: int) -> Sequence[EnrollmentInfo]:
    query_stmt = select(EnrollmentInfo).where(EnrollmentInfo.user_id == user_id)
    status, data = None, []
    try:
        status = db.execute(query_stmt)
        data = status.scalars().all()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while adding EnrollmentInfo, Error - {e}")
        data = []
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully inserted EnrollmentInfo")
    finally:
        return data


def update_enrollment_by_id(db: Session, enrollment_id: int, update_dict: Dict[str, Any]) -> Optional[EnrollmentInfo]:
    update_dict["updated_at"] = datetime.now()
    query_stmt = (
        update(EnrollmentInfo).values(**update_dict).where(EnrollmentInfo.id == enrollment_id).returning(EnrollmentInfo)
    )
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while adding EnrollmentInfo, Error - {e}")
        data = None
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully inserted EnrollmentInfo")
    finally:
        return data
