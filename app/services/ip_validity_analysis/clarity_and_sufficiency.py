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
        "1 Positive Features:\n"
        "  ○ Technical Specifications:\n"
        "    ■ Detail descriptions of the LEO satellites, beamforming technology, and dynamic routing algorithms to clarify operational aspects.\n"
        "  ○ Use Cases and Operational Scenarios:\n"
        "    ■ Illustrate how the system functions in various real-world scenarios to aid in understanding the technology's application and benefits.\n"
        "2 Opinion:\n"
        "  - Provide an opinion on the clarity and sufficiency of the disclosure, including suggestions for ensuring that the documentation "
        "    provides enough detail for a skilled individual in the field to replicate the technology. This should include clear explanations "
        "    of the satellite network design, data routing methodologies, and the integration of beamforming technology.\n\n"
        "3. Patentability Criteria Scoring Rubric:\n"
        "    - Clarity and Sufficiency of Disclosure Score (out of 10):\n"
        "        • 1-3 (Low): The documentation lacks essential details, leaving significant ambiguities about the technology's functionality or implementation.\n"
        "        • 4-6 (Medium): The documentation is generally clear, with some areas lacking in detail but overall providing enough information for understanding the technology.\n"
        "        • 7-10 (High): The documentation is exceptionally detailed and clear, thoroughly describing the technology, its operation, and implementation, enabling skilled individuals to replicate or understand it fully.\n"
        "4. Rationale:\n"
        "   - Provide a rationale for the assigned scores, detailing why the technology falls into the low, medium, or high category. For example: 'The disclosure provides a good overview but lacks in-depth technical details.'\n"
        "5. How to Improve:\n"
        "   - Suggest ways to improve the clarity and sufficiency score. For example: 'Enhance the patent application with detailed technical specifications, diagrams, and clear operational descriptions.'"
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
