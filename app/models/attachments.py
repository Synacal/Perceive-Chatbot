from pydantic import BaseModel
from typing import List


class Attachment(BaseModel):
    category_ids: list[str]
    report_id: str
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
