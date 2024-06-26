from fastapi import BackgroundTasks, HTTPException, Depends
from psycopg2.extras import execute_values
from app.core.database import get_db_connection, get_database_connection

from app.services.ip_validity_analysis.common import (
    create_assessment,
    search_documents,
    search_patents,
    get_keywords,
    add_report,
    get_summary,
    create_word_document,
    create_pdf_document,
    dict_to_formatted_string,
    get_answers,
)

from app.services.ip_license_process.common import (
    get_answers_license,
    get_summary_license,
    get_keywords_license,
    search_patents_ids,
    get_patent_data,
    create_report,
)


async def generate_reports(requirement_gathering_id: int):
    try:
        query_use_cases = """
        SELECT user_case_id FROM requirements_gathering WHERE requirement_gathering_id = %s
        """
        query_use_cases_params = (requirement_gathering_id,)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query_use_cases, query_use_cases_params)
        use_cases = cur.fetchall()
        cur.close()

        if len(use_cases) == 0:
            raise HTTPException(
                status_code=400, detail="Invalid requirement_gathering_id"
            )

        background_tasks = BackgroundTasks()
        for use_case in use_cases:
            background_tasks.add_task(
                generate_report, requirement_gathering_id, use_case[0]
            )

        answers = await get_answers_by_req_id(requirement_gathering_id)
        summary = await get_summary(answers)
        return {"summary": summary, "status": "in progress"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_answers_by_req_id(requirement_gathering_id):
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
            query = """
            SELECT answer
            FROM user_chats
            WHERE requirement_gathering_id = %s;
            """
            values = (requirement_gathering_id,)
        elif attachment_chats_count > 0:
            query = """
            SELECT answer
            FROM attachment_chats
            WHERE requirement_gathering_id = %s;
            """
            values = (requirement_gathering_id,)
        else:
            raise HTTPException(status_code=400, detail="Invalid type_id")
        cur.execute(query, values)
        result = cur.fetchall()

        answers = [row[0] for row in result]

        # Combine answers into a single paragraph
        paragraph = " ".join(answers)
        return paragraph
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


async def generate_report(requirement_gathering_id, user_case_id):
    try:
        if user_case_id == "1":
            await generate_report_1(requirement_gathering_id, user_case_id)
        elif user_case_id == "2":
            await generate_report_2(requirement_gathering_id, user_case_id)
        elif user_case_id == "3":
            await generate_report_3(requirement_gathering_id, user_case_id)
        else:
            pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def generate_report_1(requirement_gathering_id, user_case_id):
    print(f"Generating report for user_case_id {user_case_id}")
    pass


async def generate_report_2(requirement_gathering_id, user_case_id):
    try:
        answers = await get_answers_license(requirement_gathering_id, user_case_id)
        summary = await get_summary_license(answers)
        keywords = await get_keywords_license(answers)
        patents_ids = await search_patents_ids(keywords)
        patent_data = await get_patent_data(patents_ids)

        license_criteria = [
            "prompt1",
            "prompt2",
            "prompt3",
            "prompt4",
            "prompt5",
            "prompt6",
        ]

        report = {}

        for i in range(len(license_criteria)):
            assessment = await create_report(
                summary,
                patent_data,
                license_criteria[i],
            )
            report[license_criteria[i]] = assessment

        # Convert report dictionary to JSON string
        report_str = str(report)

        await create_word_document(
            report_str,
            requirement_gathering_id,
            user_case_id,
        )

        await create_pdf_document(
            report_str,
            requirement_gathering_id,
            user_case_id,
        )

        await add_report(
            report_str,
            requirement_gathering_id,
            user_case_id,
        )
        print("Report generated successfully.")
        return report
    except Exception as e:
        print(f"Error in background task for user_case_id {user_case_id}: {str(e)}")
        query_file_status = """
        INSERT INTO report_file_status (status,description,requirement_gathering_id, user_case_id)
        VALUES (%s, %s, %s, %s)
        """
        query_file_status_params = (
            "failed",
            str(e),
            requirement_gathering_id,
            user_case_id,
        )
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute(query_file_status, query_file_status_params)
            conn.commit()
            cur.close()
        except Exception as e:
            print(f"Error in updating file status: {str(e)}")
        finally:
            conn.close()


async def generate_report_3(requirement_gathering_id, user_case_id):
    try:
        query_file_status = """
         INSERT INTO report_file_status (status,requirement_gathering_id, user_case_id)
            VALUES (%s, %s, %s)
            """
        query_file_status_params = (
            "in progress",
            requirement_gathering_id,
            user_case_id,
        )
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query_file_status, query_file_status_params)
        conn.commit()
        cur.close()

        answers = await get_answers(requirement_gathering_id, user_case_id)
        summary = await get_summary(answers)
        keywords = await get_keywords(answers)
        response_data = await search_documents(keywords)
        response_data = response_data[:3]
        response_data2 = await search_patents(response_data, summary)

        patentability_criteria = [
            "Novelty (35 U.S.C. § 102)",
            "Non-Obviousness (35 U.S.C. § 103)",
            "Utility (35 U.S.C. § 101)",
            "Enablement (35 U.S.C. § 112(a))",
            "Written Description (35 U.S.C. § 112(a))",
            "Definiteness (35 U.S.C. § 112(b))",
            "Industrial Application",
            "Clarity & Sufficiency",
            "Scope & Definition",
            "Economic Significance",
        ]

        report = {}

        for i in range(len(patentability_criteria)):
            assessment = await create_assessment(
                response_data2,
                answers,
                patentability_criteria[i],
            )
            report[patentability_criteria[i]] = assessment

        # Convert report dictionary to JSON string
        # report_str = str(report)
        report_str = dict_to_formatted_string(report)

        await create_word_document(
            report_str,
            requirement_gathering_id,
            user_case_id,
        )
        await create_pdf_document(
            report_str,
            requirement_gathering_id,
            user_case_id,
        )

        await add_report(
            report_str,
            requirement_gathering_id,
            user_case_id,
        )
        print("Report generated successfully.")
        return report
    except Exception as e:
        print(f"Error in background task for user_case_id {user_case_id}: {str(e)}")
        query_file_status = """
        INSERT INTO report_file_status (status,description,requirement_gathering_id, user_case_id)
        VALUES (%s, %s, %s, %s)
        """
        query_file_status_params = (
            "failed",
            str(e),
            requirement_gathering_id,
            user_case_id,
        )
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute(query_file_status, query_file_status_params)
            conn.commit()
            cur.close()
        except Exception as e:
            print(f"Error in updating file status: {str(e)}")
        finally:
            conn.close()
    finally:
        conn.close()
        print("Connection closed.")
