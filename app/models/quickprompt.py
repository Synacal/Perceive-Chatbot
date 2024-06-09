from pydantic import BaseModel
from typing import Dict, Any, List


class QuickPrompt(BaseModel):
    user_id: str
    report_id: str
    prompt_data: List[Dict[str, Any]]
    content: str
