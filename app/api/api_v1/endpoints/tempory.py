from fastapi import APIRouter, HTTPException
from app.services.check_user_answers import check_user_answers
from psycopg2.extras import execute_values
import json
from app.core.azure_client import client

import pdfkit
import markdown
import os
import random
from bs4 import BeautifulSoup
from docx import Document
import matplotlib.pyplot as plt
import re




number_set = set()

config=pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
pdf_options = {
    'page-size': 'A4',
    'encoding': 'UTF-8',
}
system_prompt= """
Answer the following questions to the best of your ability. If you do not know the answer, Answer should be more than 1000 words. please type 'I do not know
Please generate a detailed document using the following structure and formatting requirements:

1. **Title**: The main title of the document should be formatted as a level 1 heading and use the font "Courier New, monospace".

2. **Subtopics**: Each main section should be formatted as a level 2 heading and use the font "Comic Sans MS, cursive". Sub-sections under each main section should be formatted as level 3 headings and use the font "Georgia, serif".

3. **Bold Text**: Emphasize important keywords or phrases by making them bold.

4. **Italic Text**: Use italics for additional emphasis, quotes, or specific terms that need to stand out.

5. **Fonts**: Use different fonts for different elements:
   - Main title: "Courier New, monospace"
   - Subtopics: "Comic Sans MS, cursive"
   - Sub-subtopics: "Georgia, serif"

Here is an example structure to follow:

# Main Title

<style>
h1 { font-family: 'Courier New', monospace; }
h2 { font-family: 'Comic Sans MS', cursive; }
h3 { font-family: 'Georgia', serif; }
</style>

## Subtopic 1

This is an introductory paragraph for Subtopic 1. It contains an **important keyword** and some *italicized text*.

### Sub-subtopic 1.1

This section goes into more detail under Subtopic 1. It also includes some **bold** and *italic** text for emphasis.

## Subtopic 2

This is an introductory paragraph for Subtopic 2. Similar to the previous sections, it can have **bold** keywords and *italicized** phrases.

### Sub-subtopic 2.1

Additional details for Subtopic 2. Use **bold** text for highlighting and *italic** text for emphasis.

"""

system_prompt_for_graph="""When a user asks to create a graph, provide the data strictly in the format 'x values and y values' without additional information. For example:

For the last five years of Apple product sales draw a bar chart: '2018: 868586, 2019: 6576845, 2020: 457843758, 2021: 8687475786, 2022: 876854'.
For electric vehicle sales over the last 5 years draw a graph: '2017: 198350, 2018: 361307, 2019: 531407, 2020: 752684, 2021: 1051749'.
For the population growth in major cities over the last decade draw a column chart: '2013: 1200000, 2014: 1350000, 2015: 1500000, 2016: 1650000, 2017: 1800000'.
For the quarterly revenue of a company in the current fiscal year: 'Q1: 5000000, Q2: 5500000, Q3: 6000000, Q4: 6500000'.
Please ensure that only these specific formats are provided without any additional explanations or details.dont generate any other words. only data set"""
def generate_unique_number():
    while True:
        random_integer = random.randint(10000000, 20000000)
        if random_integer not in number_set:
            number_set.add(random_integer)
            return random_integer

def create_pdf(content,save_path):
    markdown_content = markdown.markdown(content)
    html_content = f"<html><body>{markdown_content}</body></html>"
       
    with open('temp.html', 'w', encoding='utf-8') as f:
        f.write(html_content)    

    pdfkit.from_file('temp.html', save_path, configuration=config,options=pdf_options)
    os.remove('temp.html')


def create_doc(content, save_path):
    doc = Document()
    markdown_content = markdown.markdown(content)
    html_content = f"<html><body>{markdown_content}</body></html>"

    soup = BeautifulSoup(html_content, 'html.parser')

    def add_elements_from_html(element):
        if element.name == 'h1':
            doc.add_heading(element.get_text(), level=1)
        elif element.name == 'h2':
            doc.add_heading(element.get_text(), level=2)
        elif element.name == 'h3':
            doc.add_heading(element.get_text(), level=3)
        elif element.name == 'p':
            doc.add_paragraph(element.get_text())
        elif element.name == 'ul':
            for li in element.find_all('li'):
                doc.add_paragraph(li.get_text(), style='List Bullet')
        elif element.name == 'ol':
            for li in element.find_all('li'):
                doc.add_paragraph(li.get_text(), style='List Number')
        elif element.name == 'b':
            p = doc.add_paragraph()
            run = p.add_run(element.get_text())
            run.bold = True
        elif element.name == 'i':
            p = doc.add_paragraph()
            run = p.add_run(element.get_text())
            run.italic = True
        elif element.name == 'u':
            p = doc.add_paragraph()
            run = p.add_run(element.get_text())
            run.underline = True

    for tag in soup.body:
        if isinstance(tag, str):  
            continue
        add_elements_from_html(tag)
    doc.save(save_path)

def convert_to_dic(content):
    split_data = content.split(',')
    data_dic = {}
    for word in split_data:
        try:
            X, Y = word.split(':')
            X = X.strip()
            Y = Y.strip()

            if 'million' in Y:
                Y = int(re.sub(r'[^0-9]', '', Y)) * 1_000_000
            elif 'billion' in Y:
                Y = int(re.sub(r'[^0-9]', '', Y)) * 1_000_000_000
            else:
                Y = int(re.sub(r'[^0-9]', '', Y))

            data_dic[int(X)] = Y

        except ValueError as e:
            print(f"Error parsing '{word}': {e}")
            raise ValueError(f"Error parsing '{word}': {e}")
    return data_dic

def generate_image(data_dic):
    plt.figure(figsize=(8, 5))  
    plt.bar(data_dic.keys(), data_dic.values(), color='skyblue')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Chart')
    plt.grid(True)
    plt.xticks(list(data_dic.keys())) 
    plt.tight_layout()

    #Save the plot as PNG image
    plt.savefig('bar_chart.png', dpi=300) 
    plt.close()


router = APIRouter()


@router.get("/tempory/")
async def tempory():
    
    user_prompt = "draw a bar chart for android users amount for last 5 years "
    message_text = [
        {"role": "system", "content": system_prompt_for_graph},
        {"role": "user", "content": user_prompt},
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

        content = f"{completion.choices[0].message.content}"
        
        unique_integer =generate_unique_number()
        
        save_folder = r'E:\intern\Synacal\New folder\Perceive-Chatbot\app\api\api_v1\endpoints\save_files'
        os.makedirs(save_folder, exist_ok=True)
        save_pdf_path = os.path.join(save_folder, f'file{unique_integer}.pdf')
        save_doc_path = os.path.join(save_folder, f'file{unique_integer}.docx')
       
        # create_pdf(content,save_pdf_path)
        # create_doc(content,save_doc_path)
        try:
            data_dic = convert_to_dic(content)
            generate_image(data_dic)
            print("Image generated successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        


        
        return {"response": content}
    except Exception as e:
        return {"error": str(e)}
