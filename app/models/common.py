from pydantic import BaseModel
from typing import Dict, Any


class Draft(BaseModel):
    session_id: str
    user_id: str
    other_data: Dict[str, Any]
