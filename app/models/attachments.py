from pydantic import BaseModel

class Attachment(BaseModel):
    title: str
    attachment: str
    