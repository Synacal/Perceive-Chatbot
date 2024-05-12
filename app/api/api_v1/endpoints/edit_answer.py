from fastapi import APIRouter, HTTPException
from app.services.edit_answers import edit_answer

router = APIRouter()

@router.put("/edit-answer/")
async def edit_answer_endpoint(userID: str, sessionID: str, questionID: str, newAnswer: str):
    try:
        response_data = await edit_answer(userID, sessionID, questionID, newAnswer)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))