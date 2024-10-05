import logging
import sys
from typing import NoReturn, Optional, Union

from pwinput import pwinput
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from termcolor import colored

from backend.entity import Courses, Enrollment, Instructor, Lerner, User
from backend.settings import settings

logger = logging.getLogger(__name__)


class Application:
    _user_info: Union[User, Lerner, Instructor]

    def __init__(self):
        self._setup_db()

    def _setup_db(self):
        _db_url = URL.create(drivername="sqlite", database=settings.db_name)
        logger.debug(f"DB URL - ${_db_url}")
        self._engine = create_engine(_db_url, echo=False)
        self._session = sessionmaker(self._engine, expire_on_commit=False, autoflush=True)

    def run(self):
        self._print_welcome_msg()
        self._user_sign_in()
        opt = self._perse_signin_options()
        if opt in [1, 2]:
            self._user_info = self._new_sign_in(opt)
        else:
            self._user_info = self._except_credential()
        print(colored(f"\n Hi, {self._user_info.name} Kindly Choose a Valid Options\n", "light_green"))
        while True:
            self._print_input_options()
            chosen_option = self._perse_input()
            self._reolve_task(chosen_option)

    def _print_welcome_msg(self):
        starts = "*" * 20
        print(colored(f"{starts}{starts}{starts}{starts}\n", "cyan"))
        print(colored(f"{starts}  Welcome to the EdTech Backend System  {starts}\n", "cyan"))
        print(colored(f"{starts}{starts}{starts}{starts}\n", "cyan"))

    def _user_sign_in(self):
        indent = " +-->"
        print(colored(f"{indent} Press for 1 for New Lerner Signin", "green"))
        print(colored(f"{indent} Press for 2 for New Instructor Signin", "green"))
        print(colored(f"{indent} Press for 3 for Existing Lerner/Instructor Login", "green"))

    def _perse_signin_options(self) -> int:
        indent = " == "
        chosen_option = None
        while True:
            opt = input(colored(f"\n{indent} Choose a Valid Options : ", "blue"))
            print()
            opt = opt.strip().strip("\n")
            try:
                opt = int(opt)
            except ValueError:
                print(colored("Choosen Option is not Valid", "red"))
                continue
            if opt not in [1, 2, 3]:
                print(colored("Valid Options are - 1, 2, 3\n", "red"))
                continue
            chosen_option = opt
            break
        return chosen_option

    def _new_sign_in(self, opt: int) -> Union[Lerner, Instructor]:
        user_info = None
        _session = self._session()
        while True:
            name = input(colored(" Name     : ", "light_blue"))
            email_id = input(colored(" email id : ", "light_blue"))
            password = pwinput(prompt=colored(" password : ", "light_blue"), mask="X")

            name = name.strip().strip("\n")
            email_id = email_id.strip().strip("\n")
            password = password.strip().strip("\n")
            if opt == 1:
                user_info = Lerner.create_entity(session=_session, name=name, email_id=email_id, password=password)
            else:
                user_info = Instructor.create_entity(session=_session, name=name, email_id=email_id, password=password)
            if user_info is not None:
                _session.commit()
                _session.close()
                break
        print(colored(f"\n Hi ,{user_info.name} , Registration is Sucessful\n", "blue"))
        return user_info

    def _except_credential(self) -> Union[User, Lerner, Instructor]:
        user_info = None
        _session = self._session()
        while True:
            email_id = input(colored(" email id : ", "light_blue"))
            password = pwinput(prompt=colored(" password : ", "light_blue"), mask="X")
            email_id = email_id.strip().strip("\n")
            password = password.strip().strip("\n")
            user_info = User.validate_credential(session=_session, email_id=email_id, password=password)
            if user_info is not None:
                _session.commit()
                _session.close()
                break
            else:
                print(colored("\n Email id or Password is not Valid\n", "red"))
                print(colored(" Kindly Try Again\n", "blue"))
        print(colored(f"\n Hi ,{user_info.name} login Sucessful\n", "blue"))
        return user_info

    def _print_input_options(self):
        if isinstance(self._user_info, Instructor):
            self._print_instructor_options()
        elif isinstance(self._user_info, Lerner):
            self._print_lerner_options()
        else:
            self._print_admin_options()

    def _print_lerner_options(self):
        indent = " +-->"
        print(colored(f"{indent} Press 5 for Email/Passwoed Update    ", "light_green"))
        print(colored(f"{indent} Press 9 to enroll in a Course        ", "light_green"))
        print(colored(f"{indent} Press 10 to remove enrollment        ", "light_green"))
        print(colored(f"{indent} Press 11 Display all enrollment      ", "light_green"))
        print(colored(f"{indent} Press 0 to exit the Application      ", "light_green"))

    def _print_instructor_options(self):
        indent = " +-->"
        print(colored(f"{indent} Press 5 for Update Password          ", "light_green"))
        print(colored(f"{indent} Press 6 to Create a New Course       ", "light_green"))
        print(colored(f"{indent} Press 7 to Remove a Existing Course  ", "light_green"))
        print(colored(f"{indent} Press 8 to Display all your Courses  ", "light_green"))
        print(colored(f"{indent} Press 0 to exit the Application      ", "light_green"))

    def _print_admin_options(self):
        indent = " +-->"
        print(colored(f"{indent} Press 12 for New Lerner Registration     ", "light_green"))
        print(colored(f"{indent} Press 13 for New Instructor Registration ", "light_green"))
        print(colored(f"{indent} Press 14 for New Course Creation         ", "light_green"))
        print(colored(f"{indent} Press 15 for New Enrollement Creation    ", "light_green"))
        print(colored(f"{indent} Press 0 to exit the Application         ", "light_green"))

    def _perse_input(self) -> int:
        indent = " == "
        chosen_option = None
        while True:
            opt = input(colored(f"\n{indent} Choose a Valid Options : ", "blue"))
            opt = opt.strip().strip("\n")
            try:
                opt = int(opt)
            except ValueError:
                print(colored("Choosen Option is not Valid", "red"))
                continue
            if isinstance(self._user_info, Instructor):
                if opt in [5, 6, 7, 8, 0]:
                    chosen_option = opt
                    break
                else:
                    print(colored("Choosen Option is not Valid\n", "red"))
                    print(colored("Valid Options are - 5, 6, 7, 8, 0\n", "red"))
            elif isinstance(self._user_info, Lerner):
                if opt in [5, 9, 10, 11, 0]:
                    chosen_option = opt
                    break
                else:
                    print(colored("Choosen Option is not Valid\n", "red"))
                    print(colored("Valid Options are - 5, 9, 10, 11, 0\n", "red"))
            else:
                if opt in [1, 2, 3, 4, 0]:
                    chosen_option = opt
                    break
                else:
                    print(colored("Choosen Option is not Valid\n", "red"))
                    print(colored("Valid Options are - 1, 2, 3, 4, 0\n", "red"))
        return chosen_option

    def _reolve_task(self, chosen_option: int) -> None:
        if chosen_option == 0:
            self._exit()
        elif chosen_option == 1:
            self._user_info = self._new_sign_in(1)
        elif chosen_option == 2:
            self._user_info = self._new_sign_in(2)
        elif chosen_option == 3:
            self._user_info = self._existing_log_in()
        elif chosen_option == 4:
            self._enroll_course_by_admin()
        elif chosen_option == 5:
            self._reset_password()
        elif chosen_option == 6:
            self._create_course()
        elif chosen_option == 7:
            self._remove_course()
        elif chosen_option == 8:
            self._display_couseses()
        elif chosen_option == 9:
            self._enroll_course_by_user()
        elif chosen_option == 10:
            self._remove_user_enrollement()
        elif chosen_option == 11:
            self._display_user_enrollement()
        elif chosen_option == 12:
            pass
        elif chosen_option == 13:
            pass
        elif chosen_option == 14:
            pass
        elif chosen_option == 15:
            pass
        else:
            pass

    def _exit(self, exit_code: Optional[int] = None) -> NoReturn:
        logger.info(colored("EdTech Backend System : Exiting ...", "blue"))
        self._engine.dispose()
        sys.exit(exit_code)

    def _reset_password(self) -> None:
        _session = self._session()
        print()
        while True:
            old_password = pwinput(prompt=colored(" Old Password : ", "light_blue"), mask="X")
            old_password = old_password.strip().strip("\n")
            if self._user_info.password != old_password:
                print(colored("\n Old Password is not matching\n", "red"))
                print(colored("\n Kindly Try Again\n", "blue"))
                continue
            new_password = pwinput(prompt=colored(" New Password : ", "light_blue"), mask="X")
            new_password = new_password.strip().strip("\n")
            if self._user_info.password == new_password:
                print(colored("\n New Password can not be same as old pasword\n", "red"))
                print(colored("\n Kindly Try Again\n", "blue"))
                continue
            break
        user_info = self._user_info.update_password(session=_session, password=new_password)
        if user_info is not None:
            _session.commit()
            _session.close()
            self._user_info = user_info
            print(colored("\n Password Update is Sucessful\n", "blue"))
        else:
            print(colored("\n Password Update is not Sucessful\n", "red"))

    def _create_course(self) -> None:
        _session = self._session()
        while True:
            course_title = input(colored("\n Enter Course Title : ", "light_blue"))
            course_title = course_title.strip().strip("\n")
            try:
                course_title = str(course_title)
            except ValueError:
                print(colored(" Course Title is not Valid\n", "red"))
                continue
            break
        if not isinstance(self._user_info, Instructor):
            return
        couses = Courses.create_course(_session, course_title, self._user_info)
        if couses is not None:
            _session.commit()
            _session.close()
            print(colored("\n Course Creation is Sucessful\n", "blue"))
        else:
            print(colored("\n Course Creation is not Sucessful\n", "red"))

    def _existing_log_in(self) -> User:
        user_info = None
        _session = self._session()
        while True:
            name = input(colored(" Name     : ", "light_blue"))
            email_id = input(colored(" email id : ", "light_blue"))
            password = pwinput(prompt=colored(" password : ", "light_blue"), mask="X")

            name = name.strip().strip("\n")
            email_id = email_id.strip().strip("\n")
            password = password.strip().strip("\n")
            user_info = User.validate_credential(_session, email_id, password)
            if user_info is None:
                print(colored("\nEmail id or Password is not Valid\n", "red"))
                continue
            _session.close()
            break
        print(colored(f"\n Hi ,{user_info.name} , Registration is Sucessful\n", "blue"))
        return user_info

    def _enroll_course_by_user(self):
        _session = self._session()
        course_infos = Courses.get_all_courses(_session)
        if not course_infos:
            print(colored("No Course Found\n", "red"))
            return
        print()
        for course in course_infos:
            if not course.active:
                continue
            print(
                colored(
                    f" Instructor id : {course.created_by} Course ID : {course.id}  Course Title : {course.name}",
                    "light_blue",
                )
            )
        print()
        while True:
            print(" Choose a valid course id, instructor id to enroll")

            instructor_id = input(colored(" Instuctor ID  : ", "light_blue"))
            course_id = input(colored(" Course ID     : ", "light_blue"))

            course_id = course_id.strip().strip("\n")
            instructor_id = instructor_id.strip().strip("\n")
            course_id = int(course_id)
            instructor_id = int(instructor_id)

            if (course_id, instructor_id) not in [(item.id, item.created_by) for item in course_infos]:
                print(colored(" Course ID or Instructor ID is not Valid, Kindly Try Agian\n", "red"))
                continue
            break
        enrollment_info = Enrollment.get_enrollment_by_ids(_session, self._user_info.id, instructor_id, course_id)
        if enrollment_info is not None:
            print(colored("\n Already Enrolled\n", "blue"))
            _session.close()
            return
        status = Enrollment(
            user_id=self._user_info.id,
            course_id=course_id,
            instructor_id=instructor_id,
        ).make_enrollment(_session)
        if status:
            _session.commit()
            _session.close()
            print(colored(f"\n Hi ,{self._user_info.name} , Enrollment is Sucessful\n", "blue"))
        else:
            print(colored(f"\n Hi ,{self._user_info.name} , Enrollment is not Sucessful\n", "red"))

    def _enroll_course_by_admin(self):
        _session = self._session()
        course_infos = Courses.get_all_courses(_session)
        if not course_infos:
            print(colored("No Course Found\n", "red"))
            return
        for course in course_infos:
            if not course.active:
                continue
            print(
                colored(
                    f"Instructor id : {course.created_by} Course ID : {course.id}  Course Title : {course.name}",
                    "light_blue",
                )
            )
        while True:
            print("Choose a valid course id, instructor id to enroll")
            user_id = input(colored(" User ID     : ", "light_blue"))
            course_id = input(colored(" Course ID     : ", "light_blue"))
            instructor_id = input(colored(" Instuctor ID : ", "light_blue"))

            course_id = course_id.strip().strip("\n")
            instructor_id = instructor_id.strip().strip("\n")
            course_id = int(course_id)
            instructor_id = int(instructor_id)
            user_id = int(user_id)

            enrollment_info = Enrollment.get_enrollment_by_ids(_session, user_id, instructor_id, course_id)
            if enrollment_info is not None:
                print(colored("\nAlready Enrolled\n", "red"))
                break
            new_enrollment = Enrollment(
                user_id=self._user_info.id,
                course_id=course_id,
                instructor_id=instructor_id,
            )
            status = new_enrollment.make_enrollment(_session)
            if status:
                _session.commit()
                _session.close()
                print(colored("\n Hi , Admin , Enrollment is Sucessful\n", "blue"))
                break
        return

    def _display_couseses(self):
        _session = self._session()
        course_infos = Courses.get_course_by_instrucitor_id(_session, self._user_info.id)
        if not course_infos:
            print(colored("\n No Course Found\n", "red"))
            return
        print()
        for course in course_infos:
            if not course.active:
                continue
            print(
                colored(
                    f" Course ID : {course.id}  Course Title : {course.name}",
                    "light_blue",
                )
            )
        _session.close()
        print()
        return

    def _remove_user_enrollement(self):
        _session = self._session()
        enroll_infos = Enrollment.get_enrollment_by_user_id(_session, self._user_info.id)
        if not enroll_infos:
            print(colored("No Enrollment Found\n", "red"))
            return
        print(colored("Here is your list Enrollments \n", "blue"))

        for item in enroll_infos:
            if not item.active:
                continue
            print(
                colored(
                    f"Enrollment id : {item.id} Course ID : {item.course_id}  Instructor id : {item.instructor_id}",
                    "light_blue",
                )
            )
        while True:
            print(colored("Kindly Choose the Enrollment id , for removel\n", "blue"))
            enrollment_id = input(colored(" Enrollment ID     : ", "light_blue"))
            enrollment_id = enrollment_id.strip().strip("\n")
            try:
                enrollment_id = int(enrollment_id)
            except ValueError:
                print(colored("Enrollment ID is not Valid\n", "red"))
                continue
            if enrollment_id not in [item.id for item in enroll_infos]:
                print(colored("Enrollment ID is not Valid\n", "red"))
                continue
            break
        status = Enrollment.remove_user_enrollement(_session, enrollment_id)
        if status:
            _session.commit()
            _session.close()
            print(colored(f"\n Hi , {self._user_info.name} , Enrollment is Removed Sucessful\n", "blue"))
        else:
            print(colored(f"\n Hi , {self._user_info.name} , Enrollment is not Removed\n", "red"))

    def _display_user_enrollement(self):
        _session = self._session()
        enroll_infos = Enrollment.get_enrollment_by_user_id(_session, self._user_info.id)
        if not enroll_infos:
            print(colored("No Enrollment Found\n", "red"))
            return
        print("\n Here is your list Enrollments \n")

        for item in enroll_infos:
            if not item.active:
                continue
            print(
                colored(
                    f" Enrollment id : {item.id} Course ID : {item.course_id}  Instructor id : {item.instructor_id}",
                    "light_blue",
                )
            )
        print()

    def _remove_course(self):
        _session = self._session()
        course_infos = Courses.get_course_by_instrucitor_id(_session, self._user_info.id)
        if not course_infos:
            print(colored("No Course Found\n", "red"))
            return
        for course in course_infos:
            if not course.active:
                continue
            print(
                colored(
                    f"Course ID : {course.id}  Course Title : {course.name}",
                    "light_blue",
                )
            )
        while True:
            print(colored("Kindly Choose the Course Id , for removel\n", "blue"))
            course_id = input(colored(" Course Id     : ", "light_blue"))
            course_id = course_id.strip().strip("\n")
            try:
                course_id = int(course_id)
            except ValueError:
                print(colored("Course ID is not Valid\n", "red"))
                continue
            if course_id not in [item.id for item in course_infos]:
                print(colored("Course ID is not Valid\n", "red"))
                continue
            break
        if not isinstance(self._user_info, Instructor):
            return
        couses = Courses.remove_course(_session, course_id, self._user_info)
        if couses is not None:
            _session.commit()
            _session.close()
        else:
            print(colored("Course Creation is not Sucessful\n", "red"))
