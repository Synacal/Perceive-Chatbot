import os
import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize AzureOpenAI client
client = AzureOpenAI(
    azure_endpoint="https://chatbotmedipredict.openai.azure.com/",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview"
)

def main():
    st.title("Perceive - Chatbot")

    user_input = st.text_input("You:", "")

    if st.button("Send"):

        message_text = [{"role": "system", "content": "When answering queries, assess whether the question pertains to technology descriptions, patent strategies, or specific innovation applications. For technology descriptions, provide a concise overview highlighting unique features and technical aspects. If the query relates to patent strategies, discuss geographical focus, rationale for market selection, and steps for ensuring patent application effectiveness, including enablement and claim definiteness. When addressing applications, focus on industry relevance, novel contributions, and non-obviousness, leveraging specific examples from our research and development efforts. Ensure responses integrate our innovations' potential impact on the domain, distinguishing our solutions from existing technologies and outlining our approach to securing intellectual property rights globally."},{"role": "user", "content": user_input}]

   
        completion = client.chat.completions.create(
            model="gpt-35-turbo",  # model = "deployment_name"
            messages=message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        # Retrieve content from completion
        content = completion.choices[0].message.content

        # Display response
        st.text_area("Bot:", value=content, height=200, max_chars=None, key=None)

if __name__ == "__main__":
    main()
