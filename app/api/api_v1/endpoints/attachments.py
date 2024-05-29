from fastapi import APIRouter, HTTPException
from psycopg2.extras import execute_values
from app.models.attachments import Attachment, attachmentAnswerList
from app.services.check_attachment import (
    get_pdf_content,
    get_questions,
    check_user_attachment,
    get_prompts,
    check_user_attachment_temp,
    find_question_number,
)
from app.services.add_attachment_answer import (
    add_attachment_answers,
    add_attachment_answer_content,
)

router = APIRouter()

"""
@router.post("/attachment-temp/")
async def add_attachment_temp(attachment: Attachment):
    try:
        questions = get_questions(attachment.category_id)
        content = get_pdf_content(attachment.attachment)
        prompts = get_prompts(attachment.category_id)
        result = await check_user_attachment(
            questions,
            prompts,
            content,
            attachment.session_id,
            attachment.user_id,
            attachment.category_id,
        )
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
"""


@router.post("/attachment/")
async def add_attachment(attachment: Attachment):
    try:
        content = get_pdf_content(attachment.attachment)
        questions = get_questions(attachment.category_id)
        prompts = get_prompts(attachment.category_id)

        uncompletedQuestions = []
        for i in range(len(questions)):
            result = await check_user_attachment_temp(
                questions[i],
                prompts[i],
                content,
                attachment.session_id,
                attachment.user_id,
                attachment.category_id,
            )
            if result["status"] == "false":
                question_number = find_question_number(questions[i])
                uncompletedQuestions.append(question_number)
        return uncompletedQuestions
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/attachment-answers/")
async def add_attachment_answer_list(answer_list: attachmentAnswerList):
    try:
        response_data = await add_attachment_answers(answer_list)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
