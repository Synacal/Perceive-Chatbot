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
        "1. Positive Features:\n"
        "   a. Precision in Claims:\n"
        "      - Focus on the unique aspects of the technology, such as the integration of beamforming with a LEO satellite constellation for dynamic internet service delivery.\n"
        "   b. Legal Expertise:\n"
        "      - Involvement of patent professionals in crafting the claims to ensure they are both broad enough to provide substantial protection and specific enough to be defensible.\n"
        "2. Opinion:\n"
        "   - Provide an opinion on the scope and definiteness of the claims, emphasizing how they distinguish the technology from prior art and ensure adequate legal protection. "
        "     The claims should be structured to cover the novel aspects of the technology—particularly the use of LEO satellites, advanced beamforming, and dynamic routing—in a way that is clear, specific, and supported by the detailed description of the invention. "
        "     A thorough prior art search and analysis will be essential in crafting these claims to clearly delineate the innovative steps and technical solutions provided by the technology.\n\n"
        "3. Patentability Criteria Scoring Rubric:\n"
        "   - Scope and Definiteness Score (out of 10):\n"
        "      • 1-3 (Low): The claims are vague or overly broad, making it difficult to discern the unique aspects of the invention or to enforce the patent.\n"
        "      • 4-6 (Medium): The claims are somewhat clear but may include ambiguities or lack specificity in certain areas, potentially weakening the patent's enforceability.\n"
        "      • 7-10 (High): The claims are clear, specific, and well-defined, covering the innovative aspects of the technology in a way that is both broad enough to provide substantial protection and specific enough to be defensible.\n"
        "4. Rationale:\n"
        "   - Provide a rationale for the assigned scores, detailing why the technology falls into the low, medium, or high category. For example: 'Without precise claim language, the potential for broad protection is uncertain.'\n"
        "5. How to Improve:\n"
        "   - Suggest ways to improve the scope and definiteness score. For example: 'Collaborate with patent professionals to refine the scope and specificity of claims, ensuring they cover key innovations.'"
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
