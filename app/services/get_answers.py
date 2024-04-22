from fastapi import HTTPException, Depends
from typing import List
from app.models.answers import AnswerQuery, Answer
from app.core.database import get_db_connection
from psycopg2.extras import execute_values
import psycopg2.extras

async def get_answers(query: AnswerQuery):
    sql = """
    SELECT question_id, session_id, user_id, answer
    FROM user_chats
    WHERE user_id = %s AND session_id = %s;
    """

    values = (query.user_id, query.session_id)
    
    try:
        conn=get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  # Use DictCursor to access data by column names
        cur.execute(sql, values)  # Correct function for executing a query with parameters
        rows = cur.fetchall()
        cur.close()
        # Convert fetched rows to list of Answer objects
        answers = [Answer(question_id=row['question_id'], session_id=row['session_id'], user_id=row['user_id'], answer=row['answer']) for row in rows]
        return answers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))