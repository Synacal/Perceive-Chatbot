from fastapi import APIRouter, HTTPException
from app.services.check_user_answers import check_user_answers
from psycopg2.extras import execute_values
import json
from app.core.azure_client import client

router = APIRouter()


@router.get("/tempory/")
async def tempory():
    system_prompt = "Answer the following questions to the best of your ability. If you do not know the answer, Answer should be more than 100 words. please type 'I do not know'."
    user_prompt = "What is the difference between a provisional patent and a non-provisional patent?"
    message_text = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

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
