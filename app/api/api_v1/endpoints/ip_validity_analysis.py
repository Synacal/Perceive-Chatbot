import json
from fastapi import APIRouter, HTTPException, Depends
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
)

router = APIRouter()


@router.post("/ip_validity_analysis")
async def ip_validity_analysis(report_params: ReportParams):
    try:

        answers = await get_answers(
            report_params.requirement_gathering_id, report_params.user_case_id
        )
        summary = await get_summary(answers)
        print("1")
        keywords = await get_keywords(answers)
        print(keywords)
        print("2")
        response_data = await search_documents(keywords)
        print("3")
        response_data = response_data[:6]
        print(len(response_data))
        response_data2 = await search_patents(response_data, summary)
        print("4")

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
            print("4")
            assessment = await create_assessment(
                response_data2,
                answers,
                patentability_criteria[i],
            )
            report[patentability_criteria[i]] = assessment
            print("5")

        # Convert report dictionary to JSON string
        report_json = json.dumps(report)
        print("6")
        await add_report(
            report_json,
            report_params.requirement_gathering_id,
            report_params.user_case_id,
        )
        print("7")
        return report
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
