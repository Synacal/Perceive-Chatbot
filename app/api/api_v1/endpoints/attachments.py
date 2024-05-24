from fastapi import APIRouter, HTTPException
from psycopg2.extras import execute_values
from app.models.attachments import Attachment, attachmentAnswerList
from app.services.check_attachment import (
    get_pdf_content,
    get_questions,
    check_user_attachment,
    get_prompts,
    check_user_attachment_temp,
    find_question_number,
)
from app.services.add_attachment_answer import (
    add_attachment_answers,
    add_attachment_answer_content,
)

router = APIRouter()


@router.post("/add-attachment/")
async def add_attachment(attachment: Attachment):
    try:
        questions = get_questions(attachment.category_id)
        # content = get_pdf_content(attachment.attachment)
        content = f"""NextGen Innovations Inc. aims to revolutionize digital interaction through advanced augmented reality (AR) technologies. The mission centers on enhancing daily life by merging AR experiences seamlessly into physical reality, thereby providing individuals with enriched, instantaneous access to information and new communication avenues. This integration seeks to diminish the divide between digital and physical realms, offering innovative solutions that cater to both individual and collective needs across various sectors. 
NextGen Innovations has developed ARSight, a cutting-edge augmented reality platform designed to transform user engagement with their surroundings. Combining sophisticated AR glasses with a versatile software ecosystem, ARSight facilitates real-time overlays of information, immersive 3D interactions, and enriched learning environments. Tailored for both individual consumers and enterprises, ARSight is poised to redefine fields such as education, entertainment, and industrial operations by integrating digital enhancements into real-world contexts seamlessly. 
ARSight stands out through its advanced spatial computing algorithms and lightweight AR glasses, distinguishing itself with several innovative features: 
•	High-Resolution Display: Ensures crystal-clear imagery with minimal distortion for an immersive experience. 
•	Adaptive Learning: Utilizes user interaction data to personalize content delivery, enhancing learning and engagement. 
•	Energy Efficiency: Incorporates proprietary technology to significantly extend battery life, facilitating practical, all-day use. 
These innovations position ARSight as a pioneer in AR technology by offering unparalleled realtime environmental mapping, digital information overlay with minimal latency, and dynamic content adaptation, setting a new standard in user interaction and immersion within the augmented reality landscape. 
At NeuraWear, we utilize a blend of performance indicators to gauge our alignment with market dynamics. These include: 
•	Market Share Growth: We track changes in our market share quarterly, aiming for a 5% increase year-over-year, reflecting successful penetration and customer acquisition strategies. 
•	Customer Acquisition Cost (CAC): Our target CAC has been set at $120 per new user, optimized through targeted marketing and efficient sales funnel management. 
•	User Retention Rates: We aim for a retention rate of 80% over a 12-month period, indicating strong customer satisfaction and product relevance. 
 

"""

        prompts = get_prompts(attachment.category_id)
        result = await check_user_attachment(
            questions,
            prompts,
            content,
            attachment.session_id,
            attachment.user_id,
            attachment.category_id,
        )
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-attachment-temp/")
async def add_attachment_temp(attachment: Attachment):
    try:

        # content = get_pdf_content(attachment.attachment)
        content = f"""NextGen Innovations Inc. aims to revolutionize digital interaction through advanced augmented reality (AR) technologies. The mission centers on enhancing daily life by merging AR experiences seamlessly into physical reality, thereby providing individuals with enriched, instantaneous access to information and new communication avenues. This integration seeks to diminish the divide between digital and physical realms, offering innovative solutions that cater to both individual and collective needs across various sectors. 
            NextGen Innovations has developed ARSight, a cutting-edge augmented reality platform designed to transform user engagement with their surroundings. Combining sophisticated AR glasses with a versatile software ecosystem, ARSight facilitates real-time overlays of information, immersive 3D interactions, and enriched learning environments. Tailored for both individual consumers and enterprises, ARSight is poised to redefine fields such as education, entertainment, and industrial operations by integrating digital enhancements into real-world contexts seamlessly. 
            ARSight stands out through its advanced spatial computing algorithms and lightweight AR glasses, distinguishing itself with several innovative features: 
            •	High-Resolution Display: Ensures crystal-clear imagery with minimal distortion for an immersive experience. 
            •	Adaptive Learning: Utilizes user interaction data to personalize content delivery, enhancing learning and engagement. 
            •	Energy Efficiency: Incorporates proprietary technology to significantly extend battery life, facilitating practical, all-day use. 
            These innovations position ARSight as a pioneer in AR technology by offering unparalleled realtime environmental mapping, digital information overlay with minimal latency, and dynamic content adaptation, setting a new standard in user interaction and immersion within the augmented reality landscape. 
            At NeuraWear, we utilize a blend of performance indicators to gauge our alignment with market dynamics. These include: 
            •	Market Share Growth: We track changes in our market share quarterly, aiming for a 5% increase year-over-year, reflecting successful penetration and customer acquisition strategies. 
            •	Customer Acquisition Cost (CAC): Our target CAC has been set at $120 per new user, optimized through targeted marketing and efficient sales funnel management. 
            •	User Retention Rates: We aim for a retention rate of 80% over a 12-month period, indicating strong customer satisfaction and product relevance. 
            Product Innovation Cycle Times: Our goal is to shorten the cycle time to under 18 months from ideation to launch, ensuring we keep pace with technological advancements and consumer expectations. 
            NeuraWear utilizes a comprehensive analysis approach to adapt our strategies based on global market drivers and restraints: 
            •	Economic Indicators: We monitor global economic trends, such as inflation rates and consumer spending patterns, to forecast demand and adjust our pricing strategy accordingly. 
            •	Consumer Trends: Through ongoing market research, we track changes in consumer preferences and technology adoption rates, which guide our product development and feature prioritization. 
            Regulatory Changes: We keep abreast of new regulations in key markets, adapting our compliance strategies to ensure seamless market entry and sustained operations. 
            Recently, NeuraWear decided to invest heavily in AI and machine learning capabilities to enhance our wearable technology products. This strategic decision was driven by the projected market growth for AI-integrated wearables, which is expected to increase by 35% annually over the next five years. Our rationale was based on data indicating a significant consumer shift towards devices offering personalized health insights. By incorporating AI, we aim to provide superior functionality and customization, setting our products apart in a crowded market and aligning with consumer demand for highly personalized wearable technology. 
            NeuraWear targets health-conscious consumers aged 25 to 45, who are tech-savvy and have a disposable income level in the upper-middle class. This demographic is particularly inclined towards using technology to enhance their lifestyle and health, representing a significant portion of our customer base. 

        """

        questions = get_questions(attachment.category_id)
        prompts = get_prompts(attachment.category_id)

        uncompletedQuestions = []
        for i in range(len(questions)):
            result = await check_user_attachment_temp(
                questions[i],
                prompts[i],
                content,
                attachment.session_id,
                attachment.user_id,
                attachment.category_id,
            )
            if result["status"] == "false":
                question_number = find_question_number(questions[i])
                uncompletedQuestions.append(question_number)

        # await add_attachment_answer_content(
        #    content, attachment.session_id, attachment.user_id, attachment.category_id
        # )
        return uncompletedQuestions
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-attachment-answers/")
async def add_attachment_answer_list(answer_list: attachmentAnswerList):
    try:
        response_data = await add_attachment_answers(answer_list)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
