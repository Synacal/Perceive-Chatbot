
import os
from openai import AzureOpenAI
import streamlit as st
import uuid

st.title("AI-based Predictive Analytics for Healthcare Questionnaire")


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
    
    system_prompt =["you should check User Prompt that completed or not. User Prompt should include these points.\" The organization behind AI-based predictive analytics for healthcare is MediPredict Solutions. At MediPredict Solutions, we are dedicated to transforming healthcare through the power of artificial intelligence. Our flagship AI-based predictive The analytics platform is designed to revolutionize patient care by providing early warnings, personalized treatment insights and a deeper understanding of disease progression. Our mission is to provide healthcare with cutting-edge tools to more accurately predict health outcomes and improve the overall quality of care. Empowering Service Professionals.\" It is complete only if all the information included above is entered in the user prompt. it is compulsory Otherwise it is incomplete. Check the completed or incomplete user query. Return only \"NO\" word if not completed and \"YES\" word if completed. if you cant understand the user prompt, so return only \"NO\" word. ",
                    "get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content",
                    "get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content",
                    "get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content",
                    "get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content",
                    "get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content",
                    "get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content"
                    "get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content",
                    "get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content",
                    "get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content",
                    "get the user prompt and check what it has What are the various uses of Python? and it should include mentions of its applications in web development (server-side), software development, mathematics, and system scripting. please check the user prompt that is completed or uncompleted. firstly tell that completed or uncompleted. if uncompleted give full correct content"]


    for idx, question in enumerate(questions):
        st.subheader(question)

        while True:
            unique_id = uuid.uuid4()  # Generate a unique UUID
            user_input = st.text_input(f"Your Answer for Question {idx + 1}:", key=f"answer_{idx}_{unique_id}")
            message_text = [{"role": "system", "content": system_prompt[idx]},{"role": "user", "content": user_input}]
            
            if st.button(f"Submit for Question {idx + 1}"):
                generated_content = generate_completion(client, message_text)

            if generated_content== "YES":
                st.success("Answer is completed! Answer the next question.\n")
                break
            elif generated_content=="NO":
                st.warning("Answer is uncompleted! Answer again.\n")
                continue
            else:
                st.error("system error\n")
                    #return
        

if __name__ == "__main__":
    main()
