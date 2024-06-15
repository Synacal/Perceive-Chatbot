from app.core.database import get_percieve_db_connection
import time

# from app.core.pinecone import get_pinecone_client
from app.core.azure_client import client


def vectorize_description(description: str):
    model = "embedding-model"
    # client = get_pinecone_client()
    vector = (
        client.embeddings.create(input=[description], model=model).data[0].embedding
    )
    return vector


def vectorize_description_with_retries(
    description: str, retries=5, backoff_in_seconds=100
):
    for i in range(retries):
        try:
            return vectorize_description(description)
        except Exception as e:
            if "429" in str(e):
                print(
                    f"Rate limit exceeded. Retrying in {backoff_in_seconds} seconds..."
                )
                time.sleep(backoff_in_seconds)
                # backoff_in_seconds *= 2  # Exponential backoff
            else:
                raise
    raise Exception(f"Failed to vectorize description after {retries} retries.")


"""
def query_pinecone_index(description_vector, top_k=5):
    index = get_pinecone_client()
    response = index.query(vector=description_vector, top_k=top_k, include_metadata=True)
    return response"""


def generate_analysis(description: str, patent_data: dict):
    system_prompt = f"""Analyze the provided patent information against the user's invention description to identify and 
                    describe both similarities and differences, focusing on technical features, innovative aspects, 
                    and potential patentability issues.
                    Inputs:

                    User's Invention Description: {description}

                    Patent Information to Analyze: {patent_data}

                Analysis Tasks:

                    Task 1: Identify Similarities:
                        Prompt: "Given the abstract and claims of Patent X (details provided above) alongside the 
                        description of the user's invention, identify and describe the key similarities. Focus on 
                        technical features, shared functionalities, and overlapping application domains. Explain 
                        how these similarities could impact the patentability of the user’s invention."
                    Task 2: Identify Differences:
                        Prompt: "Based on the provided patent information (Patent X) and the user's invention 
                        description, identify and articulate the significant differences, particularly regarding 
                        novel features and inventive steps. Describe how these differences enhance the uniqueness 
                        of the user's invention and contribute to its patentability. Outline any new functionalities, 
                        technical solutions, or applications that differentiate the user's invention from the patent."

                Output:

                    Format for Response:
                        Similarities:
                            A detailed list and explanation of elements or concepts that are similar between the analyzed patent and the user's invention. Include any shared technological approaches or functionalities.
                        Differences:
                            A comprehensive outline of how the user's invention diverges from the analyzed patent. Highlight novel features, different technical solutions, or unique applications that are not covered by the patent.
                        Conclude with a brief summary of the potential implications of these similarities and differences on the user’s ability to patent the invention.
        """
    message_text = [{"role": "system", "content": system_prompt}]
    completion = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
    )
    return completion.choices[0].message.content
