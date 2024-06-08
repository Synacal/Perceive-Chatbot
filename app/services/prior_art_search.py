from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.prior_art_search import SearchQuery

# from app.models.document import Document  # Assuming Document is a Pydantic model for your database entries
from app.core.database import get_percieve_db_connection
from psycopg2 import sql
from app.models.prior_art_search import PatentAnalysis, PatentResult
from app.utils.prior_art_search_helpers import vectorize_description, generate_analysis
from app.core.azure_client import client


async def search_documents(query: SearchQuery):
    try:
        conn = get_percieve_db_connection()
        # Properly split and prepare the keywords for the tsquery
        # Using ' & ' for AND logic in full-text search to ensure broader results
        query_keywords = " | ".join(query.keywords)
        ts_query = sql.SQL("plainto_tsquery('english', %s)")

        # Construct the full-text search query using parameterized SQL
        query = sql.SQL(
            """
            SELECT id, title, abstract, claim_text
            FROM target.patents
            WHERE (title_abstract_tsvector @@ {ts_query})
               OR (claims_tsvector @@ {ts_query});
        """
        ).format(ts_query=ts_query)
        # print(query)
        # Execute the query
        with conn.cursor() as cur:
            cur.execute(query, [query_keywords, query_keywords])
            results = cur.fetchall()
            return results
    except Exception as e:
        print(f"Error executing search query: {e}")
        return []


async def search_patents(data: PatentAnalysis):
    description_vector = vectorize_description(data.description)
    query_results = query_pinecone_index(description_vector)
    results = []

    for match in query_results["matches"]:
        patent_id = match["metadata"]["id"]
        title = match["metadata"]["title"]
        abstract = match["metadata"]["abstract"]
        content = generate_analysis(data.description, match["metadata"])
        results.append(
            PatentResult(id=patent_id, title=title, abstract=abstract, content=content)
        )
    return results


def generate_innovation_summary(qa_pairs):
    """
    Generates a summary of the user's innovation using Azure AI based on provided question and answer pairs.

    Parameters:
    - qa_pairs (list of dicts): A list of dictionaries containing 'question' and 'answer' keys.

    Returns:
    - str: A summary of the innovation.
    """
    # Create a single string from all question-answer pairs
    prompt = f"""Summarize the key points of an innovation based on the following details. 
    Following details are on user's responses from the database for the predefined set 
    of questions relevant to their innovation.
    - Summarize the product or technology that has been developed, emphasizing its purpose and target industry.
    - Describe in detail the technical aspects and the unique features of the innovation. Highlight how these features contribute to novelty within its field.
    - Explain the innovation's business model, focusing on primary and potential revenue streams.
    - Outline the company’s strategy for patent filing, including geographic focus and any prior art or existing patents that have been identified.
    - Discuss how the innovation meets the criteria for novelty and non-obviousness, which are crucial for IP validity

    User provided answers for set of pre-defined questions: 
    {qa_pairs}
    
    """

    message_text = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": str(qa_pairs)},
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

    content = completion.choices[0].message.content

    # Extract the generated text from the response
    # summary = response.get("choices", [{}])[0].get("text", "").strip()

    return content
