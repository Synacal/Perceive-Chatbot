from typing import List
from app.core.azure_client import client


async def compare_utility(patent_abstracts: List[str], answer_list: str):
    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 40000 // len(patent_abstracts)
    truncated_abstracts = [
        abstract[:max_abstract_length] for abstract in patent_abstracts
    ]

    print("Truncated abstracts: ")

    ## Perform utility assessment
    system_prompt = (
        "Given the following patent abstracts, please provide a detailed analysis of the utility of the invention described in the patent. "
        "Your analysis should include the following sections:\n\n"
        "Utility\n"
        "1. Positive Features:\n"
        "  ○ Broadband Speeds in Remote Areas:\n"
        "    ■ Addresses the critical need for high-speed internet in locations where traditional infrastructure is not feasible.\n"
        "  ○ Reduced Latency:\n"
        "    ■ The LEO constellation significantly cuts down the latency, improving the user experience for applications requiring real-time data transfer.\n"
        "  ○ Resilience to Disasters:\n"
        "    ■ Offers a robust alternative when terrestrial networks are compromised due to natural or man-made disasters.\n"
        "2. Opinion:\n"
        "  - Provide an opinion on the utility of the service, emphasizing its essential communication capabilities in previously limited or non-existent areas. "
        "Detail how the technology impacts specific user experiences and services, such as telemedicine or remote education initiatives, to further illuminate its utility.\n\n"
        "3. Patentability Criteria Scoring Rubric:\n"
        "    - Utility Score (out of 10):\n"
        "        • 1-3 (Low): The technology offers minimal practical benefits, with unclear advantages over existing solutions.\n"
        "        • 4-6 (Medium): The technology provides clear but incremental improvements in utility or efficiency, offering tangible benefits.\n"
        "        • 7-10 (High): The technology greatly enhances utility, efficiency, or performance, presenting clear, substantial advantages over prior solutions.\n"
        "4. Rationale:\n"
        "   - Provide a rationale for the assigned scores, detailing why the technology falls into the low, medium, or high category. For example: 'The potential for widespread impact is evident, but application scenarios need fleshing out.'\n"
        "5. How to Improve:\n"
        "   - Suggest ways to improve the utility score. For example: 'Provide detailed examples of utility in various real-world applications, emphasizing measurable outcomes.'"
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
