from pydantic import BaseModel
from typing import Dict, Any


class Draft(BaseModel):
    requirement_gathering_id: int
    user_id: str
    current_page: str
    other_data: Dict[str, Any]


class SummaryData(BaseModel):
    requirement_gathering_id: int
    use_case_ids: list[str]
