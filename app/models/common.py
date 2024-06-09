from pydantic import BaseModel
from typing import Dict, Any


class Draft(BaseModel):
    report_id: str
    user_id: str
    current_page: str
    other_data: Dict[str, Any]
