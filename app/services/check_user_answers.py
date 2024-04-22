import json
from fastapi import HTTPException
from app.utils.prompts import questions, prompts
from app.core.azure_client import client

async def check_user_answers(answer: str,QuestionID: int,userID: int,sessionID: int):
    answeredQuestion = questions[QuestionID-1]

    checkPrompt = prompts[QuestionID-1]

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