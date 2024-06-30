from typing import List
from app.core.azure_client import client


async def compare_novelty(patent_abstracts: List[str], answer_list: str):
    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 120000 // len(patent_abstracts)
    truncated_abstracts = [
        abstract[:max_abstract_length] for abstract in patent_abstracts
    ]

    print("Truncated abstracts: ")

    # Perform novelty assessment
    system_prompt = (
        "Given the following patent abstracts, please provide an analysis of the novelty of the invention described in the patent. "
        "Your analysis should include the following sections:\n"
        "1. Positive Features:\n"
        "    a. Innovative Integration of Technologies:\n"
        "        - Detail any significant engineering achievements that address multiple challenges.\n"
        "    b. Sophisticated Network Management:\n"
        "        - Explain any sophisticated approaches to network management introduced by the invention.\n"
        "    c. Targeted Beamforming Application:\n"
        "        - Describe any complex technical challenges overcome in the development.\n"
        "2. Opinion:\n"
        "    - Provide an opinion on the non-obviousness of the technology, highlighting substantial departures from conventional solutions and creative problem-solving.\n"
        "3. Caveats:\n"
        "    a. Prior Art and Comparative Analysis:\n"
        "        - Note the need to evaluate the inventive step against similar technologies.\n"
        "    b. Technical Documentation and Challenges:\n"
        "        - Suggest documenting specific engineering challenges and solutions.\n"
        "    c. Comparison with Existing Solutions:\n"
        "        - Emphasize the need to show how the technology surpasses existing solutions in solving problems.\n"
        "4. Patentability Criteria Scoring Rubric:\n"
        "    - Novelty Score (out of 10):\n"
        "        • 1-3 (Low): The technology has significant overlaps with existing technologies or prior art, offering no new distinct features.\n"
        "        • 4-6 (Medium): The technology presents minor improvements over existing solutions, with some new features or uses that are not widely documented in prior art.\n"
        "        • 7-10 (High): The technology introduces groundbreaking features or applications not seen in any prior art, setting a new benchmark for innovation in its field.\n"
        "5. Rationale:\n"
        "    - Provide a rationale for the assigned score, detailing why the technology falls into the low, medium, or high category. For example: 'Integrating LEO satellites with advanced beamforming and dynamic routing presents a unique approach.'\n"
        "6. How to Improve:\n"
        "    - Suggest ways to improve the patentability score. For example: 'Conduct a comprehensive prior art search focusing on satellite communication technologies to ensure uniqueness.'"
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
        return content

    except Exception as e:
        print(f"Error generating novelty assessment: {e}")
        return None
