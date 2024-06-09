from pydantic import BaseModel
from typing import List


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