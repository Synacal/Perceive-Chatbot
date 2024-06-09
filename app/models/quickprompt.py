from pydantic import BaseModel
from typing import Dict, Any, List


class QuickPrompt(BaseModel):
    user_id: str
    requirement_gathering_id: int
    prompt_data: List[Dict[str, Any]]
    content: str
