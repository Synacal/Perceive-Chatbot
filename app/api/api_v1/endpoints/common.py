from fastapi import APIRouter, HTTPException, Depends

from app.models.common import Draft
from psycopg2.extras import execute_values
import json
from app.services.common import (
    add_draft,
    get_draft_by_ids,
    get_drafts_by_user_id,
    delete_draft_by_ids,
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
