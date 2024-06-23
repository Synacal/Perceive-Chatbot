from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.services.ip_license_process.common import (
    get_answers,
    get_keywords,
    search_patents_ids,
    search_patents,
    get_summary,
    get_patent_data,
    create_report,
)

from app.models.ip_license_process import ReportParams

router = APIRouter()


@router.post("/ip_license_process")
async def ip_license_process(report_params: ReportParams):
    try:
        answers = await get_answers(
            report_params.requirement_gathering_id, report_params.user_case_id
        )

        print("1. Answers: ", answers)
        summary = await get_summary(answers)
        print("2. Summary: ", summary)
        keywords = await get_keywords(answers)
        print("3. Keywords: ", keywords)

        patents_ids = await search_patents_ids(keywords)
        print("4. Patents IDs: ", patents_ids)
        # documents = documents[:6]
        # patents = await search_patents(documents, summary)
        patent_data = await get_patent_data(patents_ids)
        print("5. Patent Data: ", patent_data)
        report = await create_report(summary, patent_data)
        print("6. Report: ", report)
        return report

        # return {"patents": patents_ids, "patent_data": patent_data}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
