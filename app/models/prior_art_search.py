from pydantic import BaseModel
from typing import List


class SearchQuery(BaseModel):
    keywords: List[str]


class PatentAnalysis(BaseModel):
    description: str


class PatentResult(BaseModel):
    id: str
    title: str
    abstract: str
    content: str


class PatentList(BaseModel):
    patents: List[PatentResult]


class SearchRequest(BaseModel):
    query: SearchQuery
    answer_list: PatentAnalysis


class PriorArtSearch(BaseModel):
    user_id: str
    session_id: str
    keywords: List[str]


class ReportParams(BaseModel):
    requirement_gathering_id: int
    user_case_id: str
