from odoo_contacts.base_dao import BaseDAO
from odoo_contacts.users.models import User


class UserDAO(BaseDAO):
    """Data Access Object for User model"""

    model = User
