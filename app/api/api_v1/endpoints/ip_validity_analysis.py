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

router = APIRouter()


@router.post("/ip_validity_analysis", response_model=PatentList)
async def keyword_search(request: SearchRequest):
    try:
        response_data = await search_documents(request.query)
        print(len(response_data))
        response_data = response_data[:20]
        response_data2 = await search_patents(
            response_data, request.answer_list.description
        )
        return response_data2
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/novelty-assessment")
async def data_compilation(patent_ids: List[str], answer_list: PatentAnalysis):
    try:
        response_data = await create_novelty_assessment(patent_ids, answer_list)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
