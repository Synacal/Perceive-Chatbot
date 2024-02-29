
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
    print(content)
    return content







def main():
    questions=["1. What is the full name of the company developing the AI-based Predictive Analytics for Healthcare?","2. Please provide a concise description of the AI-based Predictive Analytics for Healthcare technology.","3.	Can you tell me more about the specific patents or prior art you may have encountered during your research? What similarities or differences did you find?"]

    for i in questions:
        
        print(i)

        if i == "1. What is the full name of the company developing the AI-based Predictive Analytics for Healthcare?":
            while True:
                user_input = input("You: ")
                message_text = [{"role": "system", "content": " you should check User Prompt that completed or not. User Prompt should include these points.\" The organization behind AI-based predictive analytics for healthcare is MediPredict Solutions. At MediPredict Solutions, we are dedicated to transforming healthcare through the power of artificial intelligence. Our flagship AI-based predictive The analytics platform is designed to revolutionize patient care by providing early warnings, personalized treatment insights and a deeper understanding of disease progression. Our mission is to provide healthcare with cutting-edge tools to more accurately predict health outcomes and improve the overall quality of care. Empowering Service Professionals.\" It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. "},{"role": "user", "content": user_input}]
                generated_content = generate_completion(client, message_text)

                if generated_content== "YES":
                    print("Answer is completed! Answer the next question.\n")
                    break
                elif generated_content=="NO":
                    print("Answer is uncompleted! Answer again.\n")
                    continue
                else:
                    print("system error\n")
        elif i=="2. Please provide a concise description of the AI-based Predictive Analytics for Healthcare technology.":
            while True:
                user_input = input("You: ")
                message_text = [{"role": "system", "content": " get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content"},{"role": "user", "content": user_input}]
                generated_content = generate_completion(client, message_text)

                if generated_content== "YES":
                    print("Answer is completed! Answer the next question.\n")
                    break
                elif generated_content=="NO":
                    print("Answer is uncompleted! Answer again.")
                    continue
                else:
                    print("system error")
        elif i=="3.	Can you tell me more about the specific patents or prior art you may have encountered during your research? What similarities or differences did you find?":
            while True:
                user_input = input("You: ")
                message_text = [{"role": "system", "content": " get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content"},{"role": "user", "content": user_input}]
                generated_content = generate_completion(client, message_text)

                if generated_content== "YES":
                    print("Answer is completed! Answer the next question.\n")
                    break
                elif generated_content=="NO":
                    print("Answer is uncompleted! Answer again.\n")
                    continue
                else:
                    print("system error")

        

if __name__ == "__main__":
    main()
