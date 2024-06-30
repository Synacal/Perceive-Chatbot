from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.services.ip_license_process.common import (
    get_answers_license,
    get_keywords_license,
    search_patents_ids,
    search_patents,
    get_summary_license,
    get_patent_data,
    create_report,
)

from app.models.ip_license_process import ReportParams


from pydantic import BaseModel
import pandas as pd
import psycopg2
from typing import List
import os

router = APIRouter()


@router.post("/ip_license_process")
async def ip_license_process(report_params: ReportParams):
    try:
        answers = await get_answers_license(
            report_params.requirement_gathering_id, report_params.user_case_id
        )

        summary = await get_summary_license(answers)
        keywords = await get_keywords_license(answers)
        patents_ids = await search_patents_ids(keywords)
        patent_data = await get_patent_data(patents_ids)
        report = await create_report(summary, patent_data)
        return report

        # return {"patents": patents_ids, "patent_data": patent_data}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class QueryParams(BaseModel):
    output_directory: str
    keywords: List[str]


from app.core.database import get_percieve_db_connection


def export_to_csv(query, output_path, conn):
    try:
        df = pd.read_sql_query(query, conn)
        df.to_csv(output_path, index=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-csv/")
def generate_csv(params: QueryParams):
    output_dir = params.output_directory
    keywords = params.keywords

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Build the query conditions
    title_abstract_conditions = " OR ".join(
        [f"title_abstract_tsvector @@ websearch_to_tsquery('{kw}')" for kw in keywords]
    )
    claims_conditions = " OR ".join(
        [f"claims_tsvector @@ websearch_to_tsquery('{kw}')" for kw in keywords]
    )

    conn = get_percieve_db_connection()

    try:
        # Query for patents
        patents_query = f"""
        SELECT target.patents.year, target.patents.title, target.patents.abstract, id AS patent_id,
               target.patents.claim_text AS patent_claim_text, abstract
        FROM target.patents
        JOIN target.claim c ON target.patents.id = c.patent_id
        WHERE ({title_abstract_conditions} OR {claims_conditions})
          AND target.patents.year >= (EXTRACT(year FROM current_date) - 10)
        GROUP BY target.patents.year, target.patents.title, target.patents.abstract, id, abstract;
        """
        export_to_csv(
            patents_query, os.path.join(output_dir, "perceive-patent.csv"), conn
        )

        # Query for assignees
        assignees_query = f"""
        SELECT target.patent_assignees.name, title, reel_no, target.patent_assignees.recorded_date,
               target.patent_assignees.city, target.patent_assignees.country, id AS patent_id
        FROM target.patents
        JOIN target.patent_assignees ON target.patent_assignees.patent_id = target.patents.id
        JOIN target.assignment_history ON target.assignment_history.patent_id = target.patents.id
           AND target.assignment_history.recorded_date = target.patent_assignees.recorded_date
        WHERE ({title_abstract_conditions} OR {claims_conditions})
          AND target.patents.year >= (EXTRACT(year FROM current_date) - 10);
        """
        """
        export_to_csv(
            assignees_query,
            os.path.join(output_dir, "perceive-assignees-patent.csv"),
            conn,
        )
        """

        # Query for current assignees
        current_assignees_query = f"""
        SELECT target.assignees.assignee_individual_name, assignee_organization, id AS patent_id
        FROM target.patents
        JOIN target.assignees ON target.assignees.patent_id = target.patents.id
        WHERE ({title_abstract_conditions} OR {claims_conditions})
          AND target.patents.year >= (EXTRACT(year FROM current_date) - 10);
        """
        """
        export_to_csv(
            current_assignees_query,
            os.path.join(output_dir, "perceive-current-assignees-patent.csv"),
            conn,
        )"""

        # Query for assignors
        assignors_query = f"""
        SELECT target.patent_assignors.name, title, reel_no, target.patent_assignors.recorded_date, id AS patent_id
        FROM target.patents
        JOIN target.patent_assignors ON target.patent_assignors.patent_id = target.patents.id
        JOIN target.assignment_history ON target.assignment_history.patent_id = target.patents.id
           AND target.assignment_history.recorded_date = target.patent_assignors.recorded_date
        WHERE ({title_abstract_conditions} OR {claims_conditions})
          AND target.patents.year >= (EXTRACT(year FROM current_date) - 10);
        """
        """
        export_to_csv(
            assignors_query,
            os.path.join(output_dir, "perceive-assignors-patent.csv"),
            conn,
        )"""

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()

    return {"message": "CSV files generated successfully"}
