from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AzureOpenAI
import os
import json

app = FastAPI()

client = AzureOpenAI(
    azure_endpoint="https://chatbotmedipredict.openai.azure.com/",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview"
)

class Message(BaseModel):
    user_input: str

class Question(BaseModel):
    user_input: str

@app.post("/generate/")
async def generate_response(message: Message,answeredQuestion: Question):
    
    system_prompt = f"""The user answers the following question: {answeredQuestion.user_input}
                    Then, check if the user prompt contains the following points:
                        "Evaluate the answer's level of detail regarding the technical description. Does it include operational mechanisms, implementation methods, and examples of real-world applications? If not, ask for specific details or real-world use cases that are missing."

                    The answer should be only in JSON format: 
                        {{status: "true/false", 
                        question: "question"}}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again."""
    
    message_text = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message.user_input}
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
        generated_content_json = json.loads(content)
        return generated_content_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
