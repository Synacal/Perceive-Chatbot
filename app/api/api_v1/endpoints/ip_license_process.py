from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.services.ip_license_process.common import (
    get_answers,
    get_keywords,
    search_documents,
    search_patents,
    get_summary,
)

from app.models.ip_license_process import ReportParams

router = APIRouter()


@router.post("/ip_license_process")
async def ip_license_process(report_params: ReportParams):
    try:
        answers = await get_answers(
            report_params.requirement_gathering_id, report_params.user_case_id
        )

        summary = await get_summary(answers)
        print(f"Summary: {summary}")
        keywords = await get_keywords(answers)
        documents = await search_documents(keywords)
        documents = documents[:6]
        patents = await search_patents(documents, summary)
        print(patents)
        print(f"Number of patents found: {len(patents)}")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
