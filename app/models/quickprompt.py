from pydantic import BaseModel
from typing import Dict, Any


class QuickPrompt(BaseModel):
    user_id: str
    report_id: str
    prompt_data: Dict[str, Any]
    content: str
