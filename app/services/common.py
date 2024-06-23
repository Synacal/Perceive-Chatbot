from fastapi import HTTPException, Depends
from app.core.database import get_db_connection, get_database_connection
from app.models.common import Draft
from psycopg2.extras import execute_values
import psycopg2.extras
import json
from app.models.common import Draft
from app.core.azure_client import client


async def add_draft(draft_data: Draft):
    query = """
        INSERT INTO draft (requirement_gathering_id, user_id, other_data, current_page)
        VALUES %s
        ON CONFLICT (requirement_gathering_id, user_id)
        DO UPDATE SET
            other_data = EXCLUDED.other_data,
            current_page = EXCLUDED.current_page
        """
    # Convert other_data to a JSON string
    other_data_str = json.dumps(draft_data.other_data)

    values = [
        (
            draft_data.requirement_gathering_id,
            draft_data.user_id,
            other_data_str,
            draft_data.current_page,
        )
    ]

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        execute_values(cur, query, values)
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


async def get_drafts_by_user_id(UserID: str):
    query = """
        SELECT * FROM draft WHERE user_id = %s  """
    values = (UserID,)
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, values)
        result = cur.fetchall()
        answer = []
        for row in result:
            other_data = row["other_data"]
            if isinstance(other_data, str):
                other_data = json.loads(other_data)
            answer.append(
                Draft(
                    requirement_gathering_id=row["requirement_gathering_id"],
                    user_id=row["user_id"],
                    current_page=row["current_page"],
                    other_data=other_data,
                )
            )
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


async def get_draft_by_ids(UserID: str, requirement_gathering_id: int):
    query = """
        SELECT * FROM draft WHERE user_id = %s AND requirement_gathering_id = %s
        """
    values = (UserID, requirement_gathering_id)
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, values)
        result = cur.fetchall()
        answer = []
        for row in result:
            other_data = row["other_data"]
            if isinstance(other_data, str):
                other_data = json.loads(other_data)
            answer.append(
                Draft(
                    requirement_gathering_id=row["requirement_gathering_id"],
                    user_id=row["user_id"],
                    current_page=row["current_page"],
                    other_data=other_data,
                )
            )

        return answer

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


async def delete_draft_by_ids(UserID: str, requirement_gathering_id: int):
    query = """
        DELETE FROM draft WHERE user_id = %s AND requirement_gathering_id = %s
        """
    values = (UserID, requirement_gathering_id)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


async def get_report_by_user_id(UserID: str):
    query = """
        SELECT rg.requirement_gathering_id, rg.user_id, 
               d.current_page, d.other_data,
               r.user_case_id, r.report
        FROM requirements_gathering AS rg
        JOIN reports AS r ON r.requirement_gathering_id = rg.requirement_gathering_id
        LEFT JOIN draft AS d ON rg.requirement_gathering_id = d.requirement_gathering_id
        WHERE rg.user_id = %s
        """
    values = (UserID,)
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, values)
        result = cur.fetchall()

        # Convert result to list of dictionaries
        json_result = [dict(row) for row in result]
        return json_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


async def get_report_id(requirement_gathering_id, category_id):
    query = """
    SELECT report_id FROM requirements_gathering WHERE requirement_gathering_id = %s AND user_case_id = %s
    """
    values = (
        requirement_gathering_id,
        str(category_id),
    )
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        report_id = cur.fetchone()[0]
        cur.close()
        return report_id
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_answers_with_questions(requirement_gathering_id, use_case_id):
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
            # Determine question_ids based on use_case_id
            if use_case_id == "1" or use_case_id == "2":
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
            elif use_case_id == "3":
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
            elif use_case_id == "4":
                question_ids = ["27", "28", "29", "30", "31", "32", "33", "34", "35"]
            elif use_case_id == "5":
                question_ids = ["36", "37", "38", "39", "40", "41", "42"]
            elif use_case_id == "6":
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
            elif use_case_id == "7":
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
            elif use_case_id == "8":
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
            elif use_case_id == "9":
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
            elif use_case_id == "10":
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

            report_id = await get_report_id(requirement_gathering_id, use_case_id)
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
            return []
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


async def get_summary_data(qa_pairs):
    prompt = f"""
    Summarize the key points of an innovation based on the following details. 
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

    return content


async def get_completion_precentage(requirement_gathering_id):
    QA_Count = """
    SELECT COUNT(DISTINCT question_id) FROM user_chats WHERE requirement_gathering_id = %s AND question_id IN %s
    """
    Attachment_Count = """
    SELECT COUNT(DISTINCT question_id) FROM attachment_chats WHERE requirement_gathering_id = %s AND question_id IN %s
    """
    use_case_query = """
    SELECT user_case_id FROM requirements_gathering WHERE requirement_gathering_id = %s
    """
    use_case_values = (requirement_gathering_id,)
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(use_case_query, (requirement_gathering_id,))
        use_case_ids = cur.fetchall()

        total_questions_possible = 0
        total_answered_questions = 0

        for use_case_id_tuple in use_case_ids:
            use_case_id = use_case_id_tuple[0]

            question_ids = get_questions_ids(use_case_id)
            question_ids_tuple = tuple(question_ids)

            cur.execute(
                Attachment_Count, (requirement_gathering_id, question_ids_tuple)
            )
            Attachment_count = cur.fetchone()[0]
            total_answered_questions += Attachment_count

            cur.execute(QA_Count, (requirement_gathering_id, question_ids_tuple))
            QA_count = cur.fetchone()[0]
            total_answered_questions += QA_count

            if use_case_id in ["1", "2"]:
                total_questions_possible += 10
            elif use_case_id == "3":
                total_questions_possible += 13
            elif use_case_id == "4":
                total_questions_possible += 9
            elif use_case_id == "5":
                total_questions_possible += 7
            elif use_case_id == "6":
                total_questions_possible += 16
            elif use_case_id == "7":
                total_questions_possible += 10
            elif use_case_id == "8":
                total_questions_possible += 15
            elif use_case_id == "9":
                total_questions_possible += 12
            elif use_case_id == "10":
                total_questions_possible += 13
            else:
                total_questions_possible += 3

        completion_percentage = (
            (total_answered_questions / total_questions_possible) * 100
            if total_questions_possible > 0
            else 0
        )
        if completion_percentage > 100:
            completion_percentage = 100

        completion_percentage = int(completion_percentage)

        return {"completion_percentage": completion_percentage}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_questions_ids(use_case_id):
    if use_case_id == "1" or use_case_id == "2":
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
    elif use_case_id == "3":
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
    elif use_case_id == "4":
        question_ids = ["27", "28", "29", "30", "31", "32", "33", "34", "35"]
    elif use_case_id == "5":
        question_ids = ["36", "37", "38", "39", "40", "41", "42"]
    elif use_case_id == "6":
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
    elif use_case_id == "7":
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
    elif use_case_id == "8":
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
    elif use_case_id == "9":
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
    elif use_case_id == "10":
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
    return question_ids
