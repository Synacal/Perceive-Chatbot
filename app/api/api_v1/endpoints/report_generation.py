from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

from app.services.report_generation import generate_reports

from app.models.report_generation import ReportParams


@router.get("/report_generation/")
async def generate_report(report_params: ReportParams):
    try:
        response_data = await generate_reports(report_params.requirement_gathering_id)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
