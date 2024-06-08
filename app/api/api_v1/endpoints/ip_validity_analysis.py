from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.prior_art_search import (
    PatentAnalysis,
    PatentList,
    SearchRequest,
)

# from app.models.document import Document  # Assuming Document is a Pydantic model for your database entries
from app.services.ip_validity_analysis import (
    search_documents,
    search_patents,
    create_novelty_assessment,
)

from app.services.ip_validity_analysis.common import (
    create_assessment,
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
        novelly_assessment = await create_novelty_assessment(
            response_data2, request.answer_list.description
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
        ]
        non_obviousness = await create_assessment(
            response_data2,
            request.answer_list.description,
            patentability_criteria[1],
        )
        if novelly_assessment is None:
            raise HTTPException(
                status_code=500, detail="Error generating novelty assessment."
            )

        # Ensure that the novelty_assessment matches the expected return type
        return novelly_assessment
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
