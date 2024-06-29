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

import os
import pdfkit


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
            if user_case_id == "1" or user_case_id == "2":
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
            elif user_case_id == "3":
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
            elif user_case_id == "4":
                question_ids = ["26", "27", "28", "29", "30", "31", "32", "33", "34"]
            elif user_case_id == "5":
                question_ids = ["35", "36", "37", "38", "39", "40", "41"]
            elif user_case_id == "6":
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
            elif user_case_id == "7":
                question_ids = [
                    "0",
                    "1",
                    "2",
                    "3",
                    "55",
                    "56",
                    "57",
                    "58",
                    "59",
                    "60",
                ]
            elif user_case_id == "8":
                question_ids = [
                    "0",
                    "1",
                    "2",
                    "3",
                    "61",
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
                ]
            elif user_case_id == "9":
                question_ids = [
                    "0",
                    "1",
                    "2",
                    "3",
                    "72",
                    "73",
                    "74",
                    "75",
                    "76",
                    "77",
                    "78",
                    "79",
                ]
            elif user_case_id == "10":
                question_ids = [
                    "0",
                    "1",
                    "2",
                    "3",
                    "80",
                    "81",
                    "82",
                    "83",
                    "84",
                    "85",
                    "86",
                    "87",
                    "88",
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
            raise HTTPException(
                status_code=500, detail="Details are not relevant for report creation."
            )
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


async def search_patents_prior(
    patents: List[PatentResult], description: str
) -> PatentList:
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


async def get_patent_details_by_id(patent_id: str):
    query = """
    SELECT id, date, title, abstract, published_country,kind,wipo_kind,claim_text
    FROM target.patents
    WHERE id = %s;
    """
    value = patent_id
    try:
        conn = get_percieve_db_connection()

        with conn.cursor() as cur:
            cur.execute(query, [value])
            result = cur.fetchone()
            if result:
                kind = (
                    result[5]
                    if result[5] is not None
                    else (result[6] if result[6] is not None else "")
                )
                country = result[4] if result[4] is not None else ""
                patent_details = {
                    "id": result[0],
                    "date": result[1],
                    "title": result[2],
                    "abstract": result[3],
                    "published_country": country,
                    "kind": kind,
                    "claims": result[6],
                }
                return patent_details
            else:
                return None
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
        patent_ids = await search_patents_prior(response_data, summary)
        analysed_patent_reports = ["## Relevant Patents\n\n"]
        all_patents_info = []

        for patent_id in patent_ids:
            print(patent_id)
            # patent = await get_patent_by_id(patent_id)
            patent = await get_patent_details_by_id(patent_id)
            if patent:
                patent_info = f"""
                Patent ID: {patent['id']}
                Date: {patent['date']}
                Published Country: {patent['published_country']}
                Title: {patent['title']}
                Abstract: {patent['abstract']}
                Kind: {patent['kind']}
                Claims: {patent['claims']}
                """
                all_patents_info.append(patent_info)
                relevancyReport = await getRelevantPatentDetails(summary, patent_info)
                relevancyReport = relevancyReport + os.linesep
                analysed_patent_reports.append(relevancyReport)

        analysed_patent_reports_str = "\n\n".join(analysed_patent_reports)
        # Concatenate all patent information into a single string
        patents_info_str = "\n\n".join(all_patents_info)
        report_intro = await getIntro_KeyFindings(summary, patents_info_str)
        report_conclusion = await getAnalysis_Conclusion(summary, patents_info_str)
        complete_report = (
            report_intro
            + "\n\n"
            + analysed_patent_reports_str
            + "\n\n"
            + report_conclusion
        )

        exportPdf(complete_report)
        response = {
            "summary": summary,
            "status": "in-progress",
            "analysis_results": complete_report,
        }

        str_analysis_results = str(complete_report)
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


async def getIntro_KeyFindings(userPatentSummary, patentInfo):
    system_prompt_intro_key_findings = f"""
            Conduct a Prior Art Search focusing on the following aspects:

            Key Findings:

            Provide a summary of significant prior art that could affect the technology’s patentability, including the number and relevance of found patents, and implications for the novelty of the technology.
            Focus on patents that are not owned by "User's Invention".
            Ensure the report reflects accurate background information and demonstrates the utility of the analysis.
            Output Requirements:

            The report should be insightful, highly accurate, and name specific patents.
            Structure the findings in a logical format with clear headings and subheadings.
            Background Information of "User's Invention":
                {userPatentSummary}
                
            Patent Information to Analyze: {patentInfo}

            Report should be in markdown format which can be converted to html and pdf

            Below is the structure of the report:
                # Prior Art Search Report: "Invention Name" - (This is Title)
                  ##  Introduction (h2)
                  ##  Key Findings (h2)

            Provide only the Introduction and a brief paragraph summarizing the Key Findings. Do not include detailed patent analysis.

            Give response in markdown format, make sure to follow the given structure and put Title and all headings in markdown heading formats.
            """
    message_text = [
        {"role": "system", "content": system_prompt_intro_key_findings},
        # {"role": "user", "content": answer}
    ]
    completion = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=message_text,
        temperature=0.7,
        max_tokens=2000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    response = completion.choices[0].message.content
    return response


async def getRelevantPatentDetails(userPatentSummary, patentInfo):
    prompt = f"""
            Analyze the given patent details in relation to the provided "User Patent" summary. Extract the "User Patent" name from the summary and use it throughout the response instead of the placeholder "User Patent". Follow the structure below to ensure comprehensive analysis:

            Do not include the User Patent Summary in the response.

            ### User Patent Summary:
            {userPatentSummary}

            ### Given Patent Details to Analyze:
            {patentInfo}

            ### Output Structure:
            ### [Patent ID Number]
            - **Publication Date:** [Date]
            - **Summary:** [summary of the given patent]
            - **Relevance:** [relevance of the given patent to "User Patent"]
            - **Potential Impact:** [potential impact on "User Patent" from the given patent]

            Do not include any User Patent Summary or analysis other than given structure. stick to the output structure provided.
            Make sure to replace "User Patent" with actual name of the output.

            Provide the response in markdown format.
        """
    message_text = [
        {"role": "system", "content": prompt},
        # {"role": "user", "content": answer}
    ]
    completion = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=message_text,
        temperature=0.7,
        max_tokens=2000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    response = completion.choices[0].message.content
    return response


async def getAnalysis_Conclusion(userPatentSummary, patentInfo):
    system_prompt_analysis_conclusion = f"""
                Conduct a detailed analysis focusing on the following aspects:

                Key Aspects:

                1. Novelty and Patentability
                2. Impact on the invention described in the summary
                3. Conclusion

                Provide a clear and insightful analysis for each aspect. Focus on summarizing primary concerns, necessary actions, and strategic implications for the invention described in the summary. Ensure the report reflects accurate background information and demonstrates the utility of the analysis.

                Output Requirements:

                The report should be insightful, highly accurate, and name specific patents.
                Structure the findings in a logical format with clear headings and subheadings.
                Include detailed recommendations and strategic implications in the context of novelty, patentability, and market strategy.

                Background Information of the User Patent:
                    {userPatentSummary}
                    
                Patent Information to Analyze: {patentInfo}

                Report should be in markdown format which can be converted to html and pdf.

                Below is the structure of the report:
                    ## Analysis and Implications (h2)
                       ### Novelty and Patentability (h3)
                       ### Impact on the "User Patent" (h3)
                    ## Conclusion (h2)

                Provide detailed content for the "Analysis and Implications" and "Conclusion" sections based on the above structure. Do not include the title or introduction in the response.

                Make sure to replace "User Patent" with actual name of the output. you have to extract the name of the "User Patent" from the Background Information of the User Patent.

                Give response in markdown format, make sure to follow the given structure and put all headings in markdown heading formats.
                """

    message_text = [
        {"role": "system", "content": system_prompt_analysis_conclusion},
        # {"role": "user", "content": answer}
    ]
    completion = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=message_text,
        temperature=0.7,
        max_tokens=2000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    response = completion.choices[0].message.content
    return response


"""

def exportPdf(text):

    if isinstance(text, list):
        text = "\n".join(text)
    elif not isinstance(text, str):
        raise TypeError("The input text must be a string or a list of strings")

    html_text = markdown2.markdown(text)

    output_dir = "temp_report"
    print(os.path)
    output_pdf_path = os.path.join(output_dir, "report.pdf")
    print(output_pdf_path)

    # Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    html_file_path = os.path.join(output_dir, "output.html")
    with open(html_file_path, "w") as html_file:
        html_file.write(html_text)

    path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Update this path based on your installation

    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    pdfkit.from_string(html_text, output_pdf_path, configuration=config)
    print(f"PDF file has been created successfully at {output_pdf_path}.")

"""
# markdown_text = """
# # Sample Markdown

# This is a sample markdown text.

# ## Subheading

# - List item 1
# - List item 2

# **Bold text**

# [Link](https://example.com)
# """
# exportPdf(markdown_text)
