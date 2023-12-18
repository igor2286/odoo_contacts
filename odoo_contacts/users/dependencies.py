from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from odoo_contacts.config import settings
from odoo_contacts.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)

from odoo_contacts.users.dao import UserDAO


def get_token(request: Request):
    """Get token if exist"""

    token = request.cookies.get("oddo_contacts_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    """Get current user"""

    try:
        # try to get info about current user
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
