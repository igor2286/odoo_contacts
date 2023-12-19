from typing import Dict

from pydantic import BaseModel


class SchemaContact(BaseModel):
    """Validation schema for contacts data"""

    id: int
    info: Dict

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": '1',
                    "info": {
                        "message_is_follower": False,
                        "message_follower_ids": [],
                        "message_partner_ids": [],
                        "message_ids": [885, 882],
                        "has_message": True,
                    }

                }
            ]
        }
    }
