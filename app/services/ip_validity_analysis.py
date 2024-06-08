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
from sklearn.metrics.pairwise import cosine_similarity
import time
from app.core.azure_client import client


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


#
# Load the pre-trained model
# async def encode_texts(texts: List[str]) -> List[List[float]]:
#   loop = asyncio.get_event_loop()
#   embeddings = await loop.run_in_executor(
#       None, lambda: [vectorize_description(text) for text in texts]
#  )
#  return embeddings


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


async def create_novelty_assessment(patent_ids: List[str], answer_list: str):
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

    novelty_point = await compare_novelty(patent_abstracts, answer_list)
    return novelty_point


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


async def compare_novelty(patent_abstracts: List[str], answer_list: str):

    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 40000 // len(patent_abstracts)
    truncated_abstracts = [
        abstract[:max_abstract_length] for abstract in patent_abstracts
    ]

    print("Truncated abstracts: ")

    # Perform novelty assessment
    system_prompt = (
        "Given the following patent abstracts, please provide an analysis of the novelty of the invention described in the patent. "
        "Your analysis should include the following sections:\n"
        "1. Positive Features:\n"
        "    a. Innovative Integration of Technologies:\n"
        "        - Detail any significant engineering achievements that address multiple challenges.\n"
        "    b. Sophisticated Network Management:\n"
        "        - Explain any sophisticated approaches to network management introduced by the invention.\n"
        "    c. Targeted Beamforming Application:\n"
        "        - Describe any complex technical challenges overcome in the development.\n"
        "2. Opinion:\n"
        "    - Provide an opinion on the non-obviousness of the technology, highlighting substantial departures from conventional solutions and creative problem-solving.\n"
        "3. Caveats:\n"
        "    a. Prior Art and Comparative Analysis:\n"
        "        - Note the need to evaluate the inventive step against similar technologies.\n"
        "    b. Technical Documentation and Challenges:\n"
        "        - Suggest documenting specific engineering challenges and solutions.\n"
        "    c. Comparison with Existing Solutions:\n"
        "        - Emphasize the need to show how the technology surpasses existing solutions in solving problems.\n"
        "Additionally, provide a novelty score from 0 to 100, where 0 indicates no novelty and 100 indicates complete novelty."
    )

    message_text = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": answer_list},
    ]

    try:
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

        print("Novelty assessment completion: ")

        content = completion.choices[0].message.content

        # Parse the response into a structured dictionary
        return {"novelty_assessment": content}

    except Exception as e:
        print(f"Error generating novelty assessment: {e}")
        return None
