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
        "1. Positive Features:\n"
        "   a. Comprehensive Description of Technology Components:\n"
        "      - Include sufficient details about the design and function of the satellite constellation, network management, and user terminals.\n"
        "   b. Implementation Guidelines:\n"
        "      - Guidelines on deploying and managing the satellite network to enable replication by those skilled in the art.\n"
        "2. Opinion:\n"
        "   - Provide an opinion on the enablement based on the completeness of the technical descriptions and the feasibility of replicating the technology based on the provided information. "
        "     Documenting the resolution of specific engineering challenges encountered during development can strengthen the case for enablement by showcasing the practical application of the theoretical aspects described.\n\n"
        "3. Patentability Criteria Scoring Rubric:\n"
        "   - Enablement Score (out of 10):\n"
        "      • 1-3 (Low): The information provided is insufficient for a professional in the field to replicate or fully utilize the technology without substantial additional research or experimentation.\n"
        "      • 4-6 (Medium): The technology can be replicated or utilized by professionals in the field with some effort, although certain aspects may require further clarification or experimentation.\n"
        "      • 7-10 (High): The documentation provides a complete, detailed guide that enables any skilled professional to replicate or utilize the technology without additional invention or significant effort.\n"
        "4. Rationale:\n"
        "   - Provide a rationale for the assigned scores, detailing why the technology falls into the low, medium, or high category. For example: 'Indicates an understanding of necessary detail, yet the description may not fully enable replication.'\n"
        "5. How to Improve:\n"
        "   - Suggest ways to improve the enablement score. For example: 'Include step-by-step processes, specific examples of the technology in use, and detailed component descriptions.'"
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
        return {content}

    except Exception as e:
        print(f"Error generating novelty assessment: {e}")
        return None
