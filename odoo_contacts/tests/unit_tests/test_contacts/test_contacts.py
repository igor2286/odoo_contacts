import pytest

from odoo_contacts.core.dao import ContactDAO


@pytest.mark.parametrize("contact_id,is_present", [
    (1, True),
    (2, True),
    (7, False),
])
async def test_find_user_by_id(contact_id, is_present):
    contact = await ContactDAO.find_one_or_none(id=contact_id)

    if is_present:
        assert contact
        assert contact["id"] == contact_id
    else:
        assert not contact
