from pydantic import BaseModel, EmailStr


class SchemaUserAuth(BaseModel):
    """Validation schema for user auth"""

    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": 'odo@user.com',
                    "password": "odoo"
                }
            ]
        }
    }
