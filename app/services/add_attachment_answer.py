from fastapi import HTTPException, Depends
from app.core.database import get_db_connection, get_database_connection
from app.models.answers import AnswerList, Answer
from psycopg2.extras import execute_values


async def add_attachment_answers(answer_list: AnswerList):
    answers = answer_list.answers
    query = """
    INSERT INTO attachment_chats (question_id, report_id, user_id, answer,category_id,attachment_flag)
    VALUES %s
    """

    values = [
        (
            str(ans.question_id),
            str(ans.report_id),
            str(ans.user_id),
            ans.answer,
            str(ans.category_id),
            False,
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


async def add_attachment_answer_by_llm(
    question_number,
    report_id,
    user_id,
    content,
    category_id,
):
    query = """
    INSERT INTO attachment_chats (question_id, report_id, user_id, answer,category_id,attachment_flag)
    VALUES  (%s, %s, %s, %s, %s, %s)
    """

    values = (
        str(question_number),
        str(report_id),
        str(user_id),
        str(content),
        str(category_id),
        True,
    )

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        cur.close()
        return {
            "status": "success",
        }
    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def add_attachment_answer_content(content, report_id, user_id, category_id):
    query = """
    INSERT INTO attachment (report_id, user_id, content, category_id)
    VALUES (%s, %s, %s, %s)
    """
    values = (
        str(report_id),
        str(user_id),
        content,
        str(category_id),
    )

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        cur.close()
        return {"status": "success"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
