from odoo_contacts.core.models import Contact
from odoo_contacts.base_dao import BaseDAO


class ContactDAO(BaseDAO):
    """Data Access Object for Contact model"""
    model = Contact
