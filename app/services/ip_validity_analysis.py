from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.prior_art_search import SearchQuery

# from app.models.document import Document  # Assuming Document is a Pydantic model for your database entries
from app.core.database import get_percieve_db_connection
from psycopg2 import sql
from app.models.prior_art_search import PatentAnalysis, PatentResult, PatentList
from app.utils.prior_art_search_helpers import (
    vectorize_description,
    query_pinecone_index,
    generate_analysis,
    vectorize_description_with_retry,
)
import asyncio
import numpy as np
from typing import List, Dict


async def search_documents(query: SearchQuery) -> List[PatentResult]:
    try:
        conn = get_percieve_db_connection()
        query_keywords = " | ".join(query.keywords)
        ts_query = sql.SQL("plainto_tsquery('english', %s)")

        query = sql.SQL(
            """
            SELECT id, title, COALESCE(abstract, ''), claim_text
            FROM target.patents
            WHERE (title_abstract_tsvector @@ {ts_query})
               OR (claims_tsvector @@ {ts_query});
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


#
# Load the pre-trained model
# async def encode_texts(texts: List[str]) -> List[List[float]]:
#   loop = asyncio.get_event_loop()
#   embeddings = await loop.run_in_executor(
#       None, lambda: [vectorize_description(text) for text in texts]
#  )
#  return embeddings


async def vectorize_texts_async(texts: List[str]) -> List[List[float]]:
    return await asyncio.gather(
        *[vectorize_description_with_retry(text) for text in texts]
    )


async def encode_texts(texts: List[str]) -> List[List[float]]:
    print("Starting encoding process...")
    embeddings = await vectorize_texts_async(texts)
    print("Encoding process completed.")
    return embeddings


async def search_patents_temp(
    patents: List[PatentResult], description: str
) -> PatentList:
    patent_texts = [
        f"{patent.title} {patent.abstract} {patent.content}" for patent in patents
    ]
    print("Patent texts: ", patent_texts)

    description_embedding_task = encode_texts([description])
    patent_embeddings_task = encode_texts(patent_texts)

    print("Running tasks...1")
    description_embedding, patent_embeddings = await asyncio.gather(
        description_embedding_task, patent_embeddings_task
    )
    print("Running tasks...2")

    description_embedding = np.array(description_embedding[0])
    patent_embeddings = np.array(patent_embeddings)

    print("Description embedding shape: ", description_embedding.shape)

    similarities = np.dot(patent_embeddings, description_embedding) / (
        np.linalg.norm(patent_embeddings, axis=1)
        * np.linalg.norm(description_embedding)
    )
    print("Similarities: ", similarities)
    top5_indices = np.argsort(similarities)[::-1][:5]

    top5_patents = [patents[idx] for idx in top5_indices]

    return PatentList(patents=top5_patents)


async def search_patents(patents: List[PatentResult], description: str) -> PatentList:
    patent_abstracts = [patent.abstract for patent in patents]

    description_embedding_task = encode_texts([description])
    patent_abstract_embeddings_task = encode_texts(patent_abstracts)

    description_embedding, patent_abstract_embeddings = await asyncio.gather(
        description_embedding_task, patent_abstract_embeddings_task
    )

    description_embedding = np.array(description_embedding[0])
    patent_abstract_embeddings = np.array(patent_abstract_embeddings)

    similarities = np.dot(patent_abstract_embeddings, description_embedding) / (
        np.linalg.norm(patent_abstract_embeddings, axis=1)
        * np.linalg.norm(description_embedding)
    )

    top5_indices = np.argsort(similarities)[::-1][:5]

    top5_patents = [patents[idx] for idx in top5_indices]

    return PatentList(patents=top5_patents)
