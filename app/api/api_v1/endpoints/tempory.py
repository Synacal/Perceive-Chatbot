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



router = APIRouter()


@router.get("/tempory/")
async def tempory():
    
    user_prompt = "What are the different between class and objects. "
    message_text = [
        {"role": "system", "content": system_prompt},
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
       
        create_pdf(content,save_pdf_path)
        create_doc(content,save_doc_path)
        
        


        
        return {"response": content}
    except Exception as e:
        return {"error": str(e)}
