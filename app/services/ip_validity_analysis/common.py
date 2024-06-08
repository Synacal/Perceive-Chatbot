from fastapi import HTTPException
from typing import List


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
