from pydantic import BaseModel
from typing import List


class ReportParams(BaseModel):
    requirement_gathering_id: int
    user_case_id: str


class SearchQuery(BaseModel):
    keywords: List[str]


class PatentAnalysis(BaseModel):
    description: str


class SearchRequest(BaseModel):
    query: SearchQuery
    answer_list: PatentAnalysis


class PatentResult(BaseModel):
    id: str
    title: str
    abstract: str
    content: str


class PatentList(BaseModel):
    patents: List[PatentResult]
