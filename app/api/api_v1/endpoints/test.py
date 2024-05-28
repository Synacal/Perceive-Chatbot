from fastapi import APIRouter, HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
import psycopg2
from typing import List
from pydantic import BaseModel
from app.core.database import get_percieve_db_connection
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the router
router = APIRouter()


# Define the search request model
class SearchRequest(BaseModel):
    description: str


# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer()


# Function to escape special characters for tsquery
def escape_tsquery(query):
    return (
        query.replace("'", "''")
        .replace("&", "\&")
        .replace("|", "\|")
        .replace("!", "\!")
        .replace("(", "\(")
        .replace(")", "\)")
    )


# Function to fetch relevant abstracts based on keyword search
def fetch_relevant_abstracts(keywords):
    conn = get_percieve_db_connection()
    cur = conn.cursor()

    # Prepare keywords for to_tsquery
    individual_terms = [term for keyword in keywords for term in keyword.split()]
    escaped_terms = [escape_tsquery(term) for term in individual_terms]
    formatted_keywords = " | ".join(escaped_terms)

    query = f"""
        SELECT id, abstract, ts_rank_cd(title_abstract_tsvector, to_tsquery('english', %s)) AS rank
        FROM target.patents
        WHERE title_abstract_tsvector @@ to_tsquery('english', %s)
        ORDER BY rank DESC
        LIMIT 100  -- Limiting to improve performance
    """
    logger.info(f"Executing query: {query} with keywords: {formatted_keywords}")
    cur.execute(query, (formatted_keywords, formatted_keywords))

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


# Function to preprocess and check abstracts
def preprocess_abstracts(abstracts):
    cleaned_abstracts = [abstract for abstract in abstracts if abstract.strip()]
    logger.info(
        f"Fetched {len(abstracts)} abstracts, {len(cleaned_abstracts)} after cleaning."
    )
    if not cleaned_abstracts:
        raise ValueError("All abstracts are empty after preprocessing.")
    return cleaned_abstracts


@router.post("/test")
async def test(request: SearchRequest):
    try:
        new_description = request.description

        # Extract keywords from the new description
        keywords = [
            "low-power consumption",
            "high-speed data processing",
            "power management",
        ]

        # Fetch relevant abstracts based on keyword search
        relevant_abstracts = fetch_relevant_abstracts(keywords)

        if not relevant_abstracts:
            logger.info("No relevant abstracts found.")
            raise HTTPException(status_code=404, detail="No relevant abstracts found.")

        # Extract the abstracts
        abstracts_for_vectorizer = [row[1] for row in relevant_abstracts]
        logger.info(f"Abstracts fetched from the database: {abstracts_for_vectorizer}")

        # Preprocess abstracts to ensure they are not empty
        cleaned_abstracts = preprocess_abstracts(abstracts_for_vectorizer)

        # Fit the vectorizer with relevant abstracts
        vectorizer.fit(cleaned_abstracts)

        # Transform the new description
        new_vector = vectorizer.transform([new_description]).toarray().tolist()[0]

        print(f"Transformed vector: {new_vector}")

        # Perform similarity search using the transformed vector
        conn = get_percieve_db_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, abstract, 1 - (abstract_vector <=> %s) AS similarity
            FROM target.patents
            ORDER BY abstract_vector <=> %s
            LIMIT 20
            """,
            (new_vector, new_vector),
        )

        results = cur.fetchall()
        cur.close()
        conn.close()

        return [
            {"id": result[0], "abstract": result[1], "similarity": result[2]}
            for result in results
        ]
    except HTTPException as e:
        logger.error(f"HTTP error occurred: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
