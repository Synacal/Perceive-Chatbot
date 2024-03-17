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

def select_question(question_id: int):
    questions = [
                #Synthetic data for IP validity analysis 
                'What is the full name of the company developing the AI-based Predictive Analytics for Healthcare?',
                'Please provide a concise description of the AI-based Predictive Analytics for Healthcare technology.',
                'Describe the technical aspects and unique features of the AI-based Predictive Analytics for Healthcare.',
                'Can you tell me more about the specific patents or prior art you may have encountered during your research? What similarities or differences did you find?',
                'How does the AI-based Predictive Analytics for Healthcare meet the criteria of novelty in its field?',
                'Can you explain why the features of the AI-based Predictive Analytics for Healthcare are considered non-obvious to someone skilled in the field?',
                'How is the AI-based Predictive Analytics for Healthcare applicable to industrial needs in its domain?',
                'What is your strategy for patent filing, including geographies and patent offices?',
                'How have you ensured enablement in the patent application for the AI-based Predictive Analytics for Healthcare?',
                'How have you ensured the definiteness of claims in your patent application for the AI-based Predictive Analytics for Healthcare?',
                'Can you provide the exact claims that will be present in the patent application for your AI-based Predictive Analytics solution?',

                #IP licensing strategy process document
                'What specific technologies or innovations within NeuraWear are you looking to license, and what makes these aspects unique and valuable for potential licensees?',
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
                
                #IP Valuation questions list
                'What is the pricing strategy for your product or service?',
                'How do you calculate the gross margin for your offerings?',
                'What are the total development costs incurred for your product or service?'
                'What future costs do you anticipate for full development and market launch?'
                'What discount rate do you apply to future cash flows and why?',
                'What is the projected annual revenue growth rate, and how did you arrive at this figure?',
                'What are the anticipated operating expenses, and how are they allocated?',
                'How do you project sales revenue for your products or services over the next 5 years?',
                'What market and competitive analysis data have you gathered, and how does it influence your strategy?',
                ]
    return questions[question_id]

def select_prompt(question_id:int):
    prompts = [
        #Synthetic data for IP validity analysis
        #1 prompt
        f"""
        """,
        #2 prompt
        f"""
        """,
        #3 prompt
        f"""
        """,    
        #4 prompt
        f"""
        """,    
        #5 prompt
        f"""
        """,
        #6 prompt
        f"""
        """,
        #7 prompt
        f"""
        """,
        #8 prompt
        f"""
        """,
        #9 prompt
        f"""
        """,
        #10 prompt
        f"""
        """,
        #11 prompt
        f"""
        """,

        #IP licensing strategy process document
        #12 prompt
        f"""Review the description of the technology intended for licensing. Ensure it details the unique attributes, advantages over current market offerings, and why it’s valuable to licensees.
        
        Parameters to Check:
            Comprehensive description of the technology
            Unique attributes and competitive advantages
            Value proposition to potential licensees""",
        #13 prompt
        f"""Confirm whether the target market for the technology is clearly defined. Evaluate if there’s an understanding of how the technology meets the needs of these sectors.

        Parameters to Check:
            Clear definition of target market and sectors
            Alignment of technology with sector needs
            Justification for sector selection based on technology’s capabilities""",
        #14 prompt
        f"""Determine if the business goals for IP licensing are specific and how the licensing model supports achieving these goals.

        Parameters to Check:
            Specific business goals related to IP licensing
            Licensing model's support for these goal
            Strategy for achieving goals through licensing""",
        #15 prompt   
        f"""

        """,
        #16 prompt
        f"""Assess the strategy behind geographic targeting for licensing.

        Parameters to Check:
            Rationale for choosing specific geographic regions
            Market data supporting these choices
            Trends and regulatory considerations""",
        #17 prompt
        f"""

        """,
        #18 prompt
        f"""Evaluate the preparedness for negotiating complex agreements. If the response does not reflect a comprehensive strategy.
        
        Parameters to Check:
            Strategy for negotiation of complex agreements
            Considerations for legal and contractual complexities
            Readiness for managing IP compliance""",
        #19 prompt
        f"""
            
            """,
        #20 prompt
        f"""Examine the openness to and strategy for forming strategic partnerships or cross-licensing agreements. 

        Parameters to Check:
            Criteria for selecting strategic partners
            Benefits and strategic fit of potential partnerships
            Approach to cross-licensing opportunities
            """,
        #21 prompt
        f"""Analyze the comprehensiveness of the metrics and KPIs provided for licensing strategy evaluation.

        Parameters to Check:
            Variety and relevance of metrics and KPIs
            Inclusion of qualitative metrics like licensee satisfaction
            Measurement of technological adoption by licensees""",
        #22 prompt
        f"""Scrutinize the adequacy of performance requirements for licensees. 

        Parameters to Check:
            Specificity of performance requirements
            Enforcement mechanisms for performance standards
            Support systems in place for licensees""",
        #23 prompt
        f"""Probe the strategy for managing sublicensing rights, conducting audits, and ensuring quality control. 

        Parameters to Check:
            Sublicensing approval process and criteria
            Audit procedures and frequency
            Quality control measures and licensee product standards""",
        #24 prompt
        f"""Inquire about the strategic decision-making behind the selection of fields of use for licensing. 

        Parameters to Check:
            Strategic selection of fields of use
            Market analysis supporting these choices
            Alignment with current and future market demands""",
        #IP Valuation questions list
        #25 prompt
        f"""Evaluate if the answer specifies the type of pricing strategy used (competitive, value-based, etc.), mentions the factors considered (cost, market competition, customer value), and if it covers different offerings (products and services).""",
        #26 prompt
        f"""Check if the answer includes a formula or method for calculating gross margins for both products and services, mentions specific percentages, and explains the impact of these margins on business operations.""",
        #27 prompt
        f"""Determine if the answer provides a specific total cost figure, breaks down the cost categories (R&D, legal fees, market research), and reflects on the significance of these costs in the product/service development.""",
        #28 prompt
        f"""Assess if the answer estimates future costs with a clear breakdown (product development, marketing campaign, distribution), explains the rationale behind the estimate, and outlines the strategic plan for these investments.""",
        #29 prompt
        f"""Verify if the answer specifies a discount rate percentage, provides justification based on industry risks and competitive landscape, and explains how the rate was determined.""",
        #30 prompt
        f"""Ensure the answer mentions a specific growth rate, details the factors contributing to this projection (market adoption, expansion, marketing strategies), and discusses the basis for these projections.""",
        #31 prompt
        f"""Confirm if the answer outlines total projected operating expenses, provides allocation percentages across departments (R&D, marketing, administrative), and justifies these allocations with strategic considerations.""",
        #32 prompt
        f"""Check if the answer gives projected revenue figures, describes the methodology for these projections (market trends, pre-order data, marketing strategies), and considers both products and services.""",
        #33 prompt
        f"""Evaluate if the answer identifies key competitors and market share, discusses relevant market trends and technological advancements, and explains how this data influences the company's strategic direction.""",  
        
    ]

    return prompts[question_id]

def select_follow_up_question(question_id:int):
    follow_up_questions = [
        #Synthetic data for IP validity analysis
        f"""""",
        f"""""",
        f"""""",
        f"""""",
        f"""""",
        f"""""",
        f"""""",
        f"""""",
        f"""""",
        f"""""",
        f"""""",
        #IP licensing strategy process document
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
        f"""how these fields align with current and emerging market needs.""",
        #IP Valuation questions list
        f"""Could you specify which pricing strategies you've considered and which one you're leaning towards? It would also be helpful to know the reasons behind your preference and how you plan to implement it.""",
        f"""Can you provide a detailed breakdown of how you calculate the gross margin for both your product sales and subscription services, including the costs factored into these calculations?""",
        f"""Could you approximate the total development costs you've incurred so far, including any major categories of expenses like R&D, legal, or marketing?""",
        f"""Can you estimate the future costs required for the remaining development, marketing, and launch phases of your product or service, and how you plan to allocate these costs?""",
        f"""What factors are you considering in determining your discount rate for future cash flows, and what range or specific rate are you currently leaning towards?""",
        f"""Can you share any preliminary annual revenue growth projections you have, along with the assumptions or market research that support these figures?""",
        f"""Could you specify the main categories of your anticipated operating expenses and provide a rough allocation or percentage breakdown for each category?""",
        f"""Could you outline your sales revenue targets for the next 5 years and explain the basis or methodology for these projections, including any market trends or data you're relying on?""",
        f"""Can you share specific insights or findings from your market and competitive analysis, including how these insights are influencing your product development, pricing, and marketing strategies?"""

    ]
    return follow_up_questions[question_id]

@app.post("/generate/")
async def generate_response(answer: str,answeredQuestionID: int,userID: int,sessionID: int):
    
    answeredQuestion = select_question(answeredQuestionID)

    checkPrompt = select_prompt(answeredQuestionID)

    followUpQuestion = select_follow_up_question(answeredQuestionID)

    system_prompt = f"""The user answers the following question: {answeredQuestion}
                    Then, check if the user prompt contains the following points:
                        {checkPrompt}

                    The answer should be only in JSON format: 
                        {{status: "true/false", 
                        question: "question"}}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, 
                    
                    a question must be returned from the question JSON again. question = {followUpQuestion}"""
    
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
            generated_content_json = json.loads(content)
            generated_content_json["userID"] = userID
            generated_content_json["sessionID"] = sessionID
        else:
            generated_content_json = {"error": "Server error. Please try again later."}
        
        return generated_content_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
