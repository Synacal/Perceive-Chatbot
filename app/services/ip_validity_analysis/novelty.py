from typing import List
from app.core.azure_client import client


async def compare_novelty(patent_abstracts: List[str], answer_list: str):
    # Truncate abstracts to avoid exceeding token limits
    max_abstract_length = 40000 // len(patent_abstracts)
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
        "Additionally, provide a novelty score from 0 to 100, where 0 indicates no novelty and 100 indicates complete novelty."
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
