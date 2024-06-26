from fastapi import HTTPException
from typing import List, Dict
from app.core.database import get_percieve_db_connection
from app.core.azure_client import client

from psycopg2 import sql
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.prior_art_search_helpers import (
    vectorize_description,
)
import time
import numpy as np
from app.services.add_attachment_answer import get_report_id
from app.core.database import get_db_connection
import json

from app.models.ip_license_process import PatentResult, PatentList, PatentData

from app.services.ip_license_process.prompt1 import prompt1
from app.services.ip_license_process.prompt2 import prompt2
from app.services.ip_license_process.prompt3 import prompt3
from app.services.ip_license_process.prompt4 import prompt4
from app.services.ip_license_process.prompt5 import prompt5
from app.services.ip_license_process.prompt6 import prompt6


async def search_patents_ids(keywords: List[str]) -> List[int]:
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

            patent_ids = [row[0] for row in results]  # Extracting only the ID

            return patent_ids
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


async def get_answers_license(requirement_gathering_id, user_case_id):
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
            if user_case_id == "1" or user_case_id == "2":
                question_ids = [
                    "1",
                    "2",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                ]
            elif user_case_id == "3":
                question_ids = [
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
                    "26",
                ]
            elif user_case_id == "4":
                question_ids = ["27", "28", "29", "30", "31", "32", "33", "34", "35"]
            elif user_case_id == "5":
                question_ids = ["36", "37", "38", "39", "40", "41", "42"]
            elif user_case_id == "6":
                question_ids = [
                    "1",
                    "2",
                    "3",
                    "4",
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
                    "55",
                ]
            elif user_case_id == "7":
                question_ids = [
                    "1",
                    "2",
                    "3",
                    "4",
                    "56",
                    "57",
                    "58",
                    "59",
                    "60",
                    "61",
                ]
            elif user_case_id == "8":
                question_ids = [
                    "1",
                    "2",
                    "3",
                    "4",
                    "62",
                    "63",
                    "64",
                    "65",
                    "66",
                    "67",
                    "68",
                    "69",
                    "70",
                    "71",
                    "72",
                ]
            elif user_case_id == "9":
                question_ids = [
                    "1",
                    "2",
                    "3",
                    "4",
                    "73",
                    "74",
                    "75",
                    "76",
                    "77",
                    "78",
                    "79",
                    "80",
                ]
            elif user_case_id == "10":
                question_ids = [
                    "1",
                    "2",
                    "3",
                    "4",
                    "81",
                    "82",
                    "83",
                    "84",
                    "85",
                    "86",
                    "87",
                    "88",
                    "89",
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


async def get_summary_license(answers):
    system_prompt = f"Summarize the following text: {answers}"
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": system_prompt},
        ]

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )

        content = completion.choices[0].message.content

        return content
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating response: {str(e)}"
        )


async def get_keywords_license(answers):
    system_prompt = f"Extract exactly 2 general product-related keywords from the following text. Ensure these are broad terms like 'satellite' or 'motor' and not specific names, companies, or places. Separate them with a comma: {answers}"
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": system_prompt},
        ]

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )

        content = completion.choices[0].message.content

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


async def get_patent_data(patents: List[str]) -> List[PatentData]:
    conn = None
    try:
        conn = get_percieve_db_connection()
        cur = conn.cursor()

        query = """
        SELECT
            ah.reel_no,
            ah.frame_no,
            ah.last_update_date,
            ah.recorded_date,
            pae.name AS assignee,
            ARRAY_AGG(pao.name) AS assignors
        FROM
            target.assignment_history AS ah
        JOIN
            target.patent_assignees AS pae ON ah.application_id = pae.application_id
        JOIN
            target.patent_assignors AS pao ON ah.application_id = pao.application_id
        JOIN 
            target.application AS a ON ah.application_id = a.application_id
        WHERE
            a.patent_id = ANY(%s)
        GROUP BY
            ah.reel_no,
            ah.frame_no,
            ah.last_update_date,
            ah.recorded_date,
            pae.name;
        """
        cur.execute(query, (patents,))
        results = cur.fetchall()

        if not results:
            print(f"No results found for patents: {patents}")

        patent_data = []
        for row in results:
            (
                reel_no,
                frame_no,
                last_update_date,
                recorded_date,
                assignee,
                assignors,
            ) = row
            patent_data.append(
                PatentData(
                    reel_no=reel_no,
                    frame_no=frame_no,
                    last_update_date=last_update_date,
                    recorded_date=recorded_date,
                    assignee=assignee,
                    assignors=assignors,
                ).dict()
            )

        print(f"Patent data collected: {patent_data}")
        return patent_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


"""
async def create_report(summary: str, patent_data: List[PatentData]):
    system_prompt = fDevelop an IP Licensing Strategy focusing on the following aspects:

        How to Create an IP Licensing Strategy Leveraging Past History:

        Analyze historical data to identify successful IP licensing strategies.
        Highlight key factors that contributed to the success of past licenses.
        Top Licenses:

        Identify and analyze the top licenses in the orthodontics technology sector.
        Provide insights into why these licenses were successful and how they were structured.
        Top Assignees:

        Identify the top assignees in the orthodontics technology sector.
        Analyze their patent portfolios and licensing activities.
        Top Assignors:

        Identify the top assignors in the orthodontics technology sector.
        Analyze the significance of their contributions and their impact on the market.
        Patent Filings Over Time for Top 5 Assignees:

        Track and analyze the patent filing trends over time for the top 5 assignees.
        Provide visualizations of filing trends and identify any notable patterns or shifts.
        Top Patent Filings:

        Identify the top patent filings that have had significant impacts on the technology sector.
        Provide detailed analyses of these filings and their implications for the market.
        Output Requirements:

        The report should be insightful, highly accurate, and data-centric, naming specific patents and entities.
        Structure the findings in a logical format with clear headings and subheadings.
        Include a section for each relevant entity and patent found, detailing their relevance, potential impact , and implications for market strategy.

        Background Information:{summary}

        Data: {patent_data}
        Note: don't make something vague, make it all clear
        

    message_text = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": str(patent_data),
        },
    ]

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )

        content = completion.choices[0].message.content

        # Parse the response into a structured dictionary if it's in JSON format
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return content
    except Exception as e:
        print(f"Error generating novelty assessment: {e}")
        return None
"""


async def create_report(
    summary: str, patent_data: List[PatentData], license_criteria: str
):
    try:
        if license_criteria == "prompt1":
            license_report = await prompt1(summary, patent_data)
        elif license_criteria == "prompt2":
            license_report = await prompt2(summary, patent_data)
        elif license_criteria == "prompt3":
            license_report = await prompt3(summary, patent_data)
        elif license_criteria == "prompt4":
            license_report = await prompt4(summary, patent_data)
        elif license_criteria == "prompt5":
            license_report = await prompt5(summary, patent_data)
        elif license_criteria == "prompt6":
            license_report = await prompt6(summary, patent_data)
        else:
            pass
        return license_report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
