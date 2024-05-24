from pydantic import BaseModel
from typing import List


class Attachment(BaseModel):
    category_id: str
    session_id: str
    user_id: str
    attachment: str


class attachmentAnswer(BaseModel):
    question_id: str
    session_id: str
    user_id: str
    answer: str
    category_id: str


class attachmentAnswerList(BaseModel):
    answers: List[attachmentAnswer]
