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