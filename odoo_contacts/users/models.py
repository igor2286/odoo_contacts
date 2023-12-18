from sqlalchemy.orm import mapped_column, Mapped

from odoo_contacts.sql.database import Base


class User(Base):
    """User data model"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    def __str__(self):
        return f"User {self.email}"
