from pydantic import BaseModel
from typing import List


class attachmentAnswer(BaseModel):
    question_id: str
    report_id: str
    user_id: str
    answer: str
    category_id: str


class attachmentAnswerList(BaseModel):
    answers: List[attachmentAnswer]


class attachmentFile(BaseModel):
    file: str
    fileType: str
    fileName: str


class Attachment(BaseModel):
    user_cases_ids: list[str]
    requirement_gathering_id: int
    user_id: str
    attachments: List[attachmentFile]
    web_urls: List[str]
