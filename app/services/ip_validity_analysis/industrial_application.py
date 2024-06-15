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
        "1. Positive Features:\n"
        "  ○ Versatile Use Cases:\n"
        "    ■ Describe various applications across key sectors.\n"
        "  ○ Focus on Global Connectivity:\n"
        "    ■ Explain the significance of wide coverage and global connectivity.\n"
        "2. Opinion:\n"
        "  - Provide an opinion on the industrial applicability, including suggestions for enhancing the case for applicability.\n\n"
        "3. Patentability Criteria Scoring Rubric:\n"
        "    - Industrial Applicability Score (out of 10):\n"
        "        • 1-3 (Low): The technology has limited or niche applicability, with few practical uses in existing industries.\n"
        "        • 4-6 (Medium): The technology is applicable in several industries, offering solutions to known problems but may face challenges in widespread adoption or implementation.\n"
        "        • 7-10 (High): The technology has broad industry applicability, with potential to significantly impact multiple sectors by addressing critical challenges or improving efficiency and productivity.\n"
        "    - Utility Score (out of 10):\n"
        "        • 1-3 (Low): The technology offers minimal utility, with limited practical applications or benefits.\n"
        "        • 4-6 (Medium): The technology provides moderate utility, solving some problems but may not be widely adopted due to existing alternatives or limitations.\n"
        "        • 7-10 (High): The technology offers high utility, addressing critical needs and providing significant practical benefits in its application.\n"
        "4. Rationale:\n"
        "   - Provide a rationale for the assigned scores, detailing why the technology falls into the low, medium, or high category. For example: 'The technology addresses significant connectivity challenges, demonstrating strong market and practical relevance.'\n"
        "5. How to Improve:\n"
        "   - Suggest ways to improve the industrial applicability and utility scores. For example: 'Expand on specific case studies showing the technology in action across different sectors to illustrate direct impacts.'"
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
        return {content}

    except Exception as e:
        print(f"Error generating novelty assessment: {e}")
        return None
