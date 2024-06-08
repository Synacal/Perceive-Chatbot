from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.services.get_answers import get_answers, get_all_answers_with_questions
from app.models.prior_art_search import SearchQuery, PatentAnalysis, PriorArtSearch

# from app.models.document import Document  # Assuming Document is a Pydantic model for your database entries
from app.services.prior_art_search import (
    search_documents,
    search_patents,
    generate_innovation_summary,
)

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
async def vector_search(query: PatentAnalysis):
    # try:
    response_data = await search_patents(query)
    return response_data


# except HTTPException as e:
#     raise e
# except Exception as e:
#     raise HTTPException(status_code=500, detail=str(e))


@router.post("/prior-art-search")
async def prior_art_search(query: PriorArtSearch):
    # try:
    answers = get_all_answers_with_questions(query.user_id, query.session_id)
    # docs_filtered_by_keywords = await search_documents(query)
    # print(docs_filtered_by_keywords)
    summary = generate_innovation_summary(answers[:10])
    response = {"summary": summary, "status": "in-progress"}
    return response
    # except HTTPException as e:
    #     raise e
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
