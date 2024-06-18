from fastapi import BackgroundTasks, APIRouter, HTTPException, Depends
from typing import List
from app.services.get_answers import get_all_answers_with_questions
from app.models.prior_art_search import (
    SearchQuery,
    PatentAnalysis,
    PriorArtSearch,
    ReportParams,
)

# from app.models.document import Document  # Assuming Document is a Pydantic model for your database entries
from app.services.prior_art_search2 import (
    generate_innovation_summary,
)
from app.services.prior_art_search.common import (
    get_answers,
    get_answers_with_questions,
    generate_prior_art_summary,
    get_keywords,
    search_documents,
    search_patents,
    get_patent_by_id,
    create_report_background,
)

from app.core.azure_client import client

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

"""
@router.post("/prior-art-search-temp")
async def prior_art_search_temp(query: PriorArtSearch):
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

@router.post("/prior-art-search")
async def prior_art_search(report_params: ReportParams):
    try:
        answers = await get_answers_with_questions(
            report_params.requirement_gathering_id, report_params.use_case_id
        )

        summary = generate_prior_art_summary(answers)

        keywords = await get_keywords(answers)

        response_data = await search_documents(keywords)

        response_data = response_data[:3]
        patent_ids = await search_patents(response_data, summary)
        analysis_results = []
        print("12")
        for patent_id in patent_ids:
            print(patent_id)
            patent = await get_patent_by_id(patent_id)
            system_prompt = f
                Analyze the provided patent information against the user's invention description to identify and 
                describe both similarities and differences, focusing on technical features, innovative aspects, 
                and potential patentability issues.
                Inputs:

                User's Invention Description: {summary}

                Patent Information to Analyze: {patent}

                Analysis Tasks:

                    Task 1: Identify Similarities:
                        Prompt: "Given the abstract and claims of Patent X (details provided above) alongside the 
                        description of the user's invention, identify and describe the key similarities. Focus on 
                        technical features, shared functionalities, and overlapping application domains. Explain 
                        how these similarities could impact the patentability of the user’s invention."
                    Task 2: Identify Differences:
                        Prompt: "Based on the provided patent information (Patent X) and the user's invention 
                        description, identify and articulate the significant differences, particularly regarding 
                        novel features and inventive steps. Describe how these differences enhance the uniqueness 
                        of the user's invention and contribute to its patentability. Outline any new functionalities, 
                        technical solutions, or applications that differentiate the user's invention from the patent."

                Output:

                    Format for Response:
                        Similarities:
                            A detailed list and explanation of elements or concepts that are similar between the analyzed patent and the user's invention. Include any shared technological approaches or functionalities.
                        Differences:
                            A comprehensive outline of how the user's invention diverges from the analyzed patent. Highlight novel features, different technical solutions, or unique applications that are not covered by the patent.
                        Conclude with a brief summary of the potential implications of these similarities and differences on the user’s ability to patent the invention.
                
            message_text = [
                {"role": "system", "content": system_prompt},
                # {"role": "user", "content": answer}
            ]
            completion = client.chat.completions.create(
                model="gpt-35-turbo",
                messages=message_text,
                temperature=0.7,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
            )
            print("13")
            content = completion.choices[0].message.content
            print("14")
            analysis_results.append(content)
            print("15")

        response = {
            "summary": summary,
            "status": "in-progress",
            "analysis_results": analysis_results,
        }
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""


@router.post("/prior-art-search")
async def prior_art_search(
    report_params: ReportParams, background_tasks: BackgroundTasks
):
    try:
        # Start the background task for report creation
        background_tasks.add_task(create_report_background, report_params)
        answers = await get_answers_with_questions(
            report_params.requirement_gathering_id, report_params.use_case_id
        )

        summary = generate_prior_art_summary(answers)
        # Return summary and status as "in progress" immediately
        response = {"summary": summary, "status": "in-progress"}
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
