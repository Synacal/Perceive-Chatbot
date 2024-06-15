from typing import List, Optional, Any
from pydantic import BaseModel, validator
from datetime import date, datetime


class ReportParams(BaseModel):
    requirement_gathering_id: int
    user_case_id: str


class PatentResult(BaseModel):
    id: str
    title: str
    abstract: str
    content: str


class PatentList(BaseModel):
    patents: List[PatentResult]


class PatentData(BaseModel):
    reel_no: int
    frame_no: int
    last_update_date: str
    recorded_date: date
    assignee: str
    assignors: List[str]
