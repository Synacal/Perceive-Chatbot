from fastapi import APIRouter, HTTPException
from psycopg2.extras import execute_values
from app.models.attachments import Attachment, attachmentAnswerList
from app.services.add_attachment import (
    get_pdf_content,
    get_questions,
    check_user_attachment,
    get_prompts,
)
from app.services.add_attachment_answer import add_attachment_answers

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
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-attachment-answers/")
async def add_attachment_answer_list(answer_list: attachmentAnswerList):
    try:
        response_data = await add_attachment_answers(answer_list)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
