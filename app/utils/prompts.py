questions = [
                #Common Qs
                'What is the full name of the company, and what is its core mission?',
                'Please provide a concise description of the technology or product your company has developed.',
                'Describe the technical aspects and unique features of the key product or technology developed by the company. How does your product or technology introduce innovation or novelty within its field?',
                "Could you explain your company's business model and how it generates revenue? What are the different revenue streams for your company, including primary and potential ancillary streams?",
                'What is your strategy for protecting the intellectual property associated with your product or technology? Are there specific patents or prior art that you have encountered during your research? What similarities or differences did you find?',
                
                #Synthetic data for IP validity analysis 
                # 'What is the full name of the company developing the key product or technology developed by the company?',
                # 'Please provide a concise description of the key product or technology developed by the company technology.',
                'Can you tell me more about the specific patents or prior art you may have encountered during your research? What similarities or differences did you find?',
                'How does the key product or technology developed by the company meet the criteria of novelty in its field?',
                'Can you explain why the features of the key product or technology developed by the company are considered non-obvious to someone skilled in the field?',
                'How is the key product or technology developed by the company applicable to industrial needs in its domain?',
                'What is your strategy for patent filing, including geographies and patent offices?',
                'How have you ensured enablement in the patent application for the key product or technology developed by the company?',
                'How have you ensured the definiteness of claims in your patent application for the key product or technology developed by the company?',
                'Can you provide the exact claims that will be present in the patent application for your key product or technology developed?',

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
                # "What is the full legal name of your company, and what is its primary mission?",
                # "Can you describe the key product or technology your company has developed?",
                # "Who is the target audience for your product or service?",
                "What specific problem does your product or service solve for your target audience?",
                "How does your product or service stand out from existing market offerings?",
                "What pricing strategy has your company adopted for its product or service?",
                # "Could you explain your company's business model and how it generates revenue?",
                "What are the primary and potential secondary revenue streams for your company?",
                "How is your company's cost structure organized, and what impact does it have on pricing and profitability?",
                "Which sales and distribution channels is your company planning to use?",
                "Who are your main competitors, and what differentiates your product or service from theirs?"
                ]


prompts = [
        # Common questions
        "Confirm the response includes the full legal name of the company and provides a comprehensive overview of its core mission and business focus. Check if the answer details how the company aims to impact its industry or target market through its products, services, or innovations.",
        "Verify the description clearly outlines the key product or technology developed by the company, including its main functions, how it works, and the unique benefits it offers to users. Ensure the answer highlights the technological innovation and its application.",
        f"""
        Assess the user's response regarding the technical aspects and unique features of the key product or technology developed by the company. Request elaboration How does your product or technology introduce innovation or novelty within its field?.
        """,
        "Check if the response identifies all primary and potential secondary revenue streams for the company. It should detail how each stream contributes to the overall financial sustainability and future growth plans.",
        "Check if the response identifies all strategy for protecting the intellectual property associated with related product or technology?",



        #Synthetic data for IP validity analysis
        f"""
        Confirm the user's understanding of specific patents or prior art related to their product or technology. Inquire about the identified patents, their differences from the user's solution, and how the user's platform stands out in terms of machine learning models, data integration, and empowering healthcare professionals.
        """,    
        #7 prompt
        f"""
        Evaluate how the key product or technology developed by the company meets the criteria of novelty in its field, focusing on its integration of diverse machine learning models, data fusion approach, use of NLP for unstructured data interpretation, and how these aspects contribute to its mission.
        """,
        #8 prompt
        f"""
        Check the explanation provided for why the features of the key product or technology developed by the company are considered non-obvious, emphasizing its unique combination of machine learning algorithms, data integration capabilities, real-time analysis, NLP usage, and how these aspects align with its mission. There's no need for detailed information on how your spatial computing algorithm works.
        """,
        #9 prompt
        f"""
        Examine the applicability of the key product or technology developed by the company to industrial needs within its domain, emphasizing early disease detection, personalized treatment plans, versatility across healthcare settings, and how these aspects contribute to its mission. Based on the provided answer, evaluate how ARSight addresses industrial needs in terms of efficiency, safety, and learning. Consider its practical applications across industries and how it meets the challenges and demands of the digital age. If the user's answer demonstrates that ARSight enhances efficiency, safety, and learning in manufacturing and maintenance, education and training, and design and architecture, and its practical applications across industries showcase its capacity to meet the challenges of the digital age, then confirm the completeness with a JSON response having a "true" status and an empty string for the question key.
        """,
        #10 prompt
        f"""
        Evaluate the user's strategy for patent filing, including targeted geographies and patent offices. Request specifics on key markets, rationale for choices, considerations for demand, regulatory environments, and how these strategies align with the company's mission.
        """,
        #11 prompt
        f"""
        Verify how enablement is ensured in the patent application for the key product or technology developed by the company, focusing on comprehensive details, code snippets, workflow diagrams provided, and how they contribute to the mission of empowering healthcare professionals. If the user's answer clearly demonstrates the inclusion of meticulously documented development processes, detailed descriptions of algorithms, clear instructions for reproduction, examples, and best practice scenarios showcasing application and effectiveness, and a commitment to transparency and innovation dissemination, then confirm the completeness with a JSON response having a "true" status and an empty string for the question key.
        """,
        #12 prompt
        f"""
        Confirm how definiteness of claims is ensured in the patent application for the key product or technology developed by the company, emphasizing clear, concise claims supported by detailed technology descriptions, highlighting unique aspects, and how they align with the company's mission.
        """,
        #13 prompt
        f"""
        Request the exact claims present in the patent application for the AI-based Predictive Analytics solution, seeking details on the method for predicting health outcomes, application of NLP, real-time analysis, genetic information integration, specific healthcare applications covered in the claims, and how they contribute to achieving the company's mission.
        """,

        #IP licensing strategy process document
        #14 prompt
        f"""Review the description of the technology intended for licensing. Ensure it details the unique attributes, advantages over current market offerings, and why it’s valuable to licensees.
        
        Parameters to Check:
            Comprehensive description of the technology
            Unique attributes and competitive advantages
            Value proposition to potential licensees""",
        #15 prompt
        f"""Confirm whether the target market for the technology is clearly defined. Evaluate if there’s an understanding of how the technology meets the needs of these sectors.

        Parameters to Check:
            Clear definition of target market and sectors
            Alignment of technology with sector needs
            Justification for sector selection based on technology’s capabilities""",
        #16 prompt
        f"""Determine if the business goals for IP licensing are specific and how the licensing model supports achieving these goals.

        Parameters to Check:
            Specific business goals related to IP licensing
            Licensing model's support for these goal
            Strategy for achieving goals through licensing""",
        #17 prompt   
        f"""
        Review the user's preferred licensing model for NeuraWear, which includes a mix of exclusive and non-exclusive licensing agreements. Evaluate how this preference aligns with their strategic objectives, focusing on offering exclusive licenses to strategic partners in niche medical applications and non-exclusive licenses for consumer electronics to foster broader adoption and innovation. Ensure the response includes detailed metrics such as upfront fees, royalties, and performance milestones, demonstrating a clear strategy for revenue generation and market penetration. If the user's answer provides comprehensive details about the licensing model metrics, strategic alignment with objectives, and a clear revenue generation strategy, confirm the completeness with a JSON response having a "true" status and an empty string for the question key.
        """,
        #18 prompt
        f"""Assess the strategy behind geographic targeting for licensing.

        Parameters to Check:
            Rationale for choosing specific geographic regions
            Market data supporting these choices
            Trends and regulatory considerations""",
        #19 prompt
        f"""
        Assess the user's financial expectations from licensing agreements for NeuraWear, which include upfront payments ranging from $100,000 to $500,000 and royalty rates between 4% and 7% of net sales. Evaluate the reasoning behind these financial expectations, considering factors such as market positioning, licensee's applications, and strategic value of the technology
        """,
        #20 prompt
        f"""Evaluate the preparedness for negotiating complex agreements. If the response does not reflect a comprehensive strategy.
        
        Parameters to Check:
            Strategy for negotiation of complex agreements
            Considerations for legal and contractual complexities
            Readiness for managing IP compliance""",
        #21 prompt
        f"""
        Evaluate the key terms and conditions prioritized in the user's licensing agreements for NeuraWear, focusing on strict quality control provisions to maintain technology integrity, clear definitions of fields of use to protect market segments, and robust audit rights for compliance and accurate royalty reporting. Verify how these terms align with the user's strategic goals and technology protection objectives.   
        """,
        #22 prompt
        f"""Examine the openness to and strategy for forming strategic partnerships or cross-licensing agreements. 

        Parameters to Check:
            Criteria for selecting strategic partners
            Benefits and strategic fit of potential partnerships
            Approach to cross-licensing opportunities
            """,
        #23 prompt
        f"""Analyze the comprehensiveness of the metrics and KPIs provided for licensing strategy evaluation.

        Parameters to Check:
            Variety and relevance of metrics and KPIs
            Inclusion of qualitative metrics like licensee satisfaction
            Measurement of technological adoption by licensees""",
        #24 prompt
        f"""Scrutinize the adequacy of performance requirements for licensees. 

        Parameters to Check:
            Specificity of performance requirements
            Enforcement mechanisms for performance standards
            Support systems in place for licensees""",
        #25 prompt
        f"""Probe the strategy for managing sublicensing rights, conducting audits, and ensuring quality control. 

        Parameters to Check:
            Sublicensing approval process and criteria
            Audit procedures and frequency
            Quality control measures and licensee product standards""",
        #26 prompt
        f"""Inquire about the strategic decision-making behind the selection of fields of use for licensing. 

        Parameters to Check:
            Strategic selection of fields of use
            Market analysis supporting these choices
            Alignment with current and future market demands""",

        #IP Valuation questions list
        #27 prompt
        f"""Evaluate if the answer specifies the type of pricing strategy used (competitive, value-based, etc.), mentions the factors considered (cost, market competition, customer value), and if it covers different offerings (products and services).""",
        #28 prompt
        f"""Check if the answer includes a formula or method for calculating gross margins for both products and services, mentions specific percentages, and explains the impact of these margins on business operations.""",
        #29 prompt
        f"""Determine if the answer provides a specific total cost figure, breaks down the cost categories (R&D, legal fees, market research), and reflects on the significance of these costs in the product/service development.""",
        #30 prompt
        f"""Assess if the answer estimates future costs with a clear breakdown (product development, marketing campaign, distribution), explains the rationale behind the estimate, and outlines the strategic plan for these investments.""",
        #31 prompt
        f"""Verify if the answer specifies a discount rate percentage, provides justification based on industry risks and competitive landscape, and explains how the rate was determined.""",
        #32 prompt
        f"""Ensure the answer mentions a specific growth rate, details the factors contributing to this projection (market adoption, expansion, marketing strategies), and discusses the basis for these projections.""",
        #33 prompt
        f"""Confirm if the answer outlines total projected operating expenses, provides allocation percentages across departments (R&D, marketing, administrative), and justifies these allocations with strategic considerations.""",
        #34 prompt
        f"""Check if the answer gives projected revenue figures, describes the methodology for these projections (market trends, pre-order data, marketing strategies), and considers both products and services.""",
        #35 prompt
        f"""Evaluate if the answer identifies key competitors and market share, discusses relevant market trends and technological advancements, and explains how this data influences the company's strategic direction.""",  
        


        # Market analysis Prompts
        # "Confirm the response includes the full legal name of the company and provides a comprehensive overview of its core mission and business focus. Check if the answer details how the company aims to impact its industry or target market through its products, services, or innovations.",
        # "Verify the description clearly outlines the key product or technology developed by the company, including its main functions, how it works, and the unique benefits it offers to users. Ensure the answer highlights the technological innovation and its application.",
        # "Ensure the answer specifies the target audience for the company's product or service, including demographic details, consumer behaviors, and preferences. Confirm that the response identifies why this market segment is targeted and how the product meets their needs.",
        "Check if the response articulates the specific problem or need the product or service addresses for its target audience. It should describe how the offering uniquely solves this problem and the benefits it provides over existing solutions.",
        "Confirm the answer details the product's or service's competitive advantages, including how it outperforms existing offerings in the market. Look for mentions of unique features, technology, cost-effectiveness, or any other factors that give it an edge.",
        "Verify that the response outlines the company's pricing strategy, explaining how the price was determined and the factors influencing this decision. It should also address how the pricing reflects the product's value proposition and market positioning.",
        # "Ensure the answer provides a clear explanation of the company's business model, including how it generates revenue, the value it offers customers, and its strategy for growth. Confirm it covers any unique aspects of their approach to reaching the market and securing income.",
        "Check if the response identifies all primary and potential secondary revenue streams for the company. It should detail how each stream contributes to the overall financial sustainability and future growth plans.",
        "Confirm the answer breaks down the company's cost structure, highlighting both fixed and variable costs, and discusses its implications on product pricing and overall profitability. Look for strategies mentioned for maintaining profitability.",
        "Verify the response identifies the sales and distribution channels the company uses or plans to use, explaining the choice and how these channels align with the company’s overall sales and marketing strategy.",
        "Ensure the answer provides an analysis of the competitive landscape, including direct and indirect competitors. It should evaluate how the company's offering compares in terms of features, pricing, and quality, and discuss strategies for differentiation and market positioning."
    ]