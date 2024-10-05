import logging
from datetime import datetime
from typing import Any, Dict, Optional, Sequence

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from backend.db.orm import CourseInfo

logger = logging.getLogger(__name__)


def insert_courseinfo(db: Session, obj_in: Dict[str, str | int | bool]) -> Optional[CourseInfo]:
    obj_in_ = obj_in.copy()
    obj_in_["active"] = True
    query_stmt = insert(CourseInfo).values(**obj_in_).returning(CourseInfo)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while adding CourseInfo, Error - {e}")
        data = None
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully inserted CourseInfo")
    finally:
        return data


def get_all_course_info(db: Session) -> Sequence[CourseInfo]:
    query_stmt = select(CourseInfo)
    status, data = None, []
    try:
        status = db.execute(query_stmt)
        data = status.scalars().all()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while fetching CourseInfo, Error - {e}")
        data = []
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully fetched CourseInfo")
    finally:
        return data


def get_all_course_by_instructor(db: Session, instructor_id: int) -> Sequence[CourseInfo]:
    query_stmt = select(CourseInfo).where(CourseInfo.created_by == instructor_id)
    status, data = None, []
    try:
        status = db.execute(query_stmt)
        data = status.scalars().all()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while fetching CourseInfo, Error - {e}")
        data = []
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully fetched CourseInfo")
    finally:
        return data


def update_course(db: Session, course_id: int, update_dict: Dict[str, Any]) -> Optional[CourseInfo]:
    update_dict["updated_at"] = datetime.now()
    query_stmt = update(CourseInfo).values(**update_dict).where(CourseInfo.id == course_id).returning(CourseInfo)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while Updateing CourseInfo, Error - {e}")
        data = None
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully Updated CourseInfo")
    finally:
        return data
