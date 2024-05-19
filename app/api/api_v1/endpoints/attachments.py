from fastapi import APIRouter, HTTPException
from psycopg2.extras import execute_values
import json
import base64

from app.models.attachments import Attachment
from app.services.add_attachment import (
    get_pdf_content,
    get_questions,
    check_user_attachment,
    get_prompts,
)

router = APIRouter()


@router.post("/add-attachment/")
async def add_attachment(attachment: Attachment):
    try:
        questions = get_questions(attachment.title)
        content = get_pdf_content(attachment.attachment)
        prompts = get_prompts(attachment.title)

        result = await check_user_attachment(questions, prompts, content)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
