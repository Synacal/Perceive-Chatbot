from fastapi import HTTPException, Depends
from app.core.database import get_db_connection, get_database_connection
from app.models.common import Draft
from psycopg2.extras import execute_values
import psycopg2.extras
import json
from app.models.quickprompt import QuickPrompt


async def add_quickprompt(prompt_data: QuickPrompt):
    query = """
    INSERT INTO quickprompt (user_id, content, prompt_data, requirement_gathering_id) 
    VALUES (%s, %s, %s::jsonb, %s)
    ON CONFLICT (requirement_gathering_id, user_id)
    DO UPDATE SET 
        prompt_data = EXCLUDED.prompt_data,
        content = EXCLUDED.content
    """

    values = (
        prompt_data.user_id,
        prompt_data.content,
        json.dumps(prompt_data.prompt_data),  # Convert list of dicts to JSON string
        prompt_data.requirement_gathering_id,
    )
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)  # Use execute instead of execute_values
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


async def get_quickprompt_by_ids(requirement_gathering_id: int, user_id: str):
    query = """
        SELECT * FROM quickprompt WHERE requirement_gathering_id = %s AND user_id = %s
        """
    values = (requirement_gathering_id, user_id)
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, values)
        result = cur.fetchone()
        if result:
            prompt_data = result["prompt_data"]
            if isinstance(prompt_data, str):
                prompt_data = json.loads(prompt_data)
            return {
                "requirement_gathering_id": result["requirement_gathering_id"],
                "user_id": result["user_id"],
                "prompt_data": prompt_data,
                "content": result["content"],
            }
        else:
            return {
                "requirement_gathering_id": requirement_gathering_id,
                "user_id": user_id,
                "prompt_data": [],
                "content": "",
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


async def get_quickprompts_by_user_id(user_id: str):
    query = """
        SELECT * FROM quickprompt WHERE user_id = %s
        """
    values = (user_id,)
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, values)
        results = cur.fetchall()
        prompts = []
        for result in results:
            prompt_data = result["prompt_data"]
            if isinstance(prompt_data, str):
                prompt_data = json.loads(prompt_data)
            prompts.append(
                {
                    "requirement_gathering_id": result["requirement_gathering_id"],
                    "user_id": result["user_id"],
                    "prompt_data": prompt_data,
                    "content": result["content"],
                }
            )
        return prompts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
