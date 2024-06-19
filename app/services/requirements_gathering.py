from fastapi import HTTPException
from app.models.requirements_gathering import RequirementsGathering
from app.core.database import get_db_connection
import shortuuid


async def get_requirements_gathering(requirements: RequirementsGathering):
    fetch_id_query = "SELECT nextval('requirement_gathering_id_seq')"
    insert_query = """
    INSERT INTO requirements_gathering (requirement_gathering_id, user_id, report_id, use_case_id)
    VALUES (%s, %s, %s, %s)
    RETURNING requirement_gathering_id
    """

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Fetch the next requirement_gathering_id from the sequence
            cur.execute(fetch_id_query)
            requirement_gathering_id = cur.fetchone()[0]

            results = []
            for use_case_id in requirements.use_case_ids:
                # Generate a unique ID for report_id using shortuuid
                report_id = "PR" + shortuuid.uuid()
                # Execute the insert query with the fetched requirement_gathering_id
                cur.execute(
                    insert_query,
                    (
                        requirement_gathering_id,
                        str(requirements.user_id),
                        report_id,
                        str(use_case_id),
                    ),
                )
                result = cur.fetchone()  # Fetch the returned ID
                results.append(result[0])

        conn.commit()
        return {
            "status": "success",
            "requirement_gathering_id": requirement_gathering_id,
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
