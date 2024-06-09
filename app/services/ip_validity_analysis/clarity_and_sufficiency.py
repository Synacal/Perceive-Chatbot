from typing import List
from app.core.azure_client import client


async def compare_clarity_and_sufficiency(
    patent_abstracts: List[str], answer_list: str
):
    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 40000 // len(patent_abstracts)
    truncated_abstracts = [
        abstract[:max_abstract_length] for abstract in patent_abstracts
    ]

    print("Truncated abstracts: ")

    # Perform clarity and sufficiency of disclosure assessment
    system_prompt = (
        "Given the following patent abstracts, please provide a detailed analysis of the clarity and sufficiency of disclosure "
        "of the invention described in the patent. Your analysis should include the following sections:\n\n"
        "Clarity and Sufficiency of Disclosure\n"
        "● Positive Features:\n"
        "  ○ Technical Specifications:\n"
        "    ■ Detail descriptions of the LEO satellites, beamforming technology, and dynamic routing algorithms to clarify operational aspects.\n"
        "  ○ Use Cases and Operational Scenarios:\n"
        "    ■ Illustrate how the system functions in various real-world scenarios to aid in understanding the technology's application and benefits.\n"
        "● Opinion:\n"
        "  - Provide an opinion on the clarity and sufficiency of the disclosure, including suggestions for ensuring that the documentation "
        "    provides enough detail for a skilled individual in the field to replicate the technology. This should include clear explanations "
        "    of the satellite network design, data routing methodologies, and the integration of beamforming technology.\n\n"
        "Additionally, provide a clarity and sufficiency score from 0 to 100, where 0 indicates no clarity/sufficiency and 100 indicates complete clarity/sufficiency."
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
