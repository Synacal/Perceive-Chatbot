from pydantic import BaseModel
from typing import List


class Attachment(BaseModel):
    use_cases_ids: list[str]
    requirement_gathering_id: int
    user_id: str
    attachment: str


class attachmentAnswer(BaseModel):
    question_id: str
    report_id: str
    user_id: str
    answer: str
    category_id: str


class attachmentAnswerList(BaseModel):
    answers: List[attachmentAnswer]
