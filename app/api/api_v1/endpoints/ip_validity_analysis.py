import json
from fastapi import BackgroundTasks, APIRouter, HTTPException, Depends
from typing import List

from app.models.ip_validity_analysis import ReportParams

from app.services.ip_validity_analysis.common import (
    create_assessment,
    search_documents,
    search_patents,
    get_answers,
    get_keywords,
    add_report,
    get_summary,
    create_report_background,
    get_report_file,
)

router = APIRouter()

"""
@router.post("/ip_validity_analysis")
async def ip_validity_analysis(report_params: ReportParams):
    try:

        answers = await get_answers(
            report_params.requirement_gathering_id, report_params.user_case_id
        )
        summary = await get_summary(answers)
        keywords = await get_keywords(answers)
        response_data = await search_documents(keywords)
        response_data = response_data[:10]
        response_data2 = await search_patents(response_data, summary)

        patentability_criteria = [
            "Novelty (35 U.S.C. § 102)",
            "Non-Obviousness (35 U.S.C. § 103)",
            "Utility (35 U.S.C. § 101)",
            "Enablement (35 U.S.C. § 112(a))",
            "Written Description (35 U.S.C. § 112(a))",
            "Definiteness (35 U.S.C. § 112(b))",
            "Industrial Application",
            "Clarity & Sufficiency",
            "Scope & Definition",
            "Economic Significance",
        ]

        report = {}

        for i in range(len(patentability_criteria)):
            assessment = await create_assessment(
                response_data2,
                answers,
                patentability_criteria[i],
            )
            report[patentability_criteria[i]] = assessment

        # Convert report dictionary to JSON string
        report_str = str(report)
        await add_report(
            report_str,
            report_params.requirement_gathering_id,
            report_params.user_case_id,
        )
        return report
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""


@router.post("/ip_validity_analysis")
async def ip_validity_analysis(
    report_params: ReportParams, background_tasks: BackgroundTasks
):
    try:
        # Start the background task for report creation
        background_tasks.add_task(create_report_background, report_params)
        answers = await get_answers(
            report_params.requirement_gathering_id, report_params.user_case_id
        )
        summary = await get_summary(answers)

        # Return summary and status as "in progress" immediately
        return {"summary": summary, "status": "in progress"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ip_validity_analysis/")
async def get_report(requirement_gathering_id: int, user_case_id: str, file_type: str):
    try:
        report = await get_report_file(
            requirement_gathering_id, user_case_id, file_type
        )
        return report
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
