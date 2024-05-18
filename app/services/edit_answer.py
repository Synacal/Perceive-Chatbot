from fastapi import HTTPException, Depends  
from app.core.database import get_db_connection, get_database_connection
from app.models.answers import AnswerList
from psycopg2.extras import execute_values

async def edit_answer_function(user_id: str, session_id: str, question_id: str, new_answer: str):
    sql = """
    UPDATE user_chats
    SET answer = %s
    WHERE user_id = %s AND session_id = %s AND question_id = %s;
    """

    values = (new_answer, user_id, session_id, question_id)
    
    try:
        conn = get_db_connection()
        print("Connected to DB!")
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()  # Commit the transaction
        cur.close()
        return {"message": "Answer edited successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))