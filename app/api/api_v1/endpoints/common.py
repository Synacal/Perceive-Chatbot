from fastapi import APIRouter, HTTPException, Depends

from app.models.common import Draft
from psycopg2.extras import execute_values
import json
from app.services.common import add_draft

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
