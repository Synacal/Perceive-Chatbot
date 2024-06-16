# app/api/schemas.py
from pydantic import BaseModel
from typing import List


class Answer(BaseModel):
    question_id: str
    requirement_gathering_id: int
    user_id: str
    answer: str


class AnswerList(BaseModel):
    answers: List[Answer]


class AnswerQuery(BaseModel):
    user_id: str
    requirement_gathering_id: str
