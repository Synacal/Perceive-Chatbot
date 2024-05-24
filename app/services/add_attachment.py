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


def get_questions(category_id: str) -> list:
    try:
        # Get the questions from the category
        if category_id == "1":
            selectedQuestions = questions[0:2] + questions[5:13]
        elif category_id == "2":
            selectedQuestions = questions[13:26]
        elif category_id == "3":
            selectedQuestions = questions[26:35]
        elif category_id == "4":
            selectedQuestions = questions[35:42]
        elif category_id == "5":
            selectedQuestions = questions[0:3] + questions[42:55]
        else:
            selectedQuestions = questions[0:3]
        return selectedQuestions
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error getting questions: {str(e)}"
        )


def get_prompts(category_id: str) -> list:
    try:
        # Get the prompts from the category
        if category_id == "1":
            selectedPrompts = prompts[0:2] + prompts[5:13]
        elif category_id == "2":
            selectedPrompts = prompts[13:26]
        elif category_id == "3":
            selectedPrompts = prompts[26:35]
        elif category_id == "4":
            selectedPrompts = prompts[35:42]
        elif category_id == "5":
            selectedPrompts = prompts[0:3] + prompts[42:55]
        else:
            selectedPrompts = prompts[0:3]
        return selectedPrompts
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting prompts: {str(e)}")


async def check_user_attachment(
    questions: list,
    prompts: list,
    content: str,
    session_id: str,
    user_id: str,
    category_id: str,
):
    print(json.dumps(questions))
    print(json.dumps(prompts))

    system_prompt = f"""
        Given the user's response to the questions: {json.dumps(questions)},

        evaluate the completeness based on these criteria and provide the response always in JSON format as given below:
        {json.dumps(prompts)}

        Questions and completeness criteria are entered in order to match each other.

        The response should encapsulate all specified points to be considered complete.

        If the user's input lacks any required details, is ambiguous, or misses critical information, the output should be:
        "responses": [
            {{ "index list  of the question that has not been fully answered" }},
            ...
        ]

        example response (if question 1 and 3 are not answered fully):
        {{
            "responses": [
                1,
                3
            ]
        }}

        questions that have not been fully answered should be included in the responses key of the output JSON format.
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


async def check_user_attachment_temp(
    answeredQuestion: str,
    checkPrompt: str,
    content: str,
    session_id: str,
    user_id: str,
    category_id: str,
):

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
                if (
                    "status" not in generated_content_json
                    or "question" not in generated_content_json
                ):
                    return {
                        "status": "false",
                        "question": f"I couldn't identify the required details in your response to the question: '{answeredQuestion}'. Can you provide more specific information or elaborate further?",
                    }
                return generated_content_json
            except json.JSONDecodeError:
                generated_content_json = {
                    "status": "false",
                    "question": f"I couldn't identify the required details in your response to the question: '{answeredQuestion}'. Can you provide more specific information or elaborate further?",
                }
        else:
            generated_content_json = {
                "status": "false",
                "question": f"I couldn't identify the required details in your response to the question: '{answeredQuestion}'. Can you provide more specific information or elaborate further?",
            }

        return generated_content_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
