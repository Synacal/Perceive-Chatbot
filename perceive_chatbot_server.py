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
                'Are there any particular fields of use you are considering for NeuraWear\'s licensing agreements, and how do these choices reflect market demands and opportunities?',
                
                #IP Valuation questions list
                'What is the pricing strategy for your product or service?',
                'How do you calculate the gross margin for your offerings?',
                'What are the total development costs incurred for your product or service?',
                'What future costs do you anticipate for full development and market launch?',
                'What discount rate do you apply to future cash flows and why?',
                'What is the projected annual revenue growth rate, and how did you arrive at this figure?',
                'What are the anticipated operating expenses, and how are they allocated?',
                'How do you project sales revenue for your products or services over the next 5 years?',
                'What market and competitive analysis data have you gathered, and how does it influence your strategy?',

                # Qs for Market potential report
                "What is the full legal name of your company, and what is its primary mission?",
                "Can you describe the key product or technology your company has developed?",
                "Who is the target audience for your product or service?",
                "What specific problem does your product or service solve for your target audience?",
                "How does your product or service stand out from existing market offerings?",
                "What pricing strategy has your company adopted for its product or service?",
                "Could you explain your company's business model and how it generates revenue?",
                "What are the primary and potential secondary revenue streams for your company?",
                "How is your company's cost structure organized, and what impact does it have on pricing and profitability?",
                "Which sales and distribution channels is your company planning to use?",
                "Who are your main competitors, and what differentiates your product or service from theirs?"
                ]
    return questions[question_id]

def select_prompt(question_id:int):

    prompts = [
        #Synthetic data for IP validity analysis
        #1 prompt
        f"""
        Verify the full name of the company developing the AI-based Predictive Analytics for Healthcare, which should include 'MediPredict Solutions'. Also, ensure the response includes details about empowering healthcare professionals with cutting-edge tools to predict health outcomes more accurately and improve the overall quality of care.
        """,
        #2 prompt
        f"""
        Validate the concise description of the AI-based Predictive Analytics for Healthcare technology, focusing on its utilization of advanced machine learning algorithms and big data analytics. The description should also mention its mission to revolutionize patient care and provide early warnings and personalized treatment insights.
        """,
        #3 prompt
        f"""
        Assess the user's response regarding the technical aspects and unique features of the AI-based Predictive Analytics for Healthcare. Request elaboration on specific AI technologies, machine learning algorithms, unique features, and how they empower healthcare professionals and improve patient outcomes.
        """,    
        #4 prompt
        f"""
        Confirm the user's understanding of specific patents or prior art related to AI in healthcare. Inquire about the identified patents, their differences from the user's solution, and how the user's platform stands out in terms of machine learning models, data integration, and empowering healthcare professionals.
        """,    
        #5 prompt
        f"""
        Evaluate how the AI-based Predictive Analytics for Healthcare meets the criteria of novelty in its field, focusing on its integration of diverse machine learning models, data fusion approach, use of NLP for unstructured data interpretation, and how these aspects contribute to its mission.
        """,
        #6 prompt
        f"""
        Check the explanation provided for why the features of the AI-based Predictive Analytics for Healthcare are considered non-obvious, emphasizing its unique combination of machine learning algorithms, data integration capabilities, real-time analysis, NLP usage, and how these aspects align with its mission.
        """,
        #7 prompt
        f"""
        Examine the applicability of the AI-based Predictive Analytics for Healthcare to industrial needs within its domain, emphasizing early disease detection, personalized treatment plans, versatility across healthcare settings, and how these aspects contribute to its mission.
        """,
        #8 prompt
        f"""
        Evaluate the user's strategy for patent filing, including targeted geographies and patent offices. Request specifics on key markets, rationale for choices, considerations for demand, regulatory environments, and how these strategies align with the company's mission.
        """,
        #9 prompt
        f"""
        Verify how enablement is ensured in the patent application for the AI-based Predictive Analytics for Healthcare, focusing on comprehensive details, code snippets, workflow diagrams provided, and how they contribute to the mission of empowering healthcare professionals.
        """,
        #10 prompt
        f"""
        Confirm how definiteness of claims is ensured in the patent application for the AI-based Predictive Analytics for Healthcare, emphasizing clear, concise claims supported by detailed technology descriptions, highlighting unique aspects, and how they align with the company's mission.
        """,
        #11 prompt
        f"""
        Request the exact claims present in the patent application for the AI-based Predictive Analytics solution, seeking details on the method for predicting health outcomes, application of NLP, real-time analysis, genetic information integration, specific healthcare applications covered in the claims, and how they contribute to achieving the company's mission.
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
        Review the user's preferred licensing model for NeuraWear, which includes a mix of exclusive and non-exclusive licensing agreements. Evaluate how this preference aligns with their strategic objectives, focusing on offering exclusive licenses to strategic partners in niche medical applications and non-exclusive licenses for consumer electronics to foster broader adoption and innovation. Ensure the response emphasizes the goal of penetrating specific healthcare segments while encouraging innovation in consumer electronics.
        """,
        #16 prompt
        f"""Assess the strategy behind geographic targeting for licensing.

        Parameters to Check:
            Rationale for choosing specific geographic regions
            Market data supporting these choices
            Trends and regulatory considerations""",
        #17 prompt
        f"""
        Assess the user's financial expectations from licensing agreements for NeuraWear, which include upfront payments ranging from $100,000 to $500,000 and royalty rates between 4% and 7% of net sales. Evaluate the reasoning behind these financial expectations, considering factors such as market positioning, licensee's applications, and strategic value of the technology
        """,
        #18 prompt
        f"""Evaluate the preparedness for negotiating complex agreements. If the response does not reflect a comprehensive strategy.
        
        Parameters to Check:
            Strategy for negotiation of complex agreements
            Considerations for legal and contractual complexities
            Readiness for managing IP compliance""",
        #19 prompt
        f"""
        Evaluate the key terms and conditions prioritized in the user's licensing agreements for NeuraWear, focusing on strict quality control provisions to maintain technology integrity, clear definitions of fields of use to protect market segments, and robust audit rights for compliance and accurate royalty reporting. Verify how these terms align with the user's strategic goals and technology protection objectives.   
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
        


        # Market analysis Prompts
        "Confirm the response includes the full legal name of the company and provides a comprehensive overview of its core mission and business focus. Check if the answer details how the company aims to impact its industry or target market through its products, services, or innovations.",
        "Verify the description clearly outlines the key product or technology developed by the company, including its main functions, how it works, and the unique benefits it offers to users. Ensure the answer highlights the technological innovation and its application.",
        "Ensure the answer specifies the target audience for the company's product or service, including demographic details, consumer behaviors, and preferences. Confirm that the response identifies why this market segment is targeted and how the product meets their needs.",
        "Check if the response articulates the specific problem or need the product or service addresses for its target audience. It should describe how the offering uniquely solves this problem and the benefits it provides over existing solutions.",
        "Confirm the answer details the product's or service's competitive advantages, including how it outperforms existing offerings in the market. Look for mentions of unique features, technology, cost-effectiveness, or any other factors that give it an edge.",
        "Verify that the response outlines the company's pricing strategy, explaining how the price was determined and the factors influencing this decision. It should also address how the pricing reflects the product's value proposition and market positioning.",
        "Ensure the answer provides a clear explanation of the company's business model, including how it generates revenue, the value it offers customers, and its strategy for growth. Confirm it covers any unique aspects of their approach to reaching the market and securing income.",
        "Check if the response identifies all primary and potential secondary revenue streams for the company. It should detail how each stream contributes to the overall financial sustainability and future growth plans.",
        "Confirm the answer breaks down the company's cost structure, highlighting both fixed and variable costs, and discusses its implications on product pricing and overall profitability. Look for strategies mentioned for maintaining profitability.",
        "Verify the response identifies the sales and distribution channels the company uses or plans to use, explaining the choice and how these channels align with the company’s overall sales and marketing strategy.",
        "Ensure the answer provides an analysis of the competitive landscape, including direct and indirect competitors. It should evaluate how the company's offering compares in terms of features, pricing, and quality, and discuss strategies for differentiation and market positioning."
    ]

    return prompts[question_id]


@app.post("/generate/")
async def generate_response(answer: str,QuestionID: int,userID: int,sessionID: int):
    
    answeredQuestion = select_question(QuestionID-1)

    checkPrompt = select_prompt(QuestionID-1)
    print(answeredQuestion)
    print(checkPrompt)
    # system_prompt = f"""The user answers the following question: {answeredQuestion}
    #                 Then, check if the user prompt contains the following points:
    #                     {checkPrompt}
    #                     The user prompt should include all the above details for completeness.

    #                 If the user request does not contain all the required facts or input is 
    #                 not understandable or lacks the required information, return the status as 
    #                 "false" in JSON format. If "false" is returned, provide a follow-up question 
    #                 from the question JSON to help the user provide a complete answer. 
                    
    #                 Ensure that the follow-up questions directly address any gaps, request 
    #                 more detailed descriptions, seek clarifications on technical terms, ask for 
    #                 specific examples of technology application, and justify novelty and non-obviousness.

    #                 The output response should be only in JSON format: 
    #                     {{status: "true/false", 
    #                     question: "question"}}
    #                 The JSON data must include status and question fields.
                    
    #                 If the user request contains all the required facts, return the status as 
    #                 "true" in JSON format along with any relevant question from the question JSON.
                    
    #                 The output response should always be in JSON format."""
    system_prompt = f"""Given the user's response to the question: '{answeredQuestion}',
            evaluate the completeness based on these criteria and provide the response always in JSON format as given below:
            {checkPrompt}
            The response should encapsulate all specified points to be considered complete.

            If the user's input lacks any required details, is ambiguous, or misses critical information, the output should be:
            {{"status": "false", "question": "<appropriate follow-up question from the predefined list>"}}
            This indicates the need for additional information to fulfill the request comprehensively.

            For every gap identified in the user's response, select a follow-up question that precisely targets 
            the missing information. This could involve requesting more elaborate explanations, clarification of 
            technical terms, specific instances of technology application, or arguments supporting the novelty and 
            uniqueness of the concept.

            Conversely, if the user's answer meets all the outlined criteria, confirm the completeness with:
            {{"status": "true", "question": ""}}

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
        print (content)
        if content:
            try:
                generated_content_json = json.loads(content)
                generated_content_json["userID"] = userID
                generated_content_json["sessionID"] = sessionID
                generated_content_json["questionID"] = QuestionID
            except json.JSONDecodeError:
                return {"error": "Invalid JSON response from the API. Please check the format."}
        else:
            generated_content_json = {"error": "Server error. Please try again later."}

        return generated_content_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
