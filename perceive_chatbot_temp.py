
import os
from openai import AzureOpenAI
import json



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
    print(content)
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
    
    system_prompt =["""The user answers the following question: "What is the full name of the company developing the AI-Driven Predictive Maintenance Solution?"
                    Then, check if the user prompt contains the following points:
                        "Evaluate the answer's level of detail regarding the technical description. Does it include operational mechanisms, implementation methods, and examples of real-world applications? If not, ask for specific details or real-world use cases that are missing."

                    The answer should be only in JSON format: 
                        {status: "true/false", question: "question"}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again.""",
                   """The user answers the following question: "Please provide a concise description of the AI-based Predictive Analytics for Healthcare technology."
                    Then, check if the user prompt contains the following points:
                        "Review the precision and specificity of patent claims in the answer. If claims are broad or ambiguous, request detailed explanations of the claims or specific examples that demonstrate their uniqueness."

                    The answer should be only in JSON format: 
                        {status: "true/false", question: "question"}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again.""",
                    """The user answers the following question: "Describe the technical aspects and unique features of the AI-based Predictive Analytics for Healthcare."
                    Then, check if the user prompt contains the following points:
                        "Check the answer for explanations of the technology's novelty and non-obvious aspects. If justifications are generic or absent, inquire about unique features or how the technology differs from existing solutions."

                    The answer should be only in JSON format: 
                        {status: "true/false", question: "question"}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again.""",
                    """The user answers the following question: "Can you tell me more about the specific patents or prior art you may have encountered during your research? What similarities or differences did you find?"
                    Then, check if the user prompt contains the following points:
                        "Assess if the answer clearly links the technology to specific industrial needs. If applicability is not evident, ask how the technology solves particular problems or meets market demands."

                    The answer should be only in JSON format: 
                        {status: "true/false", question: "question"}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again.""",
                    """The user answers the following question: "How does the AI-based Predictive Analytics for Healthcare meet the criteria of novelty in its field? "
                    Then, check if the user prompt contains the following points:
                        Evaluate the answer's level of detail regarding the technical description. Does it include operational mechanisms, implementation methods, and examples of real-world applications? If not, ask for specific details or real-world use cases that are missing."

                    The answer should be only in JSON format: 
                        {status: "true/false", question: "question"}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again."""
                    """The user answers the following question: "Can you explain why the features of the AI-based Predictive Analytics for Healthcare are considered non-obvious to someone skilled in the field?"
                    Then, check if the user prompt contains the following points:
                        "Ensure the answer includes integration and implementation information. If details are lacking, probe for how the technology integrates with existing systems or any proprietary processes it utilizes."

                    The answer should be only in JSON format: 
                        {status: "true/false", question: "question"}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again.""",
                    """The user answers the following question: "How is the AI-based Predictive Analytics for Healthcare applicable to industrial needs in its domain?"
                    Then, check if the user prompt contains the following points:
                        "Verify that the answer discusses strategic considerations for patent filings. If not, question the rationale behind chosen markets and the strategy for securing IP rights."

                    The answer should be only in JSON format: 
                        {status: "true/false", question: "question"}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again.""",
                    """The user answers the following question: "What is your strategy for patent filing, including geographies and patent offices?"
                    Then, check if the user prompt contains the following points:
                        "Confirm comparisons with prior art or existing patents are made in the answer. If superficial, ask for detailed analyses on how the technology advances beyond or diverges from known solutions."

                    The answer should be only in JSON format: 
                        {status: "true/false", question: "question"}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again.""",
                   """The user answers the following question: "How have you ensured enablement in the patent application for the AI-based Predictive Analytics for Healthcare?"
                    Then, check if the user prompt contains the following points:
                        "For each incomplete response, generate follow-up questions that directly address the gaps, including requests for more detailed descriptions, clarification of technical terms, specific examples of technology application, and justifications for novelty and non-obviousness."

                    The answer should be only in JSON format: 
                        {status: "true/false", question: "question"}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again.""",
                    """The user answers the following question: "How have you ensured the definiteness of claims in your patent application for the AI-based Predictive Analytics for Healthcare?"
                    Then, check if the user prompt contains the following points:
                        Evaluate the answer's level of detail regarding the technical description. Does it include operational mechanisms, implementation methods, and examples of real-world applications? If not, ask for specific details or real-world use cases that are missing."

                    The answer should be only in JSON format: 
                        {status: "true/false", question: "question"}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again.""",
                    """The user answers the following question: "Can you provide the exact claims that will be present in the patent application for your AI-based Predictive Analytics solution?"
                    Then, check if the user prompt contains the following points:
                        Evaluate the answer's level of detail regarding the technical description. Does it include operational mechanisms, implementation methods, and examples of real-world applications? If not, ask for specific details or real-world use cases that are missing."

                    The answer should be only in JSON format: 
                        {status: "true/false", question: "question"}
                    status and question json data must be included.
                    
                    The status should be returned "true" as JSON status and any question must be returned as question JSON, only if the user request contains all the above facts. If not or you cant understand, the status should be given as "false". If "false", to get a complete answer, a question must be returned from the question JSON again."""
                    ]

    for idx, question in enumerate(questions):
        print(question)

        while True:
            user_input = input("You: ")
            message_text = [{"role": "system", "content": system_prompt[idx]},{"role": "user", "content": user_input}]
            generated_content = generate_completion(client, message_text)

            try:
                # Parse the string into a dictionary
                generated_content_json = json.loads(generated_content)
                question = generated_content_json["question"]
                status = generated_content_json["status"]

            except json.JSONDecodeError as e:
                print("Error decoding JSON. Try again:", e)
                continue  # Skip further processing if JSON decoding fails


            if status== "True" or status =='true':
                print("Answer is completed! Answer the next question.\n")
                break
            elif status=="False" or status == 'false':
                print(question,"\n")
                continue
            else:
                print("system error\n")
                #return
        

if __name__ == "__main__":
    main()
