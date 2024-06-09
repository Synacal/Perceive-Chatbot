from fastapi import HTTPException
from typing import List, Dict
from app.core.database import get_percieve_db_connection
from app.core.azure_client import client

from app.services.ip_validity_analysis.novelty import compare_novelty
from app.services.ip_validity_analysis.non_obviousness import compare_non_obviousness
from app.services.ip_validity_analysis.utility import compare_utility
from app.services.ip_validity_analysis.enablement import compare_enablement
from app.services.ip_validity_analysis.written_description import (
    compare_written_description,
)
from app.services.ip_validity_analysis.definiteness import compare_definiteness
from app.services.ip_validity_analysis.industrial_application import (
    compare_industrial_application,
)
from app.services.ip_validity_analysis.clarity_and_sufficiency import (
    compare_clarity_and_sufficiency,
)
from app.services.ip_validity_analysis.scope_and_definition import (
    compare_scope_and_definition,
)
from app.services.ip_validity_analysis.economic_significance import (
    compare_economic_significance,
)
from app.models.ip_validity_analysis import (
    PatentAnalysis,
    PatentResult,
    PatentList,
    SearchQuery,
)
from psycopg2 import sql
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.prior_art_search_helpers import (
    vectorize_description,
)
import time
import numpy as np


async def search_documents(query: SearchQuery) -> List[PatentResult]:
    try:
        conn = get_percieve_db_connection()
        query_keywords = " | ".join(query.keywords)
        ts_query = sql.SQL("plainto_tsquery('english', %s)")

        query = sql.SQL(
            """
            SELECT id, title, COALESCE(abstract, ''), claim_text
            FROM target.patents
            WHERE ((title_abstract_tsvector @@ {ts_query} AND title IS NOT NULL AND title != '' AND abstract IS NOT NULL AND abstract != '' AND claim_text IS NOT NULL AND claim_text != '')
            OR (claims_tsvector @@ {ts_query} AND title IS NOT NULL AND title != '' AND abstract IS NOT NULL AND abstract != '' AND claim_text IS NOT NULL AND claim_text != ''));
            """
        ).format(ts_query=ts_query)

        with conn.cursor() as cur:
            cur.execute(query, [query_keywords, query_keywords])
            results = cur.fetchall()

            if not results:
                print("No patents found.")
                return []

            patents = []
            for row in results:
                try:
                    id_, title, abstract, content = row[:4]
                    patents.append(
                        PatentResult(
                            id=id_,
                            title=title,
                            abstract=abstract,  # Use COALESCE to handle NULL or empty abstract values
                            content=content,
                        )
                    )
                except Exception as e:
                    print(f"Error processing row: {row}")
                    print(f"Error details: {e}")
                    continue

            return patents
    except Exception as e:
        print(f"Error executing search query: {e}")
        raise HTTPException(status_code=500, detail="Error executing search query")
    finally:
        conn.close()


def encode_texts(texts: List[str]) -> List[List[float]]:
    print("Starting encoding process...")
    embeddings = vectorize_texts(texts)
    print("Encoding process completed.")
    return embeddings


def vectorize_texts(texts: List[str]):
    embeddings = []
    for text in texts:
        embedding = vectorize_description(text)
        print(f"Vectorized text ")
        embeddings.append(embedding)
        # Add a 10 second delay
        time.sleep(10)
    return embeddings


async def search_patents(patents: List[PatentResult], description: str) -> PatentList:
    patent_texts = [f"{patent.abstract} " for patent in patents]
    print("Patent texts: ", patent_texts)

    # Ensure that you await the results of the asynchronous tasks
    description_embedding_task = encode_texts([description])
    patent_embeddings_task = vectorize_texts(patent_texts)

    description_embedding = description_embedding_task
    patent_embeddings = patent_embeddings_task

    # description_embedding = np.array(description_embedding[0])
    # patent_embeddings = np.array(patent_embeddings)

    # Convert lists to NumPy arrays
    description_embedding = np.array(description_embedding).reshape(1, -1)
    patent_embeddings = np.array(patent_embeddings)

    # Ensure patent_embeddings are reshaped correctly
    if len(patent_embeddings.shape) == 1:
        patent_embeddings = patent_embeddings.reshape(1, -1)

    # Compute cosine similarity
    similarities = cosine_similarity(description_embedding, patent_embeddings)

    # Print similarities for each patent
    similarity_dict: Dict[str, float] = {}
    for i, patent in enumerate(patents):
        similarity = similarities[0][i]
        similarity_dict[patent.id] = similarity
        print(f"Similarity with patent {patent.id}: {similarity}")

    # Sort the similarities and get the top 10 most similar patent IDs
    sorted_similarities = sorted(
        similarity_dict.items(), key=lambda item: item[1], reverse=True
    )
    top_10_patent_ids = [patent_id for patent_id, _ in sorted_similarities[:5]]

    return top_10_patent_ids


async def create_assessment(patent_ids: List[str], answer_list: str, criterion: str):
    patent_abstracts = []

    print("Patent IDs: ", patent_ids)
    for patent_id in patent_ids:
        patent = await get_patent_by_id(patent_id)
        if patent:
            patent_abstracts.append(patent)
            print(f"Patent {patent_id} abstract: {patent}")
    if not patent_abstracts:
        raise HTTPException(
            status_code=404, detail="No patent abstracts found for the provided IDs."
        )

    if criterion == "Novelty (35 U.S.C. § 102)":
        assessment_point = await compare_novelty(patent_abstracts, answer_list)
    elif criterion == "Non-Obviousness (35 U.S.C. § 103)":
        assessment_point = await compare_non_obviousness(patent_abstracts, answer_list)
    elif criterion == "Utility (35 U.S.C. § 101)":
        assessment_point = await compare_utility(patent_abstracts, answer_list)
    elif criterion == "Enablement (35 U.S.C. § 112(a))":
        assessment_point = await compare_enablement(patent_abstracts, answer_list)
    elif criterion == "Written Description (35 U.S.C. § 112(a))":
        assessment_point = await compare_written_description(
            patent_abstracts, answer_list
        )
    elif criterion == "Definiteness (35 U.S.C. § 112(b))":
        assessment_point = await compare_definiteness(patent_abstracts, answer_list)
    elif criterion == "Industrial Application":
        assessment_point = await compare_industrial_application(
            patent_abstracts, answer_list
        )
    elif criterion == "Clarity & Sufficiency":
        assessment_point = await compare_clarity_and_sufficiency(
            patent_abstracts, answer_list
        )
    elif criterion == "Scope & Definition":
        assessment_point = await compare_scope_and_definition(
            patent_abstracts, answer_list
        )
    elif criterion == "Economic Significance":
        assessment_point = await compare_economic_significance(
            patent_abstracts, answer_list
        )

    return assessment_point


async def get_patent_by_id(patent_id: str):
    query = """
    SELECT abstract
    FROM target.patents
    WHERE id = %s;
    """
    value = patent_id
    try:
        conn = get_percieve_db_connection()

        with conn.cursor() as cur:
            cur.execute(query, [value])
            result = cur.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error fetching patent {patent_id}: {e}")
        return None
    finally:
        conn.close()
