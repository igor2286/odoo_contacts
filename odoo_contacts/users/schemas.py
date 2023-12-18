from pydantic import BaseModel, EmailStr


class SchemaUserAuth(BaseModel):
    """Validation schema for user auth"""

    email: EmailStr
    password: str
