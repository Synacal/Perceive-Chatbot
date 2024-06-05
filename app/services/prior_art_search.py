from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.prior_art_search import SearchQuery

# from app.models.document import Document  # Assuming Document is a Pydantic model for your database entries
from app.core.database import get_percieve_db_connection
from psycopg2 import sql
from app.models.prior_art_search import PatentAnalysis, PatentResult
from app.utils.prior_art_search_helpers import (
    vectorize_description,
    query_pinecone_index,
    generate_analysis,
)


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
            SELECT id, title, COALESCE(abstract, ''), claim_text
            FROM target.patents
            WHERE ((title_abstract_tsvector @@ {ts_query} AND title IS NOT NULL AND title != '' AND abstract IS NOT NULL AND abstract != '' AND claim_text IS NOT NULL AND claim_text != '')
            OR (claims_tsvector @@ {ts_query} AND title IS NOT NULL AND title != '' AND abstract IS NOT NULL AND abstract != '' AND claim_text IS NOT NULL AND claim_text != ''));
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
    print(description_vector)
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
