from fastapi import HTTPException, Depends
from app.core.database import get_db_connection, get_database_connection
from app.models.common import Draft
from psycopg2.extras import execute_values
import psycopg2.extras
import json
from app.models.common import Draft


async def add_draft(draft_data: Draft):
    query = """
        INSERT INTO draft (report_id, user_id, other_data,current_page) VALUES %s
        """
    # Convert other_data to a JSON string
    other_data_str = json.dumps(draft_data.other_data)

    values = [
        (
            draft_data.report_id,
            draft_data.user_id,
            other_data_str,
            draft_data.current_page,
        )
    ]
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        execute_values(cur, query, values)
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


async def get_drafts_by_user_id(UserID: str):
    query = """
        SELECT * FROM draft WHERE user_id = %s  """
    values = (UserID,)
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, values)
        result = cur.fetchall()
        answer = []
        for row in result:
            other_data = row["other_data"]
            if isinstance(other_data, str):
                other_data = json.loads(other_data)
            answer.append(
                Draft(
                    report_id=row["report_id"],
                    user_id=row["user_id"],
                    current_page=row["current_page"],
                    other_data=other_data,
                )
            )
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


async def get_draft_by_ids(UserID: str, ReportID: str):
    query = """
        SELECT * FROM draft WHERE user_id = %s AND report_id = %s
        """
    values = (UserID, ReportID)
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, values)
        result = cur.fetchall()
        answer = []
        for row in result:
            other_data = row["other_data"]
            if isinstance(other_data, str):
                other_data = json.loads(other_data)
            answer.append(
                Draft(
                    report_id=row["report_id"],
                    user_id=row["user_id"],
                    current_page=row["current_page"],
                    other_data=other_data,
                )
            )

        return answer

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
