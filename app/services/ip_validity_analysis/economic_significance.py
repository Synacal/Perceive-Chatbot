from typing import List
from app.core.azure_client import client


async def compare_economic_significance(patent_abstracts: List[str], answer_list: str):
    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 40000 // len(patent_abstracts)
    truncated_abstracts = [
        abstract[:max_abstract_length] for abstract in patent_abstracts
    ]

    print("Truncated abstracts: ")

    # Perform economic significance assessment
    system_prompt = (
        "Given the following patent abstracts, please analyze the economic significance of OrbitNet's Satellite-based Internet Service. "
        "Focus on the positive features mentioned, such as global connectivity drive, infrastructure alternatives, operational efficiency, innovation, and job creation.\n\n"
        "Economic Significance:\n"
        "1. Evaluate the potential economic impact of OrbitNet's service, including market demand, cost-effectiveness, operational efficiency, job creation, and data as an asset.\n\n"
        "2. Provide a comprehensive analysis of the economic rationale for investing in OrbitNet's technology, including market analysis, ROI projections, case studies, sustainability, CSR, job creation, and data utilization.\n\n"
        "3. Additional Economic Angles:\n"
        "   - Consider exploring job creation opportunities and the value of data aggregation from internet usage patterns as additional economic indicators of OrbitNet's services.\n\n"
        "4. Patentability Criteria Scoring Rubric:\n"
        "   - Economic Significance Score (out of 10):\n"
        "      • 1-3 (Low): The economic impact is minimal, with limited market potential and few identifiable benefits.\n"
        "      • 4-6 (Medium): The technology shows potential for economic benefits, but requires further evidence and analysis to substantiate claims.\n"
        "      • 7-10 (High): The technology demonstrates significant economic potential, with strong market demand and clear, quantifiable benefits.\n"
        "5. Rationale:\n"
        "   - Provide a rationale for the assigned scores, detailing why the technology falls into the low, medium, or high category. For example: 'Strong market potential is indicated, but needs quantifiable evidence to support claims.'\n"
        "6. How to Improve:\n"
        "   - Suggest ways to improve the economic significance score. For example: 'Incorporate market research, economic analyses, and potential ROI studies to solidify the economic significance.'"
    )

    message_text = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": str(truncated_abstracts) + "\n\nAnswer: " + answer_list,
        },
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

        # Parse the response into a structured dictionary
        return content

    except Exception as e:
        print(f"Error generating novelty assessment: {e}")
        return None
