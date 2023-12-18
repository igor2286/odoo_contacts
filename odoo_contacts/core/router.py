from typing import List
from fastapi import APIRouter, Depends
from odoo_contacts.core.dao import ContactDAO
from odoo_contacts.core.schemas import SchemaContact
from odoo_contacts.users.dependencies import get_current_user

router = APIRouter(
    prefix='/contacts',
    tags=['Contacts'],
    dependencies=[Depends(get_current_user)]
)


@router.get("/get_all")
async def get_all_contacts() -> List[SchemaContact] | None:
    """Get all contacts from DB"""
    return await ContactDAO.find_all()


@router.get("/get_by_id")
async def get_contact_by_id(contact_id: int):
    """Get contact from DB by id"""
    return await ContactDAO.find_by_id(obj_id=contact_id)
