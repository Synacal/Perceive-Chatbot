questions = [
    # Common Qs
    "What is the full name of the company, and what is its core mission?",
    "Please provide a concise description of the technology or product your company has developed.",
    "Describe the technical aspects and unique features of the key product or technology developed by the company. How does your product or technology introduce innovation or novelty within its field?",
    "Could you explain your company's business model and how it generates revenue? What are the different revenue streams for your company, including primary and potential ancillary streams?",
    # new validity analysis question
    "Can you provide key single-word terms that describe the core technologies or features of your innovation? For keywords that consist of two or three words, please separate each word with a comma. These keywords will be used to conduct a comprehensive prior art search to ensure the uniqueness of your intellectual property.",
    # Synthetic data for IP validity analysis
    # 'What is the full name of the company developing the key product or technology developed by the company?',
    # 'Please provide a concise description of the key product or technology developed by the company technology.',
    "Can you tell me more about the specific patents or prior art you may have encountered during your research? What similarities or differences did you find?",
    "How does the key product or technology developed by the company meet the criteria of novelty in its field?",
    "Can you explain why the features of the key product or technology developed by the company are considered non-obvious to someone skilled in the field?",
    "How is the key product or technology developed by the company applicable to industrial needs in its domain?",
    "What is your strategy for patent filing, including geographies and patent offices?",
    "How have you ensured enablement in the patent application for the key product or technology developed by the company?",
    "How have you ensured the definiteness of claims in your patent application for the key product or technology developed by the company?",
    "Can you provide the exact claims that will be present in the patent application for your key product or technology developed?",
    # IP licensing strategy process document
    "What specific technologies or innovations are you looking to license, and what makes these aspects unique and valuable for potential licensees?",
    "Who are your ideal licensees for your technology, and in which industries or sectors do they primarily operate?",
    "What business goals are you aiming to achieve through IP licensing?",
    "What is your preferred licensing model, and how does this preference align with your strategic objectives?",
    "Are there specific geographic regions you are targeting for licensing your technology? ",
    "What are your financial expectations from licensing agreements?",
    "How prepared are you to negotiate and manage complex licensing agreements?",
    "What key terms and conditions are you prioritizing in your licensing agreements?",
    "Are you open to exploring strategic partnerships or cross-licensing opportunities?",
    "What metrics and KPIs will you use to evaluate the success of your licensing strategy?",
    "Do you have any performance requirements or specific expectations from licensees to ensure they contribute effectively to the licensed technology's success?",
    "How do you plan to handle sublicensing rights, audit rights, and quality control provisions to safeguard the integrity and value of your licensed IP?",
    "Are there any particular fields of use you are considering for your licensing agreements, and how do these choices reflect market demands and opportunities?",
    # IP Valuation questions list
    "What is the pricing strategy for your product or service?",
    "How do you calculate the gross margin for your offerings?",
    "What are the total development costs incurred for your product or service?",
    "What future costs do you anticipate for full development and market launch?",
    "What discount rate do you apply to future cash flows and why?",
    "What is the projected annual revenue growth rate, and how did you arrive at this figure?",
    "What are the anticipated operating expenses, and how are they allocated?",
    "How do you project sales revenue for your products or services over the next 5 years?",
    "What market and competitive analysis data have you gathered, and how does it influence your strategy?",
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
    "Who are your main competitors, and what differentiates your product or service from theirs?",
    # Market analysis
    "What internal metrics does your company use to measure success in aligning with market dynamics and industry trends?",
    "How does your company assess the impact of global market drivers and restraints on its product development and marketing strategies?",
    "Can you describe a recent strategic decision made by your company in response to projected market growth in your industry? What was the rationale behind this decision?",
    "How does your company define its primary target market within its industry?",
    "What data-driven methods does your company use to segment its customer base?",
    "What are the key factors that influence the purchasing decisions of your customers?",
    "How has consumer feedback shaped the development of new features in your products?",
    "Can you describe the competitive advantages of your latest product compared to its main competitors?",
    "What role does intellectual property play in your product differentiation strategy?",
    "What primary and secondary revenue streams-based pricing strategy has your company adopted for its flagship product, and why?",
    "What are your company's sales revenue and customer base expansion targets for the next five years, especially in emerging markets?",
    "What are your customer acquisition targets for the upcoming year, and what key metrics will you use to measure success?",
    "What are your long-term customer retention targets, and how do you measure effectiveness in retaining customers?",
    # M&A strategy report
    "What are your strategic goals for mergers and acquisitions?",
    "What criteria do you use to select acquisition targets?",
    "Are there any regulatory considerations in your target markets?",
    "What financial metrics do you consider important in assessing M&A targets?",
    "How do you plan to integrate the acquired company into your operations?",
    "How do you measure the success of your M&A activities?",
    # Competitive landscape
    "What are the key factors that have contributed to changes in your company's market share over the past five years?",
    "Can you provide details on your company's brand positioning strategies and how they differ from those of your main competitors?",
    "Could you share insights into your company's financial performance trends, including revenue growth and profit margins, compared to your competitors?",
    "What are the most significant recent innovations your company has developed, and how do they compare to the innovations from your competitors?",
    "How does your company assess the effectiveness of its sales channels, and what unique strategies have you implemented compared to your competitors?",
    "What unique aspects of your recent marketing campaigns have successfully engaged consumers, and how does this engagement compare to that achieved by your competitors?",
    "What strategic moves has your company recently made to stay competitive, and how do you anticipate these moves will position you against future competitor actions?",
    "Can you provide details on the strengths and weaknesses of your supply chain compared to those of your key competitors?",
    "What specific strategies has your company employed to enhance customer satisfaction, and how do these strategies compare to those of your competitors?",
    "What are some of the most impactful strategic alliances your company has formed, and how have these alliances affected your competitive positioning?",
    "What are the most significant risks your company faces from competitive actions, and how are you managing these risks?",
    # Regulatory pathways
    "Could you provide insights into the regulatory challenges and pathways in key markets such as the USA, EU, and Asia?",
    "What operational adjustments has your company had to make to comply with international regulations?",
    "What are the major regulatory risks your company faces, and what mitigation strategies have you implemented?",
    "What quality management systems does your company implement to satisfy regulatory requirements?",
    "What emerging regulatory trends could potentially impact your market, and how do you plan to respond?",
    "What are the current regulatory challenges your company is facing, and how are these affecting your operations?",
    "What are your company's future targets in terms of regulatory achievements, and what steps are you taking to meet these goals?",
    "How does your company engage with regulatory bodies to ensure compliance and influence regulatory frameworks?",
    # Consumer intelligence
    "What are your strategic goals for expanding into new demographic or geographic markets in the next 5 years?",
    "What consumer trends and behaviors have you identified as pivotal for shaping your product development over the next few years?",
    "How do you plan to leverage digital marketing to increase consumer engagement in underpenetrated markets?",
    "What are the anticipated challenges in adopting new technologies among your target consumers, and how do you plan to address them?",
    "How do you intend to measure the success of new market entries and product launches?",
    "What strategies will you implement to enhance customer loyalty and retention in increasingly competitive markets?",
    "Can you describe how you will use consumer feedback to inform future product iterations and service improvements?",
    "What are your plans for integrating emerging technologies to stay ahead in your market?",
    "How will you adapt your pricing strategy to balance growth, competitiveness, and profitability in new markets?",
]


prompts = [
    # Common questions
    "Confirm the response includes the full legal name of the company and provides a comprehensive overview of its core mission and business focus. Check if the answer details how the company aims to impact its industry or target market through its products, services, or innovations.",
    "Verify the description clearly outlines the key product or technology developed by the company, including its main functions, how it works, and the unique benefits it offers to users. Ensure the answer highlights the technological innovation and its application.",
    f"""
        Assess the user's response regarding the technical aspects and unique features of the key product or technology developed by the company. Request elaboration How does your product or technology introduce innovation or novelty within its field?.
        """,
    "Check if the response identifies all primary and potential secondary revenue streams for the company. It should detail how each stream contributes to the overall financial sustainability and future growth plans.",
    # validity analysis new question
    "Check if the response includes a list of key single-word terms that describe the core technologies or features of the innovation, ensuring each term is separated by a comma and includes the following keywords: Spatial, Ergonomic, Adaptive, Computing, Display, Clarity, User, Engagement. Verify that there are no missing or extraneous words in the list.",
    # Synthetic data for IP validity analysis
    f"""
        Confirm the user's understanding of specific patents or prior art related to their product or technology. Inquire about the identified patents, their differences from the user's solution, and how the user's platform stands out in terms of machine learning models, data integration, and empowering healthcare professionals.
        """,
    # 7 prompt
    f"""
        Evaluate how the key product or technology developed by the company meets the criteria of novelty in its field, focusing on its integration of diverse machine learning models, data fusion approach, use of NLP for unstructured data interpretation, and how these aspects contribute to its mission.
        """,
    # 8 prompt
    f"""
        Check the explanation provided for why the features of the key product or technology developed by the company are considered non-obvious, emphasizing its unique combination of machine learning algorithms, data integration capabilities, real-time analysis, NLP usage, and how these aspects align with its mission. There's no need for detailed information on how your spatial computing algorithm works.
        """,
    # 9 prompt
    f"""
        Examine the applicability of the key product or technology developed by the company to industrial needs within its domain, emphasizing early disease detection, personalized treatment plans, versatility across healthcare settings, and how these aspects contribute to its mission. Based on the provided answer, evaluate how ARSight addresses industrial needs in terms of efficiency, safety, and learning. Consider its practical applications across industries and how it meets the challenges and demands of the digital age. If the user's answer demonstrates that ARSight enhances efficiency, safety, and learning in manufacturing and maintenance, education and training, and design and architecture, and its practical applications across industries showcase its capacity to meet the challenges of the digital age, then confirm the completeness with a JSON response having a "true" status and an empty string for the question key.
        """,
    # 10 prompt
    f"""
        Evaluate the user's strategy for patent filing, including targeted geographies and patent offices. Request specifics on key markets, rationale for choices, considerations for demand, regulatory environments, and how these strategies align with the company's mission.
        """,
    # 11 prompt
    f"""
        Verify how enablement is ensured in the patent application for the key product or technology developed by the company, focusing on comprehensive details, code snippets, workflow diagrams provided, and how they contribute to the mission of empowering healthcare professionals. If the user's answer clearly demonstrates the inclusion of meticulously documented development processes, detailed descriptions of algorithms, clear instructions for reproduction, examples, and best practice scenarios showcasing application and effectiveness, and a commitment to transparency and innovation dissemination, then confirm the completeness with a JSON response having a "true" status and an empty string for the question key.
        """,
    # 12 prompt
    f"""
        Confirm how definiteness of claims is ensured in the patent application for the key product or technology developed by the company, emphasizing clear, concise claims supported by detailed technology descriptions, highlighting unique aspects, and how they align with the company's mission.
        """,
    # 13 prompt
    f"""
        Request the exact claims present in the patent application for the AI-based Predictive Analytics solution, seeking details on the method for predicting health outcomes, application of NLP, real-time analysis, genetic information integration, specific healthcare applications covered in the claims, and how they contribute to achieving the company's mission.
        """,
    # IP licensing strategy process document
    # 14 prompt
    f"""Review the description of the technology intended for licensing. Ensure it details the unique attributes, advantages over current market offerings, and why it’s valuable to licensees.
        
        Parameters to Check:
            Comprehensive description of the technology
            Unique attributes and competitive advantages
            Value proposition to potential licensees""",
    # 15 prompt
    f"""Confirm whether the target market for the technology is clearly defined. Evaluate if there’s an understanding of how the technology meets the needs of these sectors.

        Parameters to Check:
            Clear definition of target market and sectors
            Alignment of technology with sector needs
            Justification for sector selection based on technology’s capabilities""",
    # 16 prompt
    f"""Determine if the business goals for IP licensing are specific and how the licensing model supports achieving these goals.

        Parameters to Check:
            Specific business goals related to IP licensing
            Licensing model's support for these goal
            Strategy for achieving goals through licensing""",
    # 17 prompt
    f"""
        Review the user's preferred licensing model, which includes a mix of exclusive and non-exclusive licensing agreements. Evaluate how this preference aligns with their strategic objectives, focusing on offering exclusive licenses to strategic partners in niche medical applications and non-exclusive licenses for consumer electronics to foster broader adoption and innovation. Ensure the response includes detailed metrics such as upfront fees, royalties, and performance milestones, demonstrating a clear strategy for revenue generation and market penetration. If the user's answer provides comprehensive details about the licensing model metrics, strategic alignment with objectives, and a clear revenue generation strategy, confirm the completeness with a JSON response having a "true" status and an empty string for the question key.
        """,
    # 18 prompt
    f"""Assess the strategy behind geographic targeting for licensing.

        Parameters to Check:
            Rationale for choosing specific geographic regions
            Market data supporting these choices
            Trends and regulatory considerations""",
    # 19 prompt
    f"""
        Assess the user's financial expectations from licensing agreements, which include upfront payments ranging from $100,000 to $500,000 and royalty rates between 4% and 7% of net sales. Evaluate the reasoning behind these financial expectations, considering factors such as market positioning, licensee's applications, and strategic value of the technology.
        """,
    # 20 prompt
    f"""Evaluate the preparedness for negotiating complex agreements. If the response does not reflect a comprehensive strategy.
        
        Parameters to Check:
            Strategy for negotiation of complex agreements
            Considerations for legal and contractual complexities
            Readiness for managing IP compliance""",
    # 21 prompt
    f"""
        Evaluate the key terms and conditions prioritized in the user's licensing agreements, focusing on strict quality control provisions to maintain technology integrity, clear definitions of fields of use to protect market segments, and robust audit rights for compliance and accurate royalty reporting. Verify how these terms align with the user's strategic goals and technology protection objectives.   
        """,
    # 22 prompt
    f"""Examine the openness to and strategy for forming strategic partnerships or cross-licensing agreements. 

        Parameters to Check:
            Criteria for selecting strategic partners
            Benefits and strategic fit of potential partnerships
            Approach to cross-licensing opportunities
            """,
    # 23 prompt
    f"""Analyze the comprehensiveness of the metrics and KPIs provided for licensing strategy evaluation.

        Parameters to Check:
            Variety and relevance of metrics and KPIs
            Inclusion of qualitative metrics like licensee satisfaction
            Measurement of technological adoption by licensees""",
    # 24 prompt
    f"""Scrutinize the adequacy of performance requirements for licensees. 

        Parameters to Check:
            Specificity of performance requirements
            Enforcement mechanisms for performance standards
            Support systems in place for licensees""",
    # 25 prompt
    f"""Probe the strategy for managing sublicensing rights, conducting audits, and ensuring quality control. 

        Parameters to Check:
            Sublicensing approval process and criteria
            Audit procedures and frequency
            Quality control measures and licensee product standards""",
    # 26 prompt
    f"""Inquire about the strategic decision-making behind the selection of fields of use for licensing. 

        Parameters to Check:
            Strategic selection of fields of use
            Market analysis supporting these choices
            Alignment with current and future market demands""",
    # IP Valuation questions list
    # 27 prompt
    f"""Evaluate if the answer specifies the type of pricing strategy used (competitive, value-based, etc.), mentions the factors considered (cost, market competition, customer value), and if it covers different offerings (products and services).""",
    # 28 prompt
    f"""Check if the answer includes a formula or method for calculating gross margins for both products and services, mentions specific percentages, and explains the impact of these margins on business operations.""",
    # 29 prompt
    f"""Determine if the answer provides a specific total cost figure, breaks down the cost categories (R&D, legal fees, market research), and reflects on the significance of these costs in the product/service development.""",
    # 30 prompt
    f"""Assess if the answer estimates future costs with a clear breakdown (product development, marketing campaign, distribution), explains the rationale behind the estimate, and outlines the strategic plan for these investments.""",
    # 31 prompt
    f"""Verify if the answer specifies a discount rate percentage, provides justification based on industry risks and competitive landscape, and explains how the rate was determined.""",
    # 32 prompt
    f"""Ensure the answer mentions a specific growth rate, details the factors contributing to this projection (market adoption, expansion, marketing strategies), and discusses the basis for these projections.""",
    # 33 prompt
    f"""Confirm if the answer outlines total projected operating expenses, provides allocation percentages across departments (R&D, marketing, administrative), and justifies these allocations with strategic considerations.""",
    # 34 prompt
    f"""Check if the answer gives projected revenue figures, describes the methodology for these projections (market trends, pre-order data, marketing strategies), and considers both products and services.""",
    # 35 prompt
    f"""Evaluate if the answer identifies key competitors and market share, discusses relevant market trends and technological advancements, and explains how this data influences the company's strategic direction.""",
    # Qs for Market potential report
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
    "Ensure the answer provides an analysis of the competitive landscape, including direct and indirect competitors. It should evaluate how the company's offering compares in terms of features, pricing, and quality, and discuss strategies for differentiation and market positioning.",
    # Market analysis
    f"""Ensure the response includes the following aspects related to how a company measures its success in aligning with market dynamics and industry trends:

            Description of the problem the product solves: Does the response explain the core issue the product addresses in the market?
            Explanation of how the product addresses the problem: Is there a clear explanation of how the product meets market needs or challenges?
            Examples of user scenarios or pain points: Are specific examples provided that illustrate why customers would seek out the product?
            Differentiation from traditional solutions: Does the response highlight how the product distinguishes itself from existing market solutions or competitors?
            Evidence of the product's effectiveness: Is there evidence or metrics provided that demonstrate how the product evaluates its market impact and effectiveness?

        Use these points to verify if the response comprehensively addresses how the company assesses its alignment with market dynamics and industry trends.""",
    # 44
    f"""Check if the response includes the following aspects related to how a company assesses the impact of global market drivers and restraints:

            Economic Indicators: Does the response describe how the company monitors global economic trends like inflation rates and consumer spending patterns to forecast demand and adjust pricing strategies?
            Consumer Trends: Is there an explanation of how ongoing market research helps the company track changes in consumer preferences and technology adoption rates, guiding product development and feature prioritization?
            Regulatory Changes: Does the response detail how the company keeps abreast of new regulations in key markets and adapts compliance strategies to ensure seamless market entry and sustained operations?

        Use these points to verify if the response comprehensively covers how the company adapts its strategies based on global market drivers and restraints.""",
    # 45
    f"""Check if the response includes the following aspects related to a recent strategic decision:
            1. Description of the strategic decision: Does the response describe the specific decision made?
            2. Rationale behind the decision: Is there an explanation of why this decision was made, including relevant data and projections?
            3. Expected outcomes: Does the response mention the anticipated benefits or goals of the decision?""",
    f"""Check if the response includes the following aspects related to the primary target market:
            1. Target demographic: Does the response clearly define the age range, lifestyle, and income level of the target market?
            2. Reasons for targeting this market: Is there an explanation of why this demographic is significant?""",
    f"""Check if the response includes the following aspects related to customer segmentation methods:
            1. Data-driven methods: Does the response describe the techniques used, such as cluster analysis?
            2. Types of data used: Is there a mention of the specific data factors considered, like demographic, behavioral, and psychographic?""",
    f"""Check if the response includes the following aspects related to factors influencing customers' purchasing decisions:
            1. Key factors: Does the response identify the main factors that influence purchasing decisions?
            2. Supporting evidence: Are there examples or evidence supporting these factors, such as customer testimonials or expert reviews?""",
    f"""Check if the response includes the following aspects related to the impact of consumer feedback on product development:
            1. Specific features developed: Does the response list the new features developed based on feedback?
            2. Connection to consumer needs: Is there an explanation of how these features address evolving consumer needs?""",
    f"""Check if the response includes the following aspects related to competitive advantages:
            1. Unique features: Does the response describe the distinctive features of the latest product?
            2. Comparison to competitors: Is there a comparison showing how these features set the product apart from competitors?""",
    f"""Check if the response includes the following aspects related to the role of intellectual property:
            1. Importance of IP: Does the response explain the significance of intellectual property in the company's strategy?
            2. Specific patents or technologies: Are specific patents or proprietary technologies mentioned?""",
    f"""Check if the response includes the following aspects related to the pricing strategy:
            1. Primary and secondary revenue streams: Does the response identify the primary and secondary revenue streams?
            2. Rationale for pricing: Is there an explanation of why the current pricing strategy was chosen?""",
    f"""Check if the response includes the following aspects related to sales revenue and customer base expansion targets:
            1. Revenue targets: Does the response state the sales revenue targets for the next five years?
            2. Customer base expansion: Are there specific targets for customer base growth, especially in emerging markets?""",
    f"""Check if the response includes the following aspects related to customer acquisition targets:
            1. Acquisition targets: Does the response mention the specific number of new users the company aims to acquire?
            2. Key metrics: Are the key metrics for measuring success identified?""",
    f"""Check if the response includes the following aspects related to customer retention targets:
            1. Retention targets: Does the response state the long-term customer retention rate goals?
            2. Measurement of effectiveness: Are the methods for measuring retention effectiveness described?""",
    # M&A strategy report
    f"""
    Define your strategic goals for M&A activities, outlining how these goals align with your overall business objectives. Explain the specific technologies or capabilities you aim to acquire and the expected outcomes from these strategic M&A initiatives.

    Completeness Checklist:
    • Specific strategic goals for engaging in M&A activities
    • Details on how M&A aligns with overall business objectives
    • Expected outcomes from strategic M&A initiatives

    """,
    f"""
    Specify the criteria you use to evaluate potential M&A targets, detailing the importance of technological fit, financial health, and market potential. List the key performance indicators you consider essential for assessing these targets.

    Completeness Checklist:
    • Detailed criteria used to evaluate potential M&A targets
    • Importance of technological, financial, and market fit
    • Description of key performance indicators for potential targets

    """,
    f"""
    Identify the regulatory environments impacting your M&A activities and assess the specific compliance requirements in your target markets. Explain your risk assessment strategy for managing regulatory challenges.

    Completeness Checklist:
    • Overview of regulatory environments impacting M&A activities
    • Specific compliance requirements in target markets
    • Risk assessment related to regulatory challenges

    """,
    f"""
    Analyze the list of financial metrics critical to assessing M&A targets, calculate the valuation methods used, and project the financial thresholds that guide your decision to engage in M&A.

    Completeness Checklist:
    • List of financial metrics critical in assessing M&A targets
    • Explanation of valuation methods employed
    • Financial thresholds considered for engaging in M&A

    """,
    f"""
   Check the detailed integration of new acquisitions, outlining timelines and key objectives for technology and system integration.

    Completeness Checklist:
    • Detailed plan for integrating new acquisitions
    • Timeline and key objectives for technology and system integration
    • Strategies for cultural integration and employee retention

    """,
    f"""
    Measure the metrics used to evaluate the success of M&A transactions, assess the timeframes for evaluating post-M&A performance, and evaluate the long-term impacts on the company’s market position and financial health.

    Completeness Checklist:
    • Metrics used to measure the success of M&A transactions
    • Timeframes for evaluating post-M&A performance
    • Long-term impacts on the company’s market position and financial health

    """,
    # Competitive landscape
    f"""Check if the response includes the following aspects related to changes in market share:
            1. Market share change: Does the response mention the percentage change in market share over the past five years?
            2. Key factors: Are the main factors contributing to this change, such as market expansion and product launches, identified?""",
    f"""Check if the response includes the following aspects related to brand positioning strategies:
            1. Brand positioning focus: Does the response describe the company's brand positioning strategies?
            2. Differentiation: Is there a comparison showing how these strategies differ from those of main competitors?
            3. Impact: Are the effects of these strategies on brand perception or other metrics mentioned?""",
    f"""Check if the response includes the following aspects related to financial performance trends:
            1. Revenue growth: Does the response provide details on the company's revenue growth rate over the last few years?
            2. Profit margins: Are there details on profit margin trends?
            3. Comparison to competitors: Is the company's performance compared to industry averages or main competitors?""",
    f"""Check if the response includes the following aspects related to recent innovations:
            1. Significant innovations: Does the response describe the most significant recent innovations developed by the company?
            2. Comparison to competitors: Is there a comparison of these innovations to those of competitors?""",
    f"""Check if the response includes the following aspects related to sales channel effectiveness:
            1. Assessment methods: Does the response explain how the company assesses the effectiveness of its sales channels?
            2. Unique strategies: Are unique strategies mentioned that differentiate the company from competitors?
            3. Impact: Is there evidence or metrics showing the impact of these strategies?""",
    f"""Check if the response includes the following aspects related to marketing campaign engagement:
            1. Unique aspects: Does the response describe the unique aspects of recent marketing campaigns?
            2. Engagement comparison: Is there a comparison of consumer engagement with that of competitors?""",
    f"""Check if the response includes the following aspects related to strategic moves for competitiveness:
            1. Recent strategic moves: Does the response detail recent strategic moves made by the company?
            2. Anticipated outcomes: Is there an explanation of how these moves are expected to position the company against future competitor actions?""",
    f"""Check if the response includes the following aspects related to supply chain strengths and weaknesses:
            1. Strengths: Does the response describe the strengths of the company's supply chain?
            2. Weaknesses: Are the weaknesses of the supply chain also mentioned?
            3. Comparison to competitors: Is there a comparison of these strengths and weaknesses to those of key competitors?""",
    f"""Check if the response includes the following aspects related to customer satisfaction strategies:
            1. Specific strategies: Does the response detail the specific strategies employed to enhance customer satisfaction?
            2. Comparison to competitors: Is there a comparison showing how these strategies differ from those of competitors?
            3. Impact: Are there metrics or evidence showing the impact of these strategies on customer satisfaction?""",
    f"""Check if the response includes the following aspects related to strategic alliances:
            1. Significant alliances: Does the response describe the most impactful strategic alliances formed by the company?
            2. Competitive positioning: Is there an explanation of how these alliances have affected the company's competitive positioning?""",
    f"""Check if the response includes the following aspects related to risks from competitive actions:
            1. Significant risks: Does the response identify the most significant risks the company faces from competitive actions?
            2. Risk management: Is there an explanation of how the company is managing these risks?""",
    # Regulatory pathways
    f"""Check if the response includes the following aspects related to regulatory challenges and pathways in key markets:
            1. Regulatory challenges: Does the response identify the specific regulatory challenges in key markets such as the USA, EU, and Asia?
            2. Regulatory pathways: Is there a description of how the company navigates these regulatory challenges?""",
    f"""Check if the response includes the following aspects related to operational adjustments for regulatory compliance:
            1. Operational adjustments: Does the response describe the adjustments made to comply with international regulations?
            2. Impact: Is there an explanation of how these adjustments have impacted go-to-market timelines, costs, and marketing strategies?""",
    f"""Check if the response includes the following aspects related to regulatory risks and mitigation strategies:
            1. Major risks: Does the response identify the major regulatory risks the company faces?
            2. Mitigation strategies: Is there an explanation of the strategies implemented to mitigate these risks?""",
    f"""Check if the response includes the following aspects related to quality management systems:
            1. Quality management systems: Does the response describe the quality management systems implemented to satisfy regulatory requirements?
            2. Compliance: Is there a mention of specific standards such as ISO 13485 and how they ensure continuous compliance and quality assurance?""",
    f"""Check if the response includes the following aspects related to emerging regulatory trends:
            1. Emerging trends: Does the response identify emerging regulatory trends that could impact the market?
            2. Response plan: Is there a description of how the company plans to respond to these trends?""",
    f"""Check if the response includes the following aspects related to current regulatory challenges:
            1. Current challenges: Does the response describe the current regulatory challenges the company is facing?
            2. Operational impact: Is there an explanation of how these challenges are affecting the company's operations?""",
    f"""Check if the response includes the following aspects related to future regulatory targets:
            1. Future targets: Does the response state the company's future targets in terms of regulatory achievements?
            2. Steps to meet goals: Is there a description of the steps the company is taking to meet these goals?""",
    f"""Check if the response includes the following aspects related to engagement with regulatory bodies:
            1. Engagement: Does the response describe how the company engages with regulatory bodies to ensure compliance?
            2. Influence: Is there a mention of how the company influences regulatory frameworks through participation in industry groups or consultations?""",
    # Consumer intelligence
    f"""Check if the response includes the following aspects related to strategic goals for market expansion:
            1. Geographic and demographic targets: Does the response describe the specific geographic and demographic markets the company aims to enter?
            2. Strategies for market entry: Is there a description of the strategies the company plans to use to penetrate these new markets?""",
    f"""Check if the response includes the following aspects related to consumer trends shaping product development:
            1. Identified trends: Does the response identify specific consumer trends and behaviors?
            2. Product development: Is there a description of how these trends are influencing the company's product development plans?""",
    f"""Check if the response includes the following aspects related to leveraging digital marketing:
            1. Digital marketing strategies: Does the response describe the digital marketing strategies the company plans to use?
            2. Expected outcomes: Is there an explanation of how these strategies are expected to increase consumer engagement?""",
    f"""Check if the response includes the following aspects related to challenges in adopting new technologies:
            1. Anticipated challenges: Does the response identify specific challenges the company expects to face?
            2. Mitigation strategies: Is there a description of how the company plans to address these challenges?""",
    f"""Check if the response includes the following aspects related to measuring the success of market entries and product launches:
            1. Success metrics: Does the response describe the metrics the company will use to measure success?
            2. Targets: Are there specific targets mentioned for market share, customer acquisition cost, engagement, and repeat purchase rates?""",
    f"""Check if the response includes the following aspects related to enhancing customer loyalty and retention:
            1. Loyalty strategies: Does the response describe the strategies the company plans to use to enhance customer loyalty?
            2. Retention initiatives: Is there a description of any new initiatives or programs aimed at increasing customer retention?""",
    f"""Check if the response includes the following aspects related to using consumer feedback:
            1. Feedback mechanisms: Does the response describe how the company collects consumer feedback?
            2. Implementation: Is there an explanation of how this feedback is used to inform product iterations and service improvements?""",
    f"""Check if the response includes the following aspects related to integrating emerging technologies:
            1. Emerging technologies: Does the response describe the new technologies the company plans to integrate?
            2. Expected impact: Is there an explanation of how these technologies will help the company stay ahead in the market?""",
    f"""Check if the response includes the following aspects related to adapting pricing strategy:
            1. Pricing strategies: Does the response describe the pricing strategies the company plans to use in new markets?
            2. Balancing growth, competitiveness, and profitability: Is there an explanation of how these strategies will balance growth, competitiveness, and profitability?""",
]
