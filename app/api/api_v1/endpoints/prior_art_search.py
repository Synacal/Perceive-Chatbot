from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.prior_art_search import SearchQuery, PatentAnalysis
# from app.models.document import Document  # Assuming Document is a Pydantic model for your database entries
from app.services.prior_art_search import search_documents, search_patents

router = APIRouter()

@router.post("/keyword-search")
async def keyword_search(query: SearchQuery):
    try:
        response_data = await search_documents(query)
        return response_data
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