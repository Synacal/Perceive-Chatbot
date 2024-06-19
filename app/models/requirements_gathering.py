from pydantic import BaseModel
from typing import List


class RequirementsGathering(BaseModel):
    user_id: str
    use_case_ids: List[str]
