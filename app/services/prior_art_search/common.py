from fastapi import HTTPException
from typing import List, Dict
from app.core.database import get_percieve_db_connection
from app.core.azure_client import client
from psycopg2 import sql
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.prior_art_search_helpers import (
    vectorize_description,
    vectorize_description_with_retries,
)

import time
import numpy as np
from app.services.add_attachment_answer import get_report_id
from app.core.database import get_db_connection
import json

from app.models.prior_art_search import PatentResult, PatentList, ReportParams


async def get_answers(requirement_gathering_id, user_case_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if requirement_gathering_id exists in user_chats
        query_user_chats = """
        SELECT COUNT(*)
        FROM user_chats
        WHERE requirement_gathering_id = %s;
        """

        print("1")
        cur.execute(query_user_chats, (requirement_gathering_id,))
        user_chats_count = cur.fetchone()[0]

        # Check if requirement_gathering_id exists in attachment_chats
        query_attachment_chats = """
        SELECT COUNT(*)
        FROM attachment_chats
        WHERE requirement_gathering_id = %s;
        """
        cur.execute(query_attachment_chats, (requirement_gathering_id,))
        attachment_chats_count = cur.fetchone()[0]

        if user_chats_count > 0:

            question_ids = []
            # Determine question_ids based on user_case_id
            if user_case_id == "1":
                question_ids = [
                    "0",
                    "1",
                    "2",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                ]
            elif user_case_id == "2":
                question_ids = [
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                ]
            elif user_case_id == "3":
                question_ids = ["26", "27", "28", "29", "30", "31", "32", "33", "34"]
            elif user_case_id == "4":
                question_ids = ["35", "36", "37", "38", "39", "40", "41"]
            elif user_case_id == "5":
                question_ids = [
                    "0",
                    "1",
                    "2",
                    "42",
                    "43",
                    "44",
                    "45",
                    "46",
                    "47",
                    "48",
                    "49",
                    "50",
                    "51",
                    "52",
                    "53",
                    "54",
                ]
            else:
                question_ids = ["0", "1", "2"]
            query = """
            SELECT answer
            FROM user_chats
            WHERE requirement_gathering_id = %s AND question_id IN %s;
            """
            values = (requirement_gathering_id, tuple(question_ids))

        elif attachment_chats_count > 0:

            report_id = await get_report_id(requirement_gathering_id, user_case_id)
            query = """
            SELECT answer
            FROM attachment_chats
            WHERE requirement_gathering_id = %s AND report_id = %s;
            """
            values = (
                requirement_gathering_id,
                report_id,
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid type_id")
        cur.execute(query, values)
        result = cur.fetchall()

        answers = [row[0] for row in result]
        print(f"Number of answers found: {len(answers)}")

        # Combine answers into a single paragraph
        paragraph = " ".join(answers)
        return paragraph
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:  # Ensure conn is closed only if it was successfully opened
            conn.close()


async def get_answers_with_questions(requirement_gathering_id, user_case_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if requirement_gathering_id exists in user_chats
        query_user_chats = """
        SELECT COUNT(*)
        FROM user_chats
        WHERE requirement_gathering_id = %s;
        """

        print("1")
        cur.execute(query_user_chats, (requirement_gathering_id,))
        user_chats_count = cur.fetchone()[0]

        # Check if requirement_gathering_id exists in attachment_chats
        query_attachment_chats = """
        SELECT COUNT(*)
        FROM attachment_chats
        WHERE requirement_gathering_id = %s;
        """
        cur.execute(query_attachment_chats, (requirement_gathering_id,))
        attachment_chats_count = cur.fetchone()[0]

        if user_chats_count > 0:

            question_ids = []
            # Determine question_ids based on user_case_id
            if user_case_id == "1":
                question_ids = [
                    "0",
                    "1",
                    "2",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                ]
            elif user_case_id == "2":
                question_ids = [
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                ]
            elif user_case_id == "3":
                question_ids = ["26", "27", "28", "29", "30", "31", "32", "33", "34"]
            elif user_case_id == "4":
                question_ids = ["35", "36", "37", "38", "39", "40", "41"]
            elif user_case_id == "5":
                question_ids = [
                    "0",
                    "1",
                    "2",
                    "42",
                    "43",
                    "44",
                    "45",
                    "46",
                    "47",
                    "48",
                    "49",
                    "50",
                    "51",
                    "52",
                    "53",
                    "54",
                ]
            else:
                question_ids = ["0", "1", "2"]
            query = """
            SELECT qc.question, uc.answer
            FROM user_chats uc
            JOIN questions qc ON uc.question_id = qc.question_id
            WHERE uc.requirement_gathering_id = %s AND uc.question_id IN %s;
            """
            values = (requirement_gathering_id, tuple(question_ids))

        elif attachment_chats_count > 0:

            report_id = await get_report_id(requirement_gathering_id, user_case_id)
            query = """
            SELECT qc.question,ac.answer
            FROM attachment_chats ac
            JOIN questions qc ON ac.question_id = qc.question_id
            WHERE ac.requirement_gathering_id = %s AND ac.report_id = %s;
            """
            values = (
                requirement_gathering_id,
                report_id,
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid type_id")
        cur.execute(query, values)
        result = cur.fetchall()

        # Correctly construct the list of QA pairs using integer indices
        qa_pairs = [{"question": row[0], "answer": row[1]} for row in result]

        cur.close()
        conn.close()
        return qa_pairs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:  # Ensure conn is closed only if it was successfully opened
            conn.close()


def generate_prior_art_summary(qa_pairs):
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


async def get_keywords(answers):
    system_prompt = f"Extract exactly 2 general product-related keywords from the following text. Ensure these are broad terms like 'satellite' or 'motor' and not specific names, companies, or places. Separate them with a comma: {answers}"
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": system_prompt},
        ]

        completion = client.chat.completions.create(
            model="gpt-35-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )

        content = completion.choices[0].message.content
        print(content)

        # Extract and clean keywords
        if content:
            keywords = [keyword.strip() for keyword in content.split(",") if keyword]
            return keywords
        else:
            return {"status": "No content received"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating response: {str(e)}"
        )


async def search_documents(keywords: List[str]) -> List[PatentResult]:
    try:
        conn = get_percieve_db_connection()
        query_keywords = " | ".join(keywords)
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
            print(f"Number of patents found: {len(patents)}")
            return patents
    except Exception as e:
        print(f"Error executing search query: {e}")
        raise HTTPException(status_code=500, detail="Error executing search query")
    finally:
        conn.close()


def encode_texts(texts: List[str]) -> List[List[float]]:
    embeddings = vectorize_texts(texts)
    print("Encoding summary process completed.")
    return embeddings


def vectorize_texts(texts: List[str]):
    embeddings = []
    for text in texts:
        if not text.strip():  # Check if the text is empty or only contains whitespace
            print(f"Skipping empty text: '{text}'")
            continue
        try:
            print(f"Vectorizing text: {text}")
            embedding = vectorize_description_with_retries(text)
            embeddings.append(embedding)
            print(f"Successfully vectorized text: {text}")
            # Add a 10 second delay
            time.sleep(10)
        except Exception as e:
            print(f"Failed to vectorize text: {text}. Error: {e}")

    return embeddings


async def search_patents(patents: List[PatentResult], description: str) -> PatentList:
    patent_texts = [f"{patent.abstract} " for patent in patents]

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


async def create_report_background(report_params: ReportParams):
    try:
        answers = await get_answers_with_questions(
            report_params.requirement_gathering_id, report_params.user_case_id
        )

        summary = generate_prior_art_summary(answers)

        keywords = await get_keywords(answers)

        response_data = await search_documents(keywords)

        response_data = response_data[:3]
        patent_ids = await search_patents(response_data, summary)
        analysis_results = []

        for patent_id in patent_ids:
            print(patent_id)
            patent = await get_patent_by_id(patent_id)
            system_prompt = f"""
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
                """
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

            content = completion.choices[0].message.content

            analysis_results.append(content)

        response = {
            "summary": summary,
            "status": "in-progress",
            "analysis_results": analysis_results,
        }

        str_analysis_results = str(analysis_results)
        query = """
        INSERT INTO reports (requirement_gathering_id, user_case_id, report)
        VALUES %s
        """
        values = [
            (
                report_params.requirement_gathering_id,
                report_params.user_case_id,
                str_analysis_results,
            )
        ]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()

        print("report generation completed.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
