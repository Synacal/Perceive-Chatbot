from pydantic import BaseModel
from typing import List


class RequirementsGathering(BaseModel):
    user_id: str
    user_case_ids: List[str]
