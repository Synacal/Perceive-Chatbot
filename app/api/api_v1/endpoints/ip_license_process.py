from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.services.ip_license_process.common import (
    get_answers_license,
    get_keywords_license,
    search_patents_ids,
    search_patents,
    get_summary_license,
    get_patent_data,
    create_report,
)

from app.models.ip_license_process import ReportParams

router = APIRouter()


@router.post("/ip_license_process")
async def ip_license_process(report_params: ReportParams):
    try:
        answers = await get_answers_license(
            report_params.requirement_gathering_id, report_params.user_case_id
        )

        summary = await get_summary_license(answers)
        keywords = await get_keywords_license(answers)
        patents_ids = await search_patents_ids(keywords)
        patent_data = await get_patent_data(patents_ids)
        report = await create_report(summary, patent_data)
        return report

        # return {"patents": patents_ids, "patent_data": patent_data}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
