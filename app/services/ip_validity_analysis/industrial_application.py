from typing import List
from app.core.azure_client import client


async def compare_industrial_application(patent_abstracts: List[str], answer_list: str):
    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 40000 // len(patent_abstracts)
    truncated_abstracts = [
        abstract[:max_abstract_length] for abstract in patent_abstracts
    ]

    print("Truncated abstracts: ")

    # Perform industrial applicability and utility assessment
    system_prompt = (
        "Given the following patent abstracts, please provide a detailed analysis of the industrial applicability and utility "
        "of the invention described in the patent. Your analysis should include the following sections:\n\n"
        "Industrial Applicability\n"
        "● Positive Features:\n"
        "  ○ Versatile Use Cases:\n"
        "    ■ Describe various applications across key sectors.\n"
        "  ○ Focus on Global Connectivity:\n"
        "    ■ Explain the significance of wide coverage and global connectivity.\n"
        "● Opinion:\n"
        "  - Provide an opinion on the industrial applicability, including suggestions for enhancing the case for applicability.\n\n"
        "Additionally, provide an industrial applicability score and a utility score from 0 to 100, where 0 indicates no applicability/utility and 100 indicates complete applicability/utility."
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
