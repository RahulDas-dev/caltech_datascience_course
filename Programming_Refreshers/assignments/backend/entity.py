import logging
from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy.orm import Session

from backend.db.curd.course import get_all_course_by_instructor, get_all_course_info, insert_courseinfo, update_course
from backend.db.curd.enrollment import (
    get_enrollment_by_user,
    get_enrollment_by_user_ins_course,
    insert_enrollmentinfo,
    update_enrollment_by_id,
)
from backend.db.curd.user import get_user_info_by_email, insert_userinfo, update_userinfo
from backend.types import UserType

logger = logging.getLogger(__name__)


@dataclass(init=True, frozen=True, slots=True)
class User:
    id: int
    name: str
    email_id: str
    password: str
    user_type: UserType = UserType.ADMIN

    @classmethod
    def create_entity(
        cls, session: Session, user_type: UserType, name: str, email_id: str, password: str
    ) -> Optional["User"]:
        obj_in = {
            "user_type": user_type,
            "name": name,
            "email_id": email_id,
            "password": password,
        }
        user_info = insert_userinfo(session, obj_in)
        if user_info is None:
            return None
        return cls(
            id=user_info.id,
            name=user_info.name,
            email_id=user_info.email_id,
            password=user_info.password,
            user_type=user_info.user_type,
        )

    @classmethod
    def validate_credential(cls, session: Session, email_id: str, password: str) -> Optional["User"]:
        user_info = get_user_info_by_email(session, email_id)
        if user_info is None:
            return None
        if user_info.password != password:
            return None
        if user_info.user_type == UserType.LERNER:
            return Lerner(
                id=user_info.id,
                name=user_info.name,
                email_id=user_info.email_id,
                password=user_info.password,
                user_type=user_info.user_type,
            )
        elif user_info.user_type == UserType.INSTRUCTOR:
            return Instructor(
                id=user_info.id,
                name=user_info.name,
                email_id=user_info.email_id,
                password=user_info.password,
                user_type=user_info.user_type,
            )
        return cls(
            id=user_info.id,
            name=user_info.name,
            email_id=user_info.email_id,
            password=user_info.password,
            user_type=user_info.user_type,
        )

    def update_password(self, session: Session, password: str) -> Optional["User"]:
        obj_in = {
            "password": password,
        }
        user_info = update_userinfo(session, user_id=self.id, obj_in=obj_in)
        if user_info is None:
            return None
        return User(
            id=user_info.id,
            name=user_info.name,
            email_id=user_info.email_id,
            password=user_info.password,
            user_type=user_info.user_type,
        )


@dataclass(init=True, frozen=True, slots=True)
class Lerner(User):
    @classmethod
    def create_entity(cls, session: Session, name: str, email_id: str, password: str):
        user = User.create_entity(session, user_type=UserType.LERNER, name=name, email_id=email_id, password=password)
        if user is None:
            logger.info("user_info is not Created")
            return None
        return cls(
            id=user.id,
            name=user.name,
            email_id=user.email_id,
            password=user.password,
            user_type=user.user_type,
        )

    def update_password(self, session: Session, password: str):
        user_info = super(Lerner, self).update_password(session, password)
        if user_info is None:
            logger.info("lerner_info not Created")
            return None
        return Lerner(
            id=user_info.id,
            name=user_info.name,
            email_id=user_info.email_id,
            password=user_info.password,
            user_type=user_info.user_type,
        )


@dataclass(init=True, frozen=True, slots=True)
class Instructor(User):
    @classmethod
    def create_entity(cls, session: Session, name: str, email_id: str, password: str):
        user = User.create_entity(
            session, user_type=UserType.INSTRUCTOR, name=name, email_id=email_id, password=password
        )
        if user is None:
            logger.info("user_info is not Created")
            return None
        return cls(
            id=user.id,
            name=user.name,
            email_id=user.email_id,
            password=user.password,
            user_type=user.user_type,
        )

    def update_password(self, session: Session, password: str):
        user_info = super(Instructor, self).update_password(session, password)
        if user_info is None:
            logger.info("lerner_info not Created")
            return None
        return Instructor(
            id=user_info.id,
            name=user_info.name,
            email_id=user_info.email_id,
            password=user_info.password,
            user_type=user_info.user_type,
        )


@dataclass(init=True, frozen=True, slots=True)
class Courses:
    id: Optional[int]
    name: str
    created_by: int
    active: bool = True

    @classmethod
    def get_all_courses(cls, session: Session) -> List["Courses"]:
        all_course_info = get_all_course_info(session)
        ret_list = []
        for item in all_course_info:
            new_item = cls(id=item.id, name=item.name, created_by=item.created_by, active=item.active)
            ret_list.append(new_item)
        return ret_list

    @classmethod
    def get_course_by_instrucitor_id(cls, session: Session, instructor_id: int) -> List["Courses"]:
        all_course_info = get_all_course_by_instructor(session, instructor_id)
        ret_list = []
        for item in all_course_info:
            new_item = cls(id=item.id, name=item.name, created_by=item.created_by, active=item.active)
            ret_list.append(new_item)
        return ret_list

    @classmethod
    def create_course(cls, session: Session, course_tile: str, user_info: Instructor) -> Optional["Courses"]:
        course = insert_courseinfo(db=session, obj_in={"name": course_tile, "created_by": user_info.id})
        if course is None:
            logger.info("course not Created")
            return None
        return cls(id=course.id, name=course.name, created_by=course.created_by, active=course.active)

    @classmethod
    def remove_course(cls, session: Session, course_id: int, user_info: Instructor) -> Optional["Courses"]:
        course = update_course(session, course_id, {"active": False})
        if course is None:
            logger.info("course not Removed")
            return None
        return cls(id=course.id, name=course.name, created_by=course.created_by, active=course.active)


@dataclass(init=True, frozen=True, slots=True)
class Enrollment:
    user_id: int
    course_id: int
    instructor_id: int
    active: Optional[bool] = True
    id: Optional[int] = None

    @classmethod
    def get_enrollment_by_ids(
        cls, session: Session, user_id: int, course_id: int, instructor_id: int
    ) -> Optional["Enrollment"]:
        enrollment = get_enrollment_by_user_ins_course(session, user_id, course_id, instructor_id)
        if enrollment is None:
            return None
        return cls(
            id=enrollment.id,
            user_id=enrollment.user_id,
            course_id=enrollment.course_id,
            instructor_id=enrollment.instructor_id,
            active=enrollment.active,
        )

    @classmethod
    def get_enrollment_by_user_id(cls, session: Session, user_id: int) -> List["Enrollment"]:
        enrollments = get_enrollment_by_user(session, user_id)
        if not enrollments:
            return []
        retlist = []
        for item in enrollments:
            retlist.append(
                cls(id=item.id, user_id=item.user_id, course_id=item.course_id, instructor_id=item.instructor_id)
            )
        return retlist

    def make_enrollment(self, session: Session) -> bool:
        insert_dict = {
            "user_id": self.user_id,
            "course_id": self.course_id,
            "instructor_id": self.instructor_id,
            "active": self.active,
        }
        en_info = insert_enrollmentinfo(session, insert_dict)
        return False if en_info is None else True

    @classmethod
    def remove_user_enrollement(cls, session: Session, enrollment_id: int) -> bool:
        enrollment_info = update_enrollment_by_id(session, enrollment_id, {"active": False})
        return False if enrollment_info is None else True
        return False if enrollment_info is None else True
        return False if enrollment_info is None else True
        return False if enrollment_info is None else True
        return False if enrollment_info is None else True
        return False if enrollment_info is None else True
        return False if enrollment_info is None else True
        return False if enrollment_info is None else True
