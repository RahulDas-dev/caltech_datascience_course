from enum import Enum


class UserType(str, Enum):
    """The Enum Class represents different type of user."""

    LERNER = "LERNER"
    INSTRUCTOR = "INSTRUCTOR"
    ADMIN = "ADMIN"
