from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.ip_validity_analysis import SearchRequest

from app.services.ip_validity_analysis.common import (
    create_assessment,
    search_documents,
    search_patents,
    get_answers,
    get_keywords,
    add_report,
)

router = APIRouter()


@router.post("/ip_validity_analysis")
async def ip_validity_analysis(
    requirement_gathering_id: int, user_case_id: str, type_id: str
):
    try:

        answers = await get_answers(requirement_gathering_id, user_case_id, type_id)
        print("1")
        keywords = await get_keywords(answers)
        print(keywords)
        print("2")
        response_data = await search_documents(keywords)
        print("3")
        print(len(response_data))
        response_data = response_data[:6]
        response_data2 = await search_patents(response_data, answers)
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
            print(f"Assessment for {patentability_criteria[i]}: {assessment}")

        await add_report(report, requirement_gathering_id, user_case_id)
        return report

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
