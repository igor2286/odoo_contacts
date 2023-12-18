from fastapi import HTTPException, status


class CustomExceptions(HTTPException):
    """Custom exception constructor"""
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CannotGetDataFromOdoo(CustomExceptions):
    """CannotGetDataFromOdoo exception"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to retrieve data from Odoo. Contact the administrator"


class CannotAuthenticateToOdoo(CustomExceptions):
    """CannotAuthenticateToOdoo exception"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Cannot connect to Odoo server. Verify Odoo credentials"


class UserAlreadyExistsException(CustomExceptions):
    """UserAlreadyExistsException exception"""
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exist"


class IncorrectEmailOrPasswordException(CustomExceptions):
    """IncorrectEmailOrPasswordException exception"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect password or email"


class TokenExpiredException(CustomExceptions):
    """TokenExpiredException exception"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Expired token. Please login again."


class TokenAbsentException(CustomExceptions):
    """TokenAbsentException exception"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "UNAUTHORIZED. Token not exist"


class IncorrectTokenFormatException(CustomExceptions):
    """IncorrectTokenFormatException exception"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresentException(CustomExceptions):
    """UserIsNotPresentException exception"""
    status_code = status.HTTP_401_UNAUTHORIZED


class CannotAddDataToDatabase(CustomExceptions):
    """CannotAddDataToDatabase exception"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add entry. Contact the administrator."
