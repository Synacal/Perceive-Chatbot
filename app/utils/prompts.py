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
    "Check if the response describes how a company assesses the impact of global market drivers and restraints on its product development and marketing strategies using economic indicators, consumer trends, and regulatory changes to adapt strategies, forecast demand, adjust pricing strategies, guide product development, and ensure compliance for market entry and sustained operations.",
    "Evaluate if the response describes a recent strategic decision made by a company in response to the projected market growth in wearable technology, explains the rationale behind the decision focusing on investing in AI and machine learning capabilities, driven by consumer demand for personalized health insights, and aims to provide superior functionality and customization to set products apart in the market.",
    "Confirm if the response defines a company's primary target market within the wearable technology industry as health-conscious consumers aged 25 to 45, tech-savvy individuals with disposable income, explains data-driven methods used to segment the customer base such as cluster analysis techniques on demographic, behavioral, and psychographic factors, and outlines how these methods lead to targeted marketing strategies and product offerings.",
    "Verify if the response lists key factors influencing purchasing decisions for customers like functionality and accuracy of health tracking, aesthetic design, perceived value of AI features, and customer testimonials, and explains how consumer feedback has shaped the development of new features in products like enhanced sleep tracking, stress management tools, and integration with third-party health applications.",
    "Check if the response describes the competitive advantages of a company's latest wearable device compared to its main competitors such as real-time mood assessment using EEG signals, adaptive learning algorithms, and unique health monitoring and customization features, and explains the role of intellectual property in the product differentiation strategy focusing on protecting unique neuro-adaptive technologies and maintaining a competitive edge through patents.",
    "Assess if the response explains a company's pricing strategy for its flagship product, using a value-based pricing strategy set at $299, justifies the pricing reflecting advanced technology and health benefits compared to competitors, discusses sales revenue and customer base expansion targets for the next five years, customer acquisition and engagement targets, and long-term customer retention targets with specific metrics for success measurement.",
    "Evaluate if the response includes a detailed description of a company's business model, revenue streams, and cost structure focusing on the revenue model, product pricing, subscription models, future monetization plans, customer lifecycle value, strategies for scaling the business model, primary and secondary revenue streams, revenue diversification plans, cost optimization strategies, gross and net profit margins discussion, and plans for achieving and maintaining profitability.",
    "Confirm if the response outlines a company's sales and distribution channels including primary and secondary channels, strategies for optimizing each channel, partnerships and collaborations for distribution, balancing direct sales with retail or partner sales, adaptation to different market or regional channels, competitive landscape identification of direct and indirect competitors, comparative analysis of product features and pricing, strategy for competitive differentiation, plans to address competition and market challenges, and methods for tracking and responding to competitive moves.",
    "Check if the response provides a comprehensive explanation of a company's competitive advantage, including clear identification of competitors, specific features that outperform the competition, data analysis and interpretation capabilities, unique selling propositions (USPs), and any proprietary technology or intellectual property that contributes to its competitive edge.",
    "Verify the completeness of the response regarding a company's pricing analysis and revenue streams, ensuring it includes details on the primary and secondary revenue streams-based pricing strategy for the flagship product, justification of the pricing model, comparison with competitor pricing, reflection of the value proposition in the pricing, any tiered pricing or discount strategies, and future revenue growth projections.",
    "Evaluate the response on a company's future sales and market expansion targets, focusing on the sales revenue and customer base expansion targets for the next five years, especially in emerging markets. Confirm if the response provides specific growth rates, targets for revenue and customer base expansion, strategies for achieving these targets, and considerations for emerging markets in Asia and South America.",
    "Check if the response outlines a company's customer acquisition and engagement targets for the upcoming year, including the number of new users targeted, demographic focus, key metrics used to measure success such as cost per acquisition (CPA), conversion rates, and initial user engagement levels.",
    "Confirm the response regarding a company's long-term customer retention targets and effectiveness measurement, ensuring it includes targets for annual customer retention rate over the next five years, methods for tracking retention metrics such as churn rate, customer satisfaction scores, and renewal rates, and strategies for maintaining high customer retention levels.",
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
    f"""
    Analyze historical market share changes over the past five years, compare key factors influencing market share and revenue growth, and project future market share using prediction models and underlying assumptions.

    Completeness Checklist:
    o Historical data on market share changes over the past five years
    o Analysis of key factors influencing market share and revenue growth
    o Future market share prediction models and underlying assumptions

    """,
    f"""
    Evaluate brand positioning strategies among competitors, distinguish metrics used to measure customer loyalty and brand equity, and assess brand perception in the market through detailed analysis.

    Completeness Checklist:
    o Detailed comparison of brand positioning strategies among competitors
    o Metrics used to measure customer loyalty and brand equity
    o Analysis of brand perception in the market

    """,
    f"""
    Investigate financial performance trends such as revenue, profit margins, and expenditures, compare investments in innovation and customer acquisition, and summarize the financial risk profiles of major competitors.

    Completeness Checklist:
    o Financial performance trends including revenue, profit margins, and expenditures
    o Comparative analysis of investments in innovation and customer acquisition
    o Financial risk profiles for each major competitor

    """,
    f"""
    Catalog recent significant innovations introduced by your company and competitors, assess the patents and intellectual property landscape, and compare the impact of these innovations on market dynamics.

    Completeness Checklist:
    o List of recent significant innovations introduced by the company and competitors
    o Patents and intellectual property landscape analysis
    o Assessment of the impact of these innovations on market dynamics

    """,
    f"""
    Measure sales performance metrics and evaluate the effectiveness of distribution channels. Compare online and offline sales strategies and provide insights into unique sales tactics and their impact on the market.

    Completeness Checklist:
    o Evaluation of sales performance metrics and effectiveness of distribution channels
    o Comparative analysis of online and offline sales strategies
    o Insights into unique sales tactics and their market impact

    """,
    f"""
    Analyze the comparative effectiveness of marketing strategies and campaign outcomes. Measure metrics for campaign reach and consumer engagement, and conduct a detailed content analysis of marketing materials and communication strategies.

    Completeness Checklist:
    o Comparative analysis of marketing strategies and campaign effectiveness
    o Metrics measuring campaign reach and consumer engagement
    o Content analysis for marketing materials and communication strategies

    
    """,
    f"""
    Forecast future strategic decisions by competitors, plan scenario responses, and anticipate market positioning through a historical review of strategic moves and outcomes.

    Completeness Checklist:
    o Historical review of strategic moves and their outcomes
    o Forecasting of future strategic decisions by competitors
    o Scenario planning for strategic responses

    
    """,
    f"""
    Assess supply chain robustness and agility across competitors, benchmark operational efficiencies and production costs, and optimize key performance indicators relevant to supply chain and operations.

    Completeness Checklist:
    o Comparison of supply chain robustness and agility across competitors
    o Analysis of operational efficiencies and production costs
    o Benchmarking of key performance indicators (KPIs) relevant to supply chain and operations

    """,
    f"""
    Survey customer experience metrics across competitors, compare the effectiveness of customer support strategies, and analyze the Net Promoter Score (NPS) and customer satisfaction index (CSI) for comprehensive insights.

    Completeness Checklist:
    o Detailed comparison of customer experience metrics across competitors
    o Analysis of customer support strategies and their effectiveness
    o Net Promoter Score (NPS) and customer satisfaction index (CSI) comparison

    """,
    f"""
    Review existing and potential strategic alliances, evaluate synergy effects from partnerships, and strategize on the impact of these alliances on competitive positioning.

    Completeness Checklist:
    o Review of existing and potential strategic alliances
    o Analysis of the synergy effects from partnerships
    o Evaluation of partnership strategies on competitive positioning

    """,
    f"""
    Identify comprehensive risk analysis from competitive actions, assess potential threats and their expected impact, and evaluate the company’s vulnerability to competitive moves through effective risk management strategies.

    Completeness Checklist:
    o Comprehensive risk analysis from competitive actions
    o Identification of potential threats and their expected impact
    o Assessment of the company’s vulnerability to competitive moves

    """,
    # Regulatory pathways
    f"""
    Identify and describe regulatory environments across key markets (USA, EU, Asia), including specific regulatory challenges and adaptation strategies to meet market regulations.

    Completeness Checklist:
    o Identification and comparison of regulatory environments across key markets
    o Market-specific regulatory challenges and differences
    o Adaptation strategies to meet specific market regulations

    """,
    f"""
    Detail areas affected by regulations such as marketing and manufacturing, explain specific operational adjustments required for compliance, and illustrate the impact on business timelines and costs.

    Completeness Checklist:
    o Areas affected by regulations (e.g., marketing, manufacturing)
    o Specific operational adjustments required to comply
    o Analysis of impact on business timelines and costs

    """,
    f"""
    Identify key regulatory risks by market and industry, formulate mitigation strategies, and provide examples of successfully implemented risk management plans.

    Completeness Checklist:
    o Identification of key regulatory risks by market and industry
    o Mitigation strategies and risk management plans
    o Examples of successfully implemented mitigation measures

    """,
    f"""
    Implement quality standards such as ISO, maintain robust quality management systems, and ensure effective monitoring practices to guarantee product safety and quality.

    Completeness Checklist:
    o Quality standards adhered to (e.g., ISO 13485)
    o Quality management systems and monitoring practices
    o Examples of processes ensuring product safety and quality

    """,
    f"""
    Analyze emerging trends and future regulatory environments, predict anticipated regulatory changes and their implications, and prepare planned strategies for adapting to future regulations.

    Completeness Checklist:
    o Analysis of emerging trends and future regulatory environments
    o Anticipated regulatory changes and their implications
    o Planned strategies for adapting to future regulations

    """,
    f"""
    Outline current regulatory challenges impacting operations, address strategies developed to tackle these challenges, and explain proactive and reactive measures implemented to ensure compliance and mitigate impacts.

    Completeness Checklist:
    o Outline of current regulatory challenges impacting operations
    o Strategies developed to tackle these challenges
    o Proactive and reactive measures implemented

    """,
    f"""
    Set specific future regulatory goals, outline steps planned to achieve these goals, and establish metrics for measuring progress and success in regulatory compliance.

    Completeness Checklist:
    o Setting of specific future regulatory goals
    o Steps planned to achieve these goals
    o Metrics for measuring progress and success

    """,
    f"""
    Engage regulatory bodies through active consultation in product development stages, collaborate with authorities on compliance issues, and describe influence exerted on regulatory frameworks and guidance.

    Completeness Checklist:
    o Methods for engaging with regulatory bodies
    o Examples of collaboration with authorities for compliance
    o Influence exerted on regulatory frameworks and guidance

    """,
    # Consumer intelligence
    f"""
    Identify and analyze core demographic segments targeted, conduct a detailed comparative analysis of demographic preferences, provide insights into how demographics correlate with product choice, and present statistical data supporting demographic conclusions.

    Completeness Checklist:
    • Full breakdown of core demographic segments targeted
    • Detailed comparative analysis of demographic preferences
    • Insights into how demographics correlate with product choice
    • Statistical data supporting demographic conclusions

    """,
    f"""
    Describe lifestyle characteristics that align with the company, correlate attitudes, values, and interests through a comprehensive analysis, provide examples of how psychographics influence product adoption, and visually represent psychographic segmentation.

    Completeness Checklist:
    • Detailed description of lifestyle characteristics aligning with the company
    • Comprehensive analysis of attitudes, values, and interests
    • Examples of how psychographics influence product adoption
    • Visual representation of psychographic segmentation

    """,
    f"""
    Map the consumer purchase journey with an in-depth analysis, evaluate key factors influencing purchase decisions, provide a stage-by-stage breakdown of the decision-making process, and illustrate decision points with consumer actions through visualizations.

    Completeness Checklist:
    • In-depth analysis of the consumer purchase journey
    • Key factors influencing purchase decisions
    • Stage-by-stage breakdown of the decision-making process
    • Visualizations linking decision points with consumer actions

    """,
    f"""
    Identify key regulatory risks by market and industry, formulate mitigation strategies, and provide examples of successfully implemented risk management plans.

    Completeness Checklist:
    o Identification of key regulatory risks by market and industry
    o Mitigation strategies and risk management plans
    o Examples of successfully implemented mitigation measures

    """,
    f"""
    Identify key regulatory risks by market and industry, formulate mitigation strategies, and provide examples of successfully implemented risk management plans.
    Completeness Checklist:
    o	Identification of key regulatory risks by market and industry
    o	Mitigation strategies and risk management plans
    o	Examples of successfully implemented mitigation measures

    """,
    f"""
    Identify key regulatory risks by market and industry, formulate mitigation strategies, and provide examples of successfully implemented risk management plans.
    Completeness Checklist:
    o	Identification of key regulatory risks by market and industry
    o	Mitigation strategies and risk management plans
    o	Examples of successfully implemented mitigation measures

    """,
    f"""
    Identify key regulatory risks by market and industry, formulate mitigation strategies, and provide examples of successfully implemented risk management plans.
    Completeness Checklist:
    o	Identification of key regulatory risks by market and industry
    o	Mitigation strategies and risk management plans
    o	Examples of successfully implemented mitigation measures

    """,
    f"""
    Identify key regulatory risks by market and industry, formulate mitigation strategies, and provide examples of successfully implemented risk management plans.
    Completeness Checklist:
    o	Identification of key regulatory risks by market and industry
    o	Mitigation strategies and risk management plans
    o	Examples of successfully implemented mitigation measures

    """,
    f"""
    Identify key regulatory risks by market and industry, formulate mitigation strategies, and provide examples of successfully implemented risk management plans.
    Completeness Checklist:
    o	Identification of key regulatory risks by market and industry
    o	Mitigation strategies and risk management plans
    o	Examples of successfully implemented mitigation measures
    """,
]
