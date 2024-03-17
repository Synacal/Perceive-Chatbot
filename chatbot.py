from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AzureOpenAI
from fastapi.middleware.cors import CORSMiddleware
import os
import json

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

class Message(BaseModel):
    user_input: str

class QuestionID(BaseModel):
    user_input: int

class UserID(BaseModel):
    user_input: int

class SessionID(BaseModel):
    user_input: int

def select_question(question_id: int):
    questions = ['What specific technologies or innovations within NeuraWear are you looking to license, and what makes these aspects unique and valuable for potential licensees?',
                'Who are your ideal licensees for NeuraWear\'s technology, and in which industries or sectors do they primarily operate?',
                'What business goals are you aiming to achieve through IP licensing?',
                'What is your preferred licensing model for NeuraWear, and how does this preference align with your strategic objectives?',
                'Are there specific geographic regions you are targeting for licensing NeuraWear\'s technology?',
                'What are your financial expectations from licensing agreements?',
                'How prepared are you to negotiate and manage complex licensing agreements?',
                'What key terms and conditions are you prioritizing in your licensing agreements?',
                'Are you open to exploring strategic partnerships or cross-licensing opportunities?',
                'What metrics and KPIs will you use to evaluate the success of your licensing strategy?',
                'Do you have any performance requirements or specific expectations from licensees to ensure they contribute effectively to the licensed technology\'s success?',
                'How do you plan to handle sublicensing rights, audit rights, and quality control provisions to safeguard the integrity and value of your licensed IP?',
                'Are there any particular fields of use you are considering for NeuraWear\'s licensing agreements, and how do these choices reflect market demands and opportunities?'
                ]
    return questions[question_id]

def select_prompt(question_id:int):
    prompts = [
        #1 prompt
        f"""Review the description of the technology intended for licensing. Ensure it details the unique attributes, advantages over current market offerings, and why it’s valuable to licensees.
        
        Parameters to Check:
            Comprehensive description of the technology
            Unique attributes and competitive advantages
            Value proposition to potential licensees""",
        #2 prompt
        f"""Confirm whether the target market for the technology is clearly defined. Evaluate if there’s an understanding of how the technology meets the needs of these sectors.

        Parameters to Check:
            Clear definition of target market and sectors
            Alignment of technology with sector needs
            Justification for sector selection based on technology’s capabilities""",
        #3 prompt
        f"""Determine if the business goals for IP licensing are specific and how the licensing model supports achieving these goals.

        Parameters to Check:
            Specific business goals related to IP licensing
            Licensing model's support for these goal
            Strategy for achieving goals through licensing""",
        #4 prompt   
        f"""

        """,
        #5 prompt
        f"""Assess the strategy behind geographic targeting for licensing.

        Parameters to Check:
            Rationale for choosing specific geographic regions
            Market data supporting these choices
            Trends and regulatory considerations""",
        #6 prompt
        f"""

        """,
        #7 prompt
        f"""Evaluate the preparedness for negotiating complex agreements. If the response does not reflect a comprehensive strategy.
        
        Parameters to Check:
            Strategy for negotiation of complex agreements
            Considerations for legal and contractual complexities
            Readiness for managing IP compliance""",
        #8 prompt
        f"""
            
            """,
        #9 prompt
        f"""Examine the openness to and strategy for forming strategic partnerships or cross-licensing agreements. 

        Parameters to Check:
            Criteria for selecting strategic partners
            Benefits and strategic fit of potential partnerships
            Approach to cross-licensing opportunities
            """,
        #10 prompt
        f"""Analyze the comprehensiveness of the metrics and KPIs provided for licensing strategy evaluation.

        Parameters to Check:
            Variety and relevance of metrics and KPIs
            Inclusion of qualitative metrics like licensee satisfaction
            Measurement of technological adoption by licensees""",
        #11 prompt
        f"""Scrutinize the adequacy of performance requirements for licensees. 

        Parameters to Check:
            Specificity of performance requirements
            Enforcement mechanisms for performance standards
            Support systems in place for licensees""",
        #12 prompt
        f"""Probe the strategy for managing sublicensing rights, conducting audits, and ensuring quality control. 

        Parameters to Check:
            Sublicensing approval process and criteria
            Audit procedures and frequency
            Quality control measures and licensee product standards""",
        #13 prompt
        f"""Inquire about the strategic decision-making behind the selection of fields of use for licensing. 

        Parameters to Check:
            Strategic selection of fields of use
            Market analysis supporting these choices
            Alignment with current and future market demands"""
    ]

    return prompts[question_id]

def select_follow_up_question(question_id:int):
    follow_up_questions = [
        f"""what specific aspects of the innovation need further clarification?""",
        f"""what additional information is needed to identify the ideal licensees?""",
        f"""which aspects of the business strategy require more detailed explanation?""",
        f"""what specific details about the licensing model need further clarification?""",
        f"""what market data or trends could provide further justification for these regional choices?""",
        f"""what are your financial expectations from licensing agreements?""",
        f"""what legal considerations or contractual details are not yet addressed?""",
        f"""what key terms and conditions are you prioritizing in your licensing agreements?""",
        f"""how such partnerships would work and their strategic fit?""",
        f"""what metrics and KPIs will you use to evaluate the success of your licensing strategy?""",
        f"""what support will be provided, request detailed information on enforcement mechanisms and licensee support systems""",
        f"""how do you plan to handle sublicensing rights, audit rights, and quality control provisions to safeguard the integrity and value of your licensed IP?""",
        f"""how these fields align with current and emerging market needs."""

    ]
    return follow_up_questions[question_id]

@app.post("/generate/")
async def generate_response(message: Message,answeredQuestionID: QuestionID,userID: UserID,sessionID: SessionID):
    
    answeredQuestion = select_question(answeredQuestionID.user_input)

    followUpQuestion = select_follow_up_question(answeredQuestionID.user_input)

    system_prompt = f"""The user answers the following question: {answeredQuestion}
                    Then, check if the user prompt contains the following points:
                        "Evaluate the answer's level of detail regarding the technical description. Does it include operational mechanisms, implementation methods, and examples of real-world applications? If not, ask for specific details or real-world use cases that are missing."

                    The answer should be only in JSON format: 
                        {{status: "true/false", 
                        question: "question"}}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, 
                    
                    a question must be returned from the question JSON again. question = {followUpQuestion}"""
    
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
        generated_content_json["sessionID"] = sessionID.user_input
        generated_content_json["userID"] = userID.user_input
        return generated_content_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
