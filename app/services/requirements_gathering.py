from fastapi import HTTPException
from app.models.requirements_gathering import RequirementsGathering
from app.core.database import get_db_connection
import uuid


async def get_requirements_gathering(requirements: RequirementsGathering):
    query = """
    INSERT INTO requirements_gathering (user_id, report_id,user_case_id)
    VALUES %s
    """

    try:
        conn = get_db_connection()
        async with conn.transaction():
            for user_case_id in requirements.user_case_ids:
                # Generate a UUID for report_id
                report_id = str(uuid.uuid4())
                # Execute the query with the generated report_id
                await conn.execute(
                    query, (requirements.user_id, report_id, user_case_id)
                )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
