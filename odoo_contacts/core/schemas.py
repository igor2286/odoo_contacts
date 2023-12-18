from typing import Dict

from pydantic import BaseModel


class SchemaContact(BaseModel):
    """Validation schema for contacts data"""

    id: int
    info: Dict
