from app.models.ip_license_process import PatentResult, PatentList, PatentData
from typing import List
from fastapi import APIRouter, HTTPException, Depends
import json
from app.core.azure_client import client


async def prompt1(summary: str, patent_data: List[PatentData]):
    try:
        additional_info = f"""
            Historical Analysis of Successful IP Licensing Strategies
            Please provide a detailed historical analysis of successful IP licensing strategies, focusing on the orthodontics technology sector. Include the following aspects.

            Innovation and Technological Differentiation:
                Highlight the importance of unique and innovative technologies.
                Discuss the value of patents with broad claims.
                Explain the significance of continuing innovation.

            Market Demand and Applicability:
                Address how successful IP licenses meet significant unmet market needs.
                Emphasize the importance of aligning with market trends and regulatory compliance.

            Strong Patent Protection:
                Discuss the benefits of comprehensive patent coverage in key global markets.
                Explain the role of defensive publications in maintaining competitive advantage.

            Strategic Partnerships:
                Highlight the value of collaborations with industry leaders.
                Discuss the importance of technology integration with existing systems in the orthodontics field.
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
