import xmlrpc.client
from typing import List, Dict

from odoo_contacts.exceptions import CannotGetDataFromOdoo, CannotAuthenticateToOdoo


def get_odoo_authenticated_uid(url: str, db: str, username: str, password: str) -> int:
    """Authentication to odoo"""
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
    except CannotAuthenticateToOdoo as e:
        raise e.detail
    return uid


def get_odoo_contacts_data(url: str, db: str, username: str, password: str) -> List[Dict]:
    """Retrieve data from odoo"""
    try:
        uid = get_odoo_authenticated_uid(url=url, db=db, username=username, password=password)
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        contacts_data = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                          [[['is_company', '=', True]]])

    except CannotGetDataFromOdoo as e:
        raise e.detail

    return contacts_data
