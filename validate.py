"""Handles all validations."""


import re
from fastapi import HTTPException, status


def validate_password(password: str) -> None:
    """Validate Password.

    Args:
        password (str): password to validate

    Raises:
        HTTPException: if password is invalid
    """
    msg = ""
    if len(password) < 8:
        msg = "Make sure your password is at lest 8 letters"
    elif re.search("[0-9]", password) is None:
        msg = "Make sure your password has a number in it"
    elif re.search("[A-Z]", password) is None:
        msg = "Make sure your password has a capital letter in it"
    elif re.search("[a-z]", password) is None:
        msg = "Make sure your password has a small letter in it"
    elif re.search("[@$!#%*?&^ _-]", password) is None:
        msg = "Make sure your password has a special letter in it"
    if msg != "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg,
        )


def validate_user_name(user_name: str) -> None:
    """Validate user name.

    Args:
        user_name (str): user name to validate

    Raises:
        HTTPException: if user name is invalid
    """
    if re.match(r"[A-Za-z0-9_ -]{3,15}$", user_name) is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User name must contains 3 to 15 characters and "
            "only alphanumerics, underscore, hypen and spaces are allowed",
        )
