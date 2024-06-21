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
    get_content,

    get_web_content,

)
from app.services.add_attachment_answer import (
    add_attachment_answers,
    add_attachment_answer_content,
    add_attachment_answer_by_llm,
    check_user_attachment_answer,
    get_report_id,
)


import requests
from bs4 import BeautifulSoup

router = APIRouter()


@router.post("/attachment/")
async def add_attachment(attachment: Attachment):
    try:
        # content = get_pdf_content(attachment.attachment)

        attachment_content = await get_content(attachment.attachments)
        web_content = await get_web_content(attachment.web_urls)
        content = attachment_content + web_content
        uncompleted_questions = []

        for use_case_id in attachment.use_cases_ids:
            questions = get_questions(use_case_id)
            prompts = get_prompts(use_case_id)

            attachment_content_save = await add_attachment_answer_content(

                content,
                attachment.requirement_gathering_id,
                attachment.user_id,
            )

            report_id = await get_report_id(
                attachment.requirement_gathering_id, user_case_id
            )

            for i in range(len(questions)):
                result = await check_user_attachment(
                    questions[i],
                    prompts[i],
                    content,
                    attachment.requirement_gathering_id,
                    attachment.user_id,
                    report_id,
                )
                if result["status"] == "false":
                    question_number = find_question_number(questions[i])
                    uncompleted_questions.append(
                        {
                            "question_id": question_number,
                        }
                    )

                else:
                    question_number = find_question_number(questions[i])

                    data = await add_attachment_answer_by_llm(
                        question_number,
                        report_id,
                        attachment.user_id,
                        result["answer"],
                        attachment.requirement_gathering_id,
                    )

        return uncompleted_questions

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/attachment-answer/")
async def add_attachment_answer(
    answer: str,
    QuestionID: int,
    userID: str,
    requirement_gathering_id: int,
    user_case_id: str,
):
    try:
        print("1")
        response_data = await check_user_attachment_answer(
            answer, QuestionID, userID, requirement_gathering_id, user_case_id
        )
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
