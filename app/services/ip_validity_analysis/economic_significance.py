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
        "Evaluate the potential economic impact of OrbitNet's service, including market demand, cost-effectiveness, operational efficiency, job creation, and data as an asset.\n\n"
        "Provide a comprehensive analysis of the economic rationale for investing in OrbitNet's technology, including market analysis, ROI projections, case studies, sustainability, CSR, job creation, and data utilization.\n\n"
        "Additional Economic Angles:\n"
        "Consider exploring job creation opportunities and the value of data aggregation from internet usage patterns as additional economic indicators of OrbitNet's services.\n\n"
        "Answer with detailed insights and analysis based on the patent abstracts and provided answer list."
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

        print("Novelty assessment completion: ")

        content = completion.choices[0].message.content

        # Parse the response into a structured dictionary
        return {"novelty_assessment": content}

    except Exception as e:
        print(f"Error generating novelty assessment: {e}")
        return None
