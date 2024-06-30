from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends

router = APIRouter()

from app.services.report_generation import generate_reports

from app.models.report_generation import ReportParams


@router.post("/report_generation/")
async def generate_report_endpoint(
    report_params: ReportParams, background_tasks: BackgroundTasks
):
    try:
        response_data = await generate_reports(
            report_params.requirement_gathering_id, background_tasks
        )
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from io import BytesIO
import base64
import psycopg2
from app.core.database import get_db_connection


@router.get("/download-file/")
async def download_file(
    requirement_gathering_id: int, user_case_id: str, report_type: str
):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        query = """
        SELECT file, file_type FROM report_file WHERE requirement_gathering_id = %s AND use_case_id = %s AND file_type = %s
        """
        values = (requirement_gathering_id, user_case_id, report_type)
        cur.execute(query, values)
        result = cur.fetchone()
        cur.close()

        if not result:
            raise HTTPException(
                status_code=404, detail=f"{report_type} file not found."
            )

        file_base64, file_type = result  # Unpack file_base64 and file_type from result

        # Decode base64 and create BytesIO buffer
        file_bytes = base64.b64decode(file_base64)
        file_buffer = BytesIO(file_bytes)

        # Determine media type based on file_type
        media_type = ""
        if file_type == "pdf":
            media_type = "application/pdf"
            filename = f"report_{requirement_gathering_id}_{user_case_id}.pdf"
        elif file_type == "docx":
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"report_{requirement_gathering_id}_{user_case_id}.docx"
        else:
            raise HTTPException(
                status_code=500, detail=f"Unsupported file type: {file_type}"
            )

        return StreamingResponse(
            file_buffer,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database operation failed: {str(e)}"
        )
    finally:
        conn.close()
