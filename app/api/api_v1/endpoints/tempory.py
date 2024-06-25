from fastapi import APIRouter, HTTPException
from app.services.check_user_answers import check_user_answers
from psycopg2.extras import execute_values
import json
from app.core.azure_client import client

router = APIRouter()


@router.post("/tempory/")
async def tempory(user_prompt: str):
    system_prompt = "Answer the following questions to the best of your ability. If you do not know the answer, please type 'I do not know'."

    message_text = {"system_prompt": system_prompt, "user_prompt": user_prompt}

    try:
        completion = client.chat.completions.create(
            model="gpt-35-turbo",
            messages=message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )

        content = completion.choices[0].message.content
        return {"response": content}
    except Exception as e:
        return {"error": str(e)}
