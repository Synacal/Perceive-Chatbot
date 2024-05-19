from fastapi import FastAPI, HTTPException
import base64
from io import BytesIO
from PyPDF2 import PdfReader
from app.utils.prompts import questions, prompts
from app.core.azure_client import client
import json


def get_pdf_content(attachment_base64: str) -> str:
    try:
        # Decode the base64 string
        pdf_bytes = base64.b64decode(attachment_base64)
        # Use BytesIO to read the PDF bytes
        pdf_file = BytesIO(pdf_bytes)
        # Create a PDF reader
        pdf_reader = PdfReader(pdf_file)
        # Extract text from each page
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text() + "\n"

        return content
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error reading PDF content: {str(e)}"
        )


def get_questions(title: str) -> list:
    try:
        # Get the questions from the title
        if title == "Market analysis":
            selectedQuestions = questions[0:3] + questions[42:55]
        elif title == "Business model":
            selectedQuestions = questions[3:7] + questions[55:62]
        else:
            selectedQuestions = questions[7:42]
        return selectedQuestions
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error getting questions: {str(e)}"
        )


def get_prompts(title: str) -> list:
    try:
        # Get the prompts from the title
        if title == "Market analysis":
            selectedPrompts = prompts[0:3] + prompts[42:55]
        elif title == "Business model":
            selectedPrompts = prompts[3:7] + prompts[55:62]
        else:
            selectedPrompts = prompts[7:42]
        return selectedPrompts
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting prompts: {str(e)}")


async def check_user_attachment(questions: list, prompts: list, content: str) -> dict:
    system_prompt = f"""
    Given the user's response to the questions: {json.dumps(questions)},

    evaluate the completeness based on these criteria and provide the response always in JSON format as given below:
    {json.dumps(prompts)}

    Questions and completeness criteria are entered in order to match each other.

    The response should encapsulate all specified points to be considered complete.

    If the user's input lacks any required details, is ambiguous, or misses critical information, the output should be:
    {{
    "responses": [
        {{"status": "false", "question": "<appropriate follow-up question from the predefined list>"}},
        ...
    ]
    }}

    This indicates the need for additional information to fulfill the request comprehensively.

    For every gap identified in the user's response, select a follow-up question that precisely targets the missing information. This could involve requesting more elaborate explanations, clarification of technical terms, specific instances of technology application, or arguments supporting the novelty and uniqueness of the concept. It should be included in the question key of the output JSON format. Always format the output in JSON, including 'status' and 'question' keys, to streamline the evaluation process and guide the user towards providing a fully rounded response.

    Conversely, if the user's answer meets all the outlined criteria, confirm the completeness with:
    {{
    "responses": [
        {{"status": "true", "question": ""}},
        ...
    ]
    }}
    """
    message_text = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content},
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
        print(content)

        if content:
            try:
                generated_content_json = json.loads(content)
                return generated_content_json
            except json.JSONDecodeError:
                return {
                    "status": "Error of code",
                }
        else:
            return {"Error of code"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating response: {str(e)}"
        )
