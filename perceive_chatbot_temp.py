
import os
from openai import AzureOpenAI



client = AzureOpenAI(
  azure_endpoint = "https://chatbotmedipredict.openai.azure.com/", 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="2024-02-15-preview"
)


def generate_completion(client, message_text, model="gpt-35-turbo", temperature=0.7, max_tokens=800, top_p=0.95, frequency_penalty=0, presence_penalty=0, stop=None):
    completion = client.chat.completions.create(
        model=model,
        messages=message_text,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )

    content = completion.choices[0].message.content
    #print(content)
    return content

def main():
    questions=["1. What is the full name of the company developing the AI-based Predictive Analytics for Healthcare?",
               "2. Please provide a concise description of the AI-based Predictive Analytics for Healthcare technology.",
               "3. Describe the technical aspects and unique features of the AI-based Predictive Analytics for Healthcare.",
               "4. Can you tell me more about the specific patents or prior art you may have encountered during your research? What similarities or differences did you find?",
               "5. How does the AI-based Predictive Analytics for Healthcare meet the criteria of novelty in its field? ",
               "6. Can you explain why the features of the AI-based Predictive Analytics for Healthcare are considered non-obvious to someone skilled in the field? ",
               "7. How is the AI-based Predictive Analytics for Healthcare applicable to industrial needs in its domain? ",
               "8. What is your strategy for patent filing, including geographies and patent offices?",
               "9. How have you ensured enablement in the patent application for the AI-based Predictive Analytics for Healthcare? ",
               "10. How have you ensured the definiteness of claims in your patent application for the AI-based Predictive Analytics for Healthcare? ",
               "11. Can you provide the exact claims that will be present in the patent application for your AI-based Predictive Analytics solution?"]
    
    system_prompt =["you should check User Prompt that completed or not. User Prompt should include these points.\" The organization behind AI-based predictive analytics for healthcare is MediPredict Solutions. At MediPredict Solutions, we are dedicated to transforming healthcare through the power of artificial intelligence. Our flagship AI-based predictive The analytics platform is designed to revolutionize patient care by providing early warnings, personalized treatment insights and a deeper understanding of disease progression. Our mission is to provide healthcare with cutting-edge tools to more accurately predict health outcomes and improve the overall quality of care. Empowering Service Professionals.\" It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. ",
                    " you should check User Prompt that completed or not. User Prompt should include these points.     Our AI-based Predictive Analytics for Healthcare technology utilizes advanced machine learning algorithms and big data analytics to accurately forecast health outcomes. By analyzing vast datasets, including EHRs, genetic data, and real-time monitoring inputs, it identifies risk patterns and anticipates health issues before they escalate. Incorporating NLP allows for the interpretation of unstructured medical notes, enhancing prediction accuracy and facilitating personalized healthcare interventions.              It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. ",
                    " you should check User Prompt that completed or not. User Prompt should include these points.         Our Predictive Analytics for Healthcare platform leverages advanced AI technologies, including machine learning algorithms such as deep learning, neural networks, and natural language processing. These algorithms are integrated with vast amounts of healthcare data, including electronic health records, medical imaging data, genomic data, and patient-generated data from wearable devices. By analyzing this data, our platform can accurately predict diseases, identify risk factors, and suggest personalized treatment plans for patients. One of our unique features is real-time data analysis, allowing healthcare providers to make timely decisions based on the most up-to-date information. Additionally, our platform can seamlessly integrate with wearable technology, enabling continuous monitoring and feedback for patients outside of traditional healthcare settings. Overall, our AI-based Predictive Analytics for Healthcare offers a comprehensive solution that empowers healthcare professionals to deliver proactive and personalized care to their patients.         It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. ",
                    " you should check User Prompt that completed or not. User Prompt should include these points.        During our research, we identified several patents related to AI in healthcare, such as Patent ID XYZ123, which covers algorithms for predicting cardiovascular diseases. Our platform differentiates itself by employing a broader spectrum of machine learning models and a more sophisticated data integration approach, allowing for comprehensive health predictions across multiple conditions. Additionally, our use of NLP to parse and utilize unstructured data from medical records introduces a new layer of depth to predictive analytics in healthcare.          It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. ",
                    " you should check User Prompt that completed or not. User Prompt should include these points.       Our AI-based Predictive Analytics platform introduces novelty by integrating a wide array of machine learning models with a sophisticated data fusion approach, enabling it to consider a broader range of health indicators and predict multiple conditions simultaneously. The incorporation of NLP to interpret unstructured medical data further enhances its novelty, offering deeper insights and more accurate predictions than previously possible.           It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. ",
                    " you should check User Prompt that completed or not. User Prompt should include these points.        The non-obviousness of our solution lies in its unique combination of diverse machine learning algorithms and its ability to seamlessly integrate and analyze both structured and unstructured healthcare data. This comprehensive approach, coupled with real-time analysis capabilities and the application of NLP for depth in data interpretation, represents a significant leap forward in predictive healthcare analytics.          It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. ",
                    " you should check User Prompt that completed or not. User Prompt should include these points.         Our AI-based Predictive Analytics platform meets critical industrial needs by enabling early disease detection, personalized treatment plans, and improved patient outcomes. It serves as a powerful tool for healthcare providers, insurance companies, and research institutions by offering detailed risk assessments and facilitating data-driven decision-making. Its versatility makes it applicable across various healthcare settings, including hospitals, clinics, and remote patient monitoring systems.         It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. "
                    " you should check User Prompt that completed or not. User Prompt should include these points.          Our patent filing strategy focuses on key geographical markets where the demand for AI in healthcare is notably high and where the regulatory environment is conducive to the adoption of such technologies. We prioritize regions such as the United States, European Union, China, and Japan due to their large healthcare markets and supportive regulatory frameworks for innovation. These regions also represent diverse populations and healthcare systems, allowing us to address a broad range of healthcare challenges and opportunities. Additionally, we may consider filing patents in other countries or regions based on emerging trends, market dynamics, and strategic partnerships. Overall, our goal is to protect our intellectual property globally while aligning with the needs and priorities of the healthcare industry in various geographies.        It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. ",
                    " you should check User Prompt that completed or not. User Prompt should include these points.       To ensure enablement in our patent application, we've provided comprehensive details on our AI algorithms, including machine learning models and NLP techniques, along with their implementation in analyzing healthcare data. Detailed descriptions, code snippets, and workflow diagrams are included to ensure that a person skilled in the art can replicate our technology effectively.           It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. ",
                    " you should check User Prompt that completed or not. User Prompt should include these points.        Our patent claims are carefully crafted to be clear, concise, and supported by the detailed technology descriptions in the application. We specifically highlight the unique aspects of our platform, such as the integration of diverse AI models and the novel use of NLP for medical data analysis, to clearly define the invention's scope and secure robust IP protection.          It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. ",
                    " you should check User Prompt that completed or not. User Prompt should include these points.         In our patent application for the AI-based Predictive Analytics platform, we've outlined several claims to comprehensively protect our innovative technology. Claim 1 details a method for predicting health outcomes using a combination of machine learning algorithms, specifying the process of data collection, analysis, and outcome prediction. Claim 2 focuses on the application of NLP to extract meaningful information from unstructured medical data, outlining steps for data parsing, interpretation, and integration into the predictive model. Additional claims cover the real-time analysis of health monitoring data, the integration of genetic information for personalized health predictions, and the use of our platform for specific healthcare applications like disease prevention and treatment optimization. These claims are designed to ensure broad and effective protection for our pioneering healthcare analytics technology         It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. "]

    for idx, question in enumerate(questions):
        print(question)

        while True:
            user_input = input("You: ")
            message_text = [{"role": "system", "content": system_prompt[idx]},{"role": "user", "content": user_input}]
            generated_content = generate_completion(client, message_text)

            if generated_content== "YES":
                print("Answer is completed! Answer the next question.\n")
                break
            elif generated_content=="NO":
                print("Answer is uncompleted! Answer again.\n")
                continue
            else:
                print("system error\n")
                #return
        

if __name__ == "__main__":
    main()
