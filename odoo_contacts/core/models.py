from sqlalchemy import Column, Integer, JSON

from odoo_contacts.sql.database import Base


class Contact(Base):
    """Contact data model"""
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, autoincrement=False)
    info = Column(JSON)

