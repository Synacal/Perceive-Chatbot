from typing import List
from app.core.azure_client import client


async def compare_enablement(patent_abstracts: List[str], answer_list: str):
    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 40000 // len(patent_abstracts)
    truncated_abstracts = [
        abstract[:max_abstract_length] for abstract in patent_abstracts
    ]

    print("Truncated abstracts: ")

    # Perform enablement assessment
    system_prompt = (
        "Given the following patent abstracts, please provide a detailed analysis of the enablement of the invention described in the patent. "
        "Your analysis should include the following sections:\n\n"
        "Enablement\n"
        "● Positive Features:\n"
        "  ○ Comprehensive Description of Technology Components:\n"
        "    ■ Include sufficient details about the design and function of the satellite constellation, network management, and user terminals.\n"
        "  ○ Implementation Guidelines:\n"
        "    ■ Guidelines on deploying and managing the satellite network to enable replication by those skilled in the art.\n"
        "● Opinion:\n"
        "  - Provide an opinion on the enablement based on the completeness of the technical descriptions and the feasibility of replicating the technology based on the provided information. "
        "Documenting the resolution of specific engineering challenges encountered during development can strengthen the case for enablement by showcasing the practical application of the theoretical aspects described.\n\n"
        "Additionally, provide an enablement score from 0 to 100, where 0 indicates no enablement and 100 indicates complete enablement."
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
