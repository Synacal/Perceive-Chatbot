from fastapi import APIRouter, HTTPException, Depends

from app.models.quickprompt import QuickPrompt
from psycopg2.extras import execute_values
import json
from app.services.quickprompt import (
    add_quickprompt,
    get_quickprompt_by_ids,
    update_quickprompt_by_user_id_and_report_id,
    get_quickprompts_by_user_id,
)

router = APIRouter()


@router.post("/quick-prompt/")
async def add_quick_prompt(prompt_data: QuickPrompt):
    try:
        response_data = await add_quickprompt(prompt_data)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quick-prompt-by-ids/")
async def get_quick_prompt_by_ids(report_id: str, user_id: str):
    try:
        response_data = await get_quickprompt_by_ids(report_id, user_id)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quick-prompt-by-user-id")
async def get_quick_prompt_by_user_id(user_id: str):
    try:
        response_data = await get_quickprompts_by_user_id(user_id)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/quick-prompt/")
async def get_quick_prompt_by_ids(prompt_data: QuickPrompt):
    try:
        response_data = await update_quickprompt_by_user_id_and_report_id(prompt_data)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
