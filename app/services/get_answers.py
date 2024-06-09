from fastapi import HTTPException, Depends
from typing import List
from app.models.answers import AnswerQuery, Answer
from app.core.database import get_db_connection
import psycopg2
import psycopg2.extras


def get_answers(user_id: str, session_id: str):
    sql = """
    SELECT question_id, session_id, user_id, answer
    FROM user_chats
    WHERE user_id = %s AND session_id = %s;
    """
    values = (user_id, session_id)

    try:
        conn = (
            get_db_connection()
        )  # Ensure this function has its own error handling or is reliable
        print("Connected to DB!")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql, values)
        rows = cur.fetchall()

        if not rows:
            cur.close()
            conn.close()  # Ensure to close the connection in every exit path
            # Handling no records found scenario
            raise HTTPException(
                status_code=404,
                detail="No answers found for the specified user and session.",
            )

        answers = [
            Answer(
                question_id=row["question_id"],
                session_id=row["session_id"],
                user_id=row["user_id"],
                answer=row["answer"],
            )
            for row in rows
        ]
        cur.close()
        conn.close()  # Close connection after operation
        return answers

    except psycopg2.DatabaseError as e:
        # Handling database connection errors or SQL errors
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to the database or execute the query.",
        )
    except Exception as e:
        # General exception for any other unforeseen errors
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def get_all_answers_with_questions(user_id: str, session_id: str):
    # SQL query to join user_chats with question_category on question_id
    sql = """
    SELECT qc.question, uc.answer
    FROM user_chats uc
    JOIN questions qc ON uc.question_id = qc.question_id
    WHERE uc.user_id = %s AND uc.session_id = %s;
    """
    values = (user_id, session_id)

    try:
        conn = get_db_connection()
        print("Connected to DB!")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql, values)
        rows = cur.fetchall()

        if not rows:
            cur.close()
            conn.close()  # Ensure to close the connection
            raise HTTPException(
                status_code=404,
                detail="No answers found for the specified user and session.",
            )

        # Create a dictionary to hold the questions and answers
        qa_pairs = [
            {"question": row["question"], "answer": row["answer"]} for row in rows
        ]

        cur.close()
        conn.close()
        return qa_pairs

    except psycopg2.DatabaseError as e:
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to the database or execute the query.",
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
