from fastapi import APIRouter, HTTPException, Depends
from app.services.add_answers import add_answers
from app.services.get_answers import get_answers
from app.services.edit_answer import edit_answer_function
from app.models.answers import AnswerList, AnswerQuery
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
    
@router.get("/get-answers/")
async def get_answer_list(userID: str,sessionID: str):
    try:
        response_data = await get_answers(userID,sessionID)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/edit-answer/")
async def edit_answer(userID: str, sessionID: str, questionID: str, newAnswer: str):
    try:
        response_data = await edit_answer_function(userID, sessionID, questionID, newAnswer)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))