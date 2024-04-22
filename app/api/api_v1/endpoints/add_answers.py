from fastapi import APIRouter, HTTPException, Depends
from app.services.add_answers import add_answers
from app.models.answers import AnswerList
from psycopg2.extras import execute_values
import json

router = APIRouter()

@router.post("/add-answers/")
async def add_answer_list(answer_list: AnswerList):
    try:
        response_data = await add_answers(answer_list)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
