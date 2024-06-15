from typing import List
from app.core.azure_client import client


async def compare_non_obviousness(patent_abstracts: List[str], answer_list: str):
    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 40000 // len(patent_abstracts)
    truncated_abstracts = [
        abstract[:max_abstract_length] for abstract in patent_abstracts
    ]

    print("Truncated abstracts: ")

    # Perform non-obviousness assessment
    system_prompt = (
        "Given the following patent abstracts, please provide a detailed analysis of the non-obviousness (inventive step) "
        "of the invention described in the patent. Your analysis should include the following sections:\n\n"
        "Non-Obviousness (Inventive Step)\n"
        "● Positive Features:\n"
        "  ○ Innovative Integration of Technologies:\n"
        "    ■ Detail any significant engineering achievements that address multiple challenges simultaneously.\n"
        "  ○ Sophisticated Network Management:\n"
        "    ■ Explain any sophisticated approaches to network management introduced by the invention.\n"
        "  ○ Targeted Beamforming Application:\n"
        "    ■ Describe any complex technical challenges overcome in the development.\n"
        "● Opinion:\n"
        "  - Provide an opinion on the non-obviousness of the technology, highlighting substantial departures from conventional solutions and creative problem-solving.\n"
        "● Caveats:\n"
        "  ○ Prior Art and Comparative Analysis:\n"
        "    ■ Note the need to evaluate the inventive step against similar technologies.\n"
        "  ○ Technical Documentation and Challenges:\n"
        "    ■ Suggest documenting specific engineering challenges and solutions.\n"
        "  ○ Comparison with Existing Solutions:\n"
        "    ■ Emphasize the need to show how the technology surpasses existing solutions in solving problems.\n\n"
        "Additionally, provide a non-obviousness score from 1 to 10, with the following rubric:\n"
        "4. Patentability Criteria Scoring Rubric:\n"
        "    - Non-Obviousness Score (out of 10):\n"
        "        • 1-3 (Low): The technology's advancements are obvious to professionals in the field and represent logical next steps rather than inventive leaps.\n"
        "        • 4-6 (Medium): The technology demonstrates an inventive step that may not be immediately obvious, incorporating unique approaches or solving problems in unexpected ways.\n"
        "        • 7-10 (High): The technology's development required overcoming significant technical challenges, offering solutions that are not intuitive or straightforward, showcasing a high degree of creativity and innovation.\n"
        "5. Rationale:\n"
        "   - Provide a rationale for the assigned score, detailing why the technology falls into the low, medium, or high category. For example: 'The combination of technologies suggests an inventive step, but detailed innovation specifics are crucial.'\n"
        "6. How to Improve:\n"
        "   - Suggest ways to improve the non-obviousness score. For example: 'Document and detail the unique engineering challenges and solutions developed, particularly in dynamic routing.'"
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
