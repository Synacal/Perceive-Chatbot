from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.prior_art_search import (
    SearchQuery,
    PatentAnalysis,
    PatentList,
    SearchRequest,
)

# from app.models.document import Document  # Assuming Document is a Pydantic model for your database entries
from app.services.ip_validity_analysis import search_documents, search_patents

router = APIRouter()


@router.post("/ip_validity_analysis", response_model=PatentList)
async def keyword_search(request: SearchRequest):
    try:
        response_data = await search_documents(request.query)
        response_data2 = await search_patents(
            response_data, request.answer_list.description
        )
        return response_data2
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vector-search")
async def keyword_search(query: PatentAnalysis):
    # try:
    response_data = await search_patents(query)
    return response_data


# except HTTPException as e:
#     raise e
# except Exception as e:
#     raise HTTPException(status_code=500, detail=str(e))
