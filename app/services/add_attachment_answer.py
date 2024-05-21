from fastapi import HTTPException, Depends
from app.core.database import get_db_connection, get_database_connection
from app.models.answers import AnswerList
from psycopg2.extras import execute_values


async def add_attachment_answers(answer_list: AnswerList):
    answers = answer_list.answers
    query = """
    INSERT INTO attachment_chats (question_id, session_id, user_id, answer,category_id)
    VALUES %s
    """

    values = [
        (
            str(ans.question_id),
            str(ans.session_id),
            str(ans.user_id),
            ans.answer,
            str(ans.category_id),
        )
        for ans in answers
    ]

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        execute_values(cur, query, values)
        conn.commit()
        cur.close()
        return {"status": "success", "inserted_count": len(values)}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
