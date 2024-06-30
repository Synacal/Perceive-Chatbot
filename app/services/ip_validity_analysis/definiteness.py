from typing import List
from app.core.azure_client import client


async def compare_definiteness(patent_abstracts: List[str], answer_list: str):
    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 40000 // len(patent_abstracts)
    truncated_abstracts = [
        abstract[:max_abstract_length] for abstract in patent_abstracts
    ]

    print("Truncated abstracts: ")

    # Perform definiteness assessment
    system_prompt = (
        "Given the following patent abstracts, please analyze the definiteness of the claims presented in the patents. "
        "Your analysis should focus on the clarity and precision of the claims, ensuring that the boundaries of the patent rights are well-defined and there is no ambiguity in what the patent covers.\n\n"
        "Definiteness (35 U.S.C. § 112(b)):\n"
        "Claims must be clear and precise. The 'Scope & Definition' ensure that the boundaries of the patent rights are well-defined, preventing ambiguity in what the patent covers.\n\n"
        "Evaluate each patent's claims for clarity, precision, and absence of ambiguity. Provide an assessment of the definiteness of each patent's claims and an overall score from 0 to 100, where 0 indicates poor definiteness and 100 indicates excellent definiteness."
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
