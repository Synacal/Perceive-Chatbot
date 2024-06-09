from fastapi import HTTPException
from app.models.requirements_gathering import RequirementsGathering
from app.core.database import get_db_connection
import shortuuid


async def get_requirements_gathering(requirements: RequirementsGathering):
    query = """
    INSERT INTO requirements_gathering (user_id, report_id, user_case_id)
    VALUES (%s, %s, %s)
    RETURNING requirement_gathering_id
    """

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            for user_case_id in requirements.user_case_ids:
                # Generate a unique ID for report_id using shortuuid
                report_id = "PR" + shortuuid.uuid()
                # Execute the query with the generated report_id
                cur.execute(
                    query, (str(requirements.user_id), report_id, str(user_case_id))
                )
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
