from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.ip_validity_analysis import SearchRequest

from app.services.ip_validity_analysis.common import (
    create_assessment,
    search_documents,
    search_patents,
)

router = APIRouter()


@router.post("/ip_validity_analysis")
async def keyword_search(request: SearchRequest):
    try:
        response_data = await search_documents(request.query)
        print(len(response_data))
        response_data = response_data[:6]
        response_data2 = await search_patents(
            response_data, request.answer_list.description
        )

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
                request.answer_list.description,
                patentability_criteria[i],
            )
            report[patentability_criteria[i]] = assessment
            print(f"Assessment for {patentability_criteria[i]}: {assessment}")

        return report

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
