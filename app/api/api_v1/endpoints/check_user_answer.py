from fastapi import APIRouter, HTTPException
from app.services.check_user_answers import check_user_answers
from psycopg2.extras import execute_values
import json

router = APIRouter()

@router.post("/generate/")
async def generate_response(answer: str,QuestionID: int,userID: int,sessionID: int):
    try:
        response_data = await check_user_answers(answer,QuestionID,userID,sessionID)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
