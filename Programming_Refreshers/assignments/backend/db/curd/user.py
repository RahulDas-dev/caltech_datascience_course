import logging
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from backend.db.orm import UserInfo

logger = logging.getLogger(__name__)


def get_user_info_by_email(db: Session, email_id: str) -> Optional[UserInfo]:
    query_stmt = select(UserInfo).where(UserInfo.email_id == email_id)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while fetching UserInfo, for id: {email_id}, Error - {e}")
        data = None
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully fetched UserInfo, for id: {email_id}")
    finally:
        return data


def create_admin_entry(db: Session) -> Optional[UserInfo]:
    obj_in = {
        "user_type": "ADMIN",
        "name": "ADMIN",
        "email_id": "admin@sltech.com",
        "password": "password",
    }
    query_stmt = insert(UserInfo).values(**obj_in).returning(UserInfo)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while adding UserInfo, Error - {e}")
        data = None
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully inserted UserInfo for Admin")
    finally:
        return data


def insert_userinfo(db: Session, obj_in: Dict[str, Any]) -> Optional[UserInfo]:
    query_stmt = insert(UserInfo).values(**obj_in).returning(UserInfo)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while adding UserInfo, Error - {e}")
        data = None
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully inserted UserInfo")
    finally:
        return data


def update_userinfo(db: Session, user_id: int, obj_in: Dict[str, Any]) -> Optional[UserInfo]:
    obj_in["updated_at"] = datetime.now()
    update_stmt = update(UserInfo).values(**obj_in).where(UserInfo.id == user_id).returning(UserInfo)
    status, data = None, None
    try:
        # status = db.execute(ModelDetails.i)
        status = db.execute(update_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.debug(f"Session id {id(db)} | Error while bulk Update on Model details, Error - {e}")
        data = None
    else:
        logger.debug(f"Session id {id(db)} | Sucessfully Updateed Model deatails ")
    finally:
        return data
