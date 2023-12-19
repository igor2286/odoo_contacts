import asyncio
from typing import List
from odoo_contacts.core.dao import ContactDAO
from odoo_contacts.core.schemas import SchemaContact
from odoo_contacts.odoo import get_odoo_contacts_data
from odoo_contacts.config import settings
from odoo_contacts.utils.pool_utils import process_polling


def check_contacts(iterable: List, contacts_from_storage: List, model_dao: ContactDAO):
    """Util for adding and updating data in DB"""
    to_insert_objects, to_update_objects = [], []
    get_contact_id_list = [contact.id for contact in contacts_from_storage]

    for contact in iterable:
        if contact.id not in get_contact_id_list:
            to_insert_objects.append(contact.dict())
        else:
            if contact not in contacts_from_storage:
                to_update_objects.append(contact.dict())

    def insert():
        if to_insert_objects:
            to_ins = model_dao.add_bulk(to_insert_objects)
            asyncio.run(to_ins)

    def update():
        if to_update_objects:
            for update_obj in to_update_objects:
                to_upd = model_dao.update(obj_id=update_obj['id'], info=update_obj['info'])
                asyncio.run(to_upd)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(insert())
    loop.run_until_complete(update())


async def odoo_contacts():
    """Get and manipulate with odoo data util"""
    odoo_contact_data = get_odoo_contacts_data(url=settings.ODOO_URL,
                                               db=settings.ODOO_DB,
                                               username=settings.ODOO_USERNAME,
                                               password=settings.ODOO_PASSWORD
                                               )

    odoo_contacts_objects = [SchemaContact(id=contact.pop("id"), info=contact) for contact in odoo_contact_data]

    contacts = await ContactDAO.find_all()

    process_polling(call_func=check_contacts,
                    iterable=odoo_contacts_objects,
                    contacts_from_storage=contacts,
                    return_result=False,
                    model_dao=ContactDAO)

    contacts = await ContactDAO.find_all()
    to_delete_objects = []
    odoo_contacts_objects_id = [contact.id for contact in odoo_contacts_objects]

    for contact in contacts:
        if contact.id not in odoo_contacts_objects_id:
            to_delete_objects.append(contact.id)

    for contact_to_delete in to_delete_objects:
        await ContactDAO.delete(id=contact_to_delete)
