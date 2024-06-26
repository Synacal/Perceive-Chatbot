from pydantic import BaseModel


class ReportParams(BaseModel):
    requirement_gathering_id: int
