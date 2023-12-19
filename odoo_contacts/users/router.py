from fastapi import APIRouter, Response

from odoo_contacts.exceptions import UserAlreadyExistsException, CannotAddDataToDatabase
from odoo_contacts.users.auth import authenticate_user, create_access_token, get_password_hash
from odoo_contacts.users.dao import UserDAO
from odoo_contacts.users.schemas import SchemaUserAuth

# prefix route for endpoints
router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)


@router.post("/signup", status_code=201)
async def register_user(user_data: SchemaUserAuth):
    """Endpoint to sign up user in the system."""
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    if not new_user:
        raise CannotAddDataToDatabase
    return {'info': 'Registration was successful!'}


@router.post("/login")
async def login_user(response: Response, user_data: SchemaUserAuth):
    """Endpoint ot log in user in the system."""
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("oddo_contacts_access_token", access_token, httponly=True)
    return {'access_token': access_token}


@router.post("/logout")
async def logout_user(response: Response):
    """Endpoint ot log out user in the system"""
    response.delete_cookie('oddo_contacts_access_token')
