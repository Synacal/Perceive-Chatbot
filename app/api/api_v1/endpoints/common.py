from fastapi import APIRouter, HTTPException, Depends

from app.models.common import Draft, SummaryData
from psycopg2.extras import execute_values
import json
from app.services.common import (
    add_draft,
    get_draft_by_ids,
    get_drafts_by_user_id,
    delete_draft_by_ids,
    get_answers_with_questions,
    get_summary_data,
    get_report_by_user_id,
)

router = APIRouter()


@router.post("/draft/")
async def add_answer_list(draft_data: Draft):
    try:
        response_data = await add_draft(draft_data)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/draft-by-ids/")
async def get_draft(user_id: str, requirement_gathering_id: int):
    try:
        response_data = await get_draft_by_ids(user_id, requirement_gathering_id)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/drafts-by-user-id/")
async def get_drafts(user_id: str):
    try:
        response_data = await get_drafts_by_user_id(user_id)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/draft/")
async def delete_draft(user_id: str, requirement_gathering_id: int):
    try:
        response_data = await delete_draft_by_ids(user_id, requirement_gathering_id)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summary")
async def get_summary(summary_data: SummaryData):
    try:
        response_data = []
        for use_case_id in summary_data.use_case_ids:
            if not isinstance(use_case_id, str):
                raise HTTPException(
                    status_code=400, detail="use_case_id should be a list of strings"
                )
            answers = await get_answers_with_questions(
                summary_data.requirement_gathering_id, use_case_id
            )
            # if answers:
            summary = await get_summary_data(answers)
            # elif answers == []:
            #    summary = ""
            # else:
            #    summary = "false"
            response_data.append({"use_case_id": use_case_id, "summary": summary})
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports-by-user-id")
async def get_report_by_user(user_id: str):
    try:
        response_data = await get_report_by_user_id(user_id)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
