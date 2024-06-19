from fastapi import HTTPException, Depends
from app.core.database import get_db_connection, get_database_connection
from app.models.answers import AnswerList, Answer
from psycopg2.extras import execute_values
from app.utils.prompts import questions, prompts
import json
from app.core.azure_client import client


async def add_attachment_answers(answer_list: AnswerList):
    answers = answer_list.answers
    query = """
    INSERT INTO attachment_chats (question_id, report_id, user_id, answer,category_id,attachment_flag)
    VALUES %s
    """

    values = [
        (
            str(ans.question_id),
            str(ans.report_id),
            str(ans.user_id),
            ans.answer,
            str(ans.category_id),
            False,
        )
        for ans in answers
    ]

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        execute_values(cur, query, values)
        conn.commit()
        cur.close()
        return {"status": "success", "inserted_count": len(values)}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def check_user_attachment_answer(
    answer: str,
    QuestionID: str,
    userID: str,
    requirement_gathering_id: int,
    use_case_id: str,
):
    try:
        report_id = await get_report_id(requirement_gathering_id, use_case_id)
        response_data = await check_user_answers(
            answer, QuestionID, userID, requirement_gathering_id, report_id
        )
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_attachment_answer_by_llm(
    question_number,
    report_id,
    user_id,
    content,
    requirement_gathering_id,
):
    query = """
    INSERT INTO attachment_chats (question_id, report_id, user_id, answer, attachment_flag, requirement_gathering_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (question_id, report_id, user_id, requirement_gathering_id) DO UPDATE 
    SET answer = EXCLUDED.answer
"""

    values = (
        str(question_number),
        str(report_id),
        str(user_id),
        str(content),
        True,
        requirement_gathering_id,
    )

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        cur.close()
        return {
            "status": "success",
        }
    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def add_attachment_answer_content(content, requirement_gathering_id, user_id):
    query = """
    INSERT INTO attachment (user_id, content, requirement_gathering_id)
    VALUES (%s, %s, %s)
    ON CONFLICT (requirement_gathering_id, user_id)
    DO UPDATE SET
        content = EXCLUDED.content
    """
    values = (str(user_id), content, requirement_gathering_id)

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        cur.close()
        return {"status": "success"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_report_id(requirement_gathering_id, category_id):
    query = """
    SELECT report_id FROM requirements_gathering WHERE requirement_gathering_id = %s AND use_case_id = %s
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


async def check_user_answers(
    answer: str,
    QuestionID: int,
    userID: int,
    requirement_gathering_id: int,
    report_id: int,
):
    answeredQuestion = questions[QuestionID - 1]

    checkPrompt = prompts[QuestionID - 1]

    system_prompt = f"""Given the user's response to the question: '{answeredQuestion}',
            evaluate the completeness based on these criteria and provide the response always in JSON format as given below:
            '{checkPrompt}'

            The response should encapsulate all specified points to be considered complete.

            If the user's input lacks any required details, is ambiguous, or misses critical information, the output should be:
            {{"status": "false", 
              "question": "<appropriate follow-up question from the predefined list>"}}
            
            This indicates the need for additional information to fulfill the request comprehensively.

            For every gap identified in the user's response, select a follow-up question that precisely targets 
            the missing information. This could involve requesting more elaborate explanations, clarification of 
            technical terms, specific instances of technology application, or arguments supporting the novelty and 
            uniqueness of the concept. It should be included in the question key of the output JSON format. 
            Always format the output in JSON, including 'status' and 'question' keys, to streamline the evaluation 
            process and guide the user towards providing a fully rounded response.

            Conversely, if the user's answer meets all the outlined criteria, confirm the completeness with:
            {{"status": "true", 
            "question": ""}}
            
            Avoid generating apology messages or phrases like "I'm sorry" in the follow-up questions or responses.

            Always format the output in JSON, including 'status' and 'question' keys, to streamline the evaluation 
            process and guide the user towards providing a fully rounded response.
            """

    message_text = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": answer},
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

        content = completion.choices[0].message.content

        if content:
            try:
                generated_content_json = json.loads(content)
                if (
                    "status" not in generated_content_json
                    or "question" not in generated_content_json
                ):
                    return {
                        "status": "false",
                        "question": f"I couldn't identify the required details in your response to the question: '{answeredQuestion}'. Can you provide more specific information or elaborate further?",
                        "userID": userID,
                        "sessionID": requirement_gathering_id,
                        "questionID": QuestionID,
                    }
                generated_content_json["userID"] = userID
                generated_content_json["sessionID"] = requirement_gathering_id
                generated_content_json["questionID"] = QuestionID

                if generated_content_json["status"] == "true":
                    # Insert the answer and question ID, session ID, and user ID into the database
                    query = """
                        INSERT INTO attachment_chats (question_id, report_id, user_id, answer, attachment_flag, requirement_gathering_id)
                        VALUES %s
                        ON CONFLICT (question_id, report_id, user_id, requirement_gathering_id) DO UPDATE
                        SET answer = EXCLUDED.answer,
                            attachment_flag = EXCLUDED.attachment_flag
                        """

                    values = [
                        (
                            str(QuestionID),
                            str(report_id),
                            str(userID),
                            answer,
                            False,
                            requirement_gathering_id,
                        )
                    ]
                    conn = get_db_connection()
                    try:
                        # Create a cursor and use `execute_values` to efficiently insert multiple row
                        cur = conn.cursor()
                        execute_values(cur, query, values)
                        conn.commit()
                        cur.close()
                    except Exception as e:
                        conn.rollback()
                        raise HTTPException(status_code=500, detail=str(e))

            except json.JSONDecodeError:
                generated_content_json = {
                    "status": "false",
                    "question": f"I couldn't identify the required details in your response to the question: '{answeredQuestion}'. Can you provide more specific information or elaborate further?",
                    "userID": userID,
                    "sessionID": requirement_gathering_id,
                    "questionID": QuestionID,
                }
        else:
            generated_content_json = {
                "status": "false",
                "question": f"I couldn't identify the required details in your response to the question: '{answeredQuestion}'. Can you provide more specific information or elaborate further?",
                "userID": userID,
                "sessionID": requirement_gathering_id,
                "questionID": QuestionID,
            }

        return generated_content_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
