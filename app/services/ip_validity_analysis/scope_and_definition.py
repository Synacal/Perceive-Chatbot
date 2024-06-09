from typing import List
from app.core.azure_client import client


async def compare_scope_and_definition(patent_abstracts: List[str], answer_list: str):
    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 40000 // len(patent_abstracts)
    truncated_abstracts = [
        abstract[:max_abstract_length] for abstract in patent_abstracts
    ]

    print("Truncated abstracts: ")

    # Perform scope and definiteness assessment
    system_prompt = (
        "Given the following patent abstracts, please provide a detailed analysis of the scope and definiteness of the claims in the patent. "
        "Your analysis should include the following sections:\n\n"
        "Scope and Definiteness of Claims\n"
        "● Positive Features:\n"
        "  ○ Precision in Claims:\n"
        "    ■ Focus on the unique aspects of the technology, such as the integration of beamforming with a LEO satellite constellation for dynamic internet service delivery.\n"
        "  ○ Legal Expertise:\n"
        "    ■ Involvement of patent professionals in crafting the claims to ensure they are both broad enough to provide substantial protection and specific enough to be defensible.\n"
        "● Opinion:\n"
        "  - Provide an opinion on the scope and definiteness of the claims, emphasizing how they distinguish the technology from prior art and ensure adequate legal protection. "
        "The claims should be structured to cover the novel aspects of the technology—particularly the use of LEO satellites, advanced beamforming, and dynamic routing—in a way that is clear, specific, and supported by the detailed description of the invention. "
        "A thorough prior art search and analysis will be essential in crafting these claims to clearly delineate the innovative steps and technical solutions provided by the technology.\n\n"
        "Additionally, provide a scope and definiteness score from 0 to 100, where 0 indicates poor scope and definiteness and 100 indicates excellent scope and definiteness."
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
