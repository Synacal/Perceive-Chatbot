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
    add_attachment_answer_by_llm,
)

router = APIRouter()


@router.post("/attachment/")
async def add_attachment(attachment: Attachment):
    try:
        content = get_pdf_content(attachment.attachment)
        uncompleted_questions = []

        for category_id in attachment.category_ids:
            questions = get_questions(category_id)
            prompts = get_prompts(category_id)

            for i in range(len(questions)):
                attachment_content = await add_attachment_answer_content(
                    content,
                    attachment.report_id,
                    attachment.user_id,
                    category_id,
                )
                result = await check_user_attachment(
                    questions[i],
                    prompts[i],
                    content,
                    attachment.report_id,
                    attachment.user_id,
                    category_id,
                )
                if result["status"] == "false":
                    question_number = find_question_number(questions[i])
                    uncompleted_questions.append(
                        {
                            "question_id": question_number,
                        }
                    )
                else:
                    add_attachment_answer_by_llm(
                        question_number,
                        attachment.report_id,
                        attachment.user_id,
                        content,
                        category_id,
                    )
        return uncompleted_questions

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
