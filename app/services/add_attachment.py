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
        if title == "Synthetic data for IP validity analysis":
            selectedQuestions = questions[0:2] + questions[5:13]
        elif title == "IP licensing strategy process document":
            selectedQuestions = questions[13:26]
        elif title == "IP Valuation questions list":
            selectedQuestions = questions[26:35]
        elif title == "Qs for Market potential report":
            selectedQuestions = questions[35:42]
        elif title == "Market analysis":
            selectedQuestions = questions[0:3] + questions[42:55]
        else:
            selectedQuestions = questions[0:3]
        return selectedQuestions
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error getting questions: {str(e)}"
        )


def get_prompts(title: str) -> list:
    try:
        # Get the prompts from the title
        if title == "Synthetic data for IP validity analysis":
            selectedPrompts = prompts[0:2] + prompts[5:13]
        elif title == "IP licensing strategy process document":
            selectedPrompts = prompts[13:26]
        elif title == "IP Valuation questions list":
            selectedPrompts = prompts[26:35]
        elif title == "Qs for Market potential report":
            selectedPrompts = prompts[35:42]
        elif title == "Market analysis":
            selectedPrompts = prompts[0:3] + prompts[42:55]
        else:
            selectedPrompts = prompts[0:3]
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
        {{"question": "<question that has not been fully answered>"}},
        ...
    ]
    questions that has not been fully answered should be included in the responses key of the output JSON format.
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
                generated_content_json = content
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
