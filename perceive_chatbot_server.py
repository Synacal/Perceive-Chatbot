from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AzureOpenAI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from typing import List
from prompts import questions, prompts
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AzureOpenAI(
    azure_endpoint="https://chatbotmedipredict.openai.azure.com/",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview"
)

def select_question(question_id: int):
    return questions[question_id]

def select_prompt(question_id:int):
    return prompts[question_id]

# Define Pydantic models for the request and response
class Answer(BaseModel):
    question_id: str
    session_id: str
    user_id: str
    answer: str

class AnswerList(BaseModel):
    answers: List[Answer]

conn = psycopg2.connect(
    dbname="pn-chatbot", 
    user="synacal", 
    password="ZnkyD5knABer9#F", 
    host="pnchatbot.postgres.database.azure.com"
)


@app.post("/generate/")
async def generate_response(answer: str,QuestionID: int,userID: int,sessionID: int):
    
    answeredQuestion = select_question(QuestionID-1)

    checkPrompt = select_prompt(QuestionID-1)

    print("answeredQuestion",answeredQuestion)
    print("checkPrompt",checkPrompt)
    system_prompt = f"""Given the user's response to the question: '{answeredQuestion}',
            evaluate the completeness based on these criteria and provide the response always in JSON format as given below:
            {checkPrompt}
            The response should encapsulate all specified points to be considered complete.

            If the user's input lacks any required details, is ambiguous, or misses critical information, the output should be:
            {{"status": "false",
              "question": "<appropriate follow-up question from the predefined list>"}}
            This indicates the need for additional information to fulfill the request comprehensively.

            For every gap identified in the user's response, select a follow-up question that precisely targets 
            the missing information. This could involve requesting more elaborate explanations, clarification of 
            technical terms, specific instances of technology application, or arguments supporting the novelty and 
            uniqueness of the concept.

            Conversely, if the user's answer meets all the outlined criteria, confirm the completeness with:
            {{"status": "true", 
            "question": ""}}

            Avoid generating apology messages or phrases like "I'm sorry" in the follow-up questions or responses.

            Always format the output in JSON, including 'status' and 'question' keys, to streamline the evaluation 
            process and guide the user towards providing a fully rounded response.
            """

    
    message_text = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": answer}
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
            stop=None
        )

        content = completion.choices[0].message.content
        print("content",content)

        if content:
            try:
                generated_content_json = json.loads(content)
                if "status" not in generated_content_json or "question" not in generated_content_json:
                    return {"status": "false", 
                            "question": f"I couldn't identify the required details in your response to the question: '{answeredQuestion}'. Can you provide more specific information or elaborate further?",
                            "userID": userID,
                            "sessionID": sessionID,
                            "questionID": QuestionID}
                generated_content_json["userID"] = userID
                generated_content_json["sessionID"] = sessionID
                generated_content_json["questionID"] = QuestionID
            except json.JSONDecodeError:
                 generated_content_json = {
                "status": "false", 
                "question": f"I couldn't identify the required details in your response to the question: '{answeredQuestion}'. Can you provide more specific information or elaborate further?",
                "userID": userID,
                "sessionID": sessionID,
                "questionID": QuestionID,
            }
        else:
            generated_content_json = {
                "status": "false", 
                "question": f"I couldn't identify the required details in your response to the question: '{answeredQuestion}'. Can you provide more specific information or elaborate further?",
                "userID": userID,
                "sessionID": sessionID,
                "questionID": QuestionID,
            }

        return generated_content_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add-answers/")
async def create_answers(answer_list: AnswerList):
    answers = answer_list.answers
    query = """
    INSERT INTO user_chats (question_id, session_id, user_id, answer)
    VALUES %s
    """
    
    values = [(str(ans.question_id), str(ans.session_id), str(ans.user_id), ans.answer) for ans in answers]
    
    try:
        # Create a cursor and use `execute_values` to efficiently insert multiple rows
        cur = conn.cursor()
        execute_values(cur, query, values)
        conn.commit()
        cur.close()
        return {"status": "success", "inserted_count": len(values)}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))