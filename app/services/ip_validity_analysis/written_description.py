from typing import List
from app.core.azure_client import client


async def compare_written_description(patent_abstracts: List[str], answer_list: str):
    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 40000 // len(patent_abstracts)
    truncated_abstracts = [
        abstract[:max_abstract_length] for abstract in patent_abstracts
    ]

    print("Truncated abstracts: ")

    # Perform written description assessment
    system_prompt = (
        "Given the following patent abstracts, please provide a detailed analysis of the written description of the invention described in the patent. "
        "Your analysis should include the following sections:\n\n"
        "Written Description\n"
        "● Positive Features:\n"
        "  ○ Technical Specifications:\n"
        "    ■ Evaluate the clarity and detail of the technical specifications provided. Are they sufficient to understand the invention?\n"
        "  ○ Use Cases and Operational Scenarios:\n"
        "    ■ Assess how well the use cases and operational scenarios are illustrated. Do they help in understanding the application and benefits of the invention?\n"
        "● Opinion:\n"
        "  - Provide an opinion on the overall clarity and sufficiency of the written description. Does the documentation provide enough detail for a skilled individual in the field to replicate the technology? "
        "Are the descriptions clear and detailed enough to communicate the invention effectively?\n\n"
        "Additionally, provide a clarity and sufficiency score from 0 to 100, where 0 indicates poor clarity and sufficiency and 100 indicates excellent clarity and sufficiency."
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
