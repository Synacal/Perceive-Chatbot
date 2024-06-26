from app.models.ip_license_process import PatentResult, PatentList, PatentData
from typing import List
from fastapi import APIRouter, HTTPException, Depends
import json
from app.core.azure_client import client


async def prompt4(summary: str, patent_data: List[PatentData]):
    try:
        additional_info = f"""
            Analyzing Top Assignors in the Orthodontics Technology Sector
            Please identify the top assignors in the orthodontics technology sector. For each assignor, provide:

            Assignor Details:
                Name of the assignor.
                Overview of their contributions.

            Significance:
                Analysis of their most significant patents and innovations.
                Impact of their work on the market and industry.

            Market Impact:
                How their contributions have influenced market trends and technology development.

            """

        system_prompt = f"""
            An IP Licensing Strategy must be developed focusing on the following background information and output requirements mentioned. After this prompt separate prompts will be prompted describing how each section of the IP Licensing Strategy must be generated. 


            Background Information:{summary}
            Data on Patents:{patent_data}

            {additional_info}

            Output Requirements:
                The report should be insightful, highly accurate, and data-centric, naming specific patents and entities.
                Structure the findings in a logical format with clear headings and subheadings.
                Include a section for each relevant entity and patent found, detailing their relevance, potential impact on BRIUS's technology, and implications for market strategy.

            Note: don't make something vague, make it all clear

            """
        message_text = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": str(patent_data),
            },
        ]
        try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=message_text,
                temperature=0.7,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
            )

            content = completion.choices[0].message.content

            # Parse the response into a structured dictionary if it's in JSON format
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return content
        except Exception as e:
            print(f"Error generating novelty assessment: {e}")
            return None
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
