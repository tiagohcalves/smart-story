import json
import os
import re
from time import sleep

import PIL.Image
import google.generativeai as genai
from pypdf import PdfReader

API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    response = model.generate_content(f"Retorne um objeto JSON contendo as seguintes chaves: 'description' (descrição do conteúdo da imagem), 'date' (data mais provável da imagem ter sido gerada, formato YYYY-MM-DD) sobre o seguinte texto: {text}")
    return response.text

def process_pdf_file(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    response = model.generate_content(f"Retorne um objeto JSON contendo as seguintes chaves: 'description' (descrição do conteúdo da imagem), 'date' (data mais provável da imagem ter sido gerada, formato YYYY-MM-DD) sobre o seguinte texto: {text}")
    return response.text

def process_image_file(file_path):
    img = PIL.Image.open(file_path)
    response = model.generate_content([
        "Retorne um objeto JSON contendo as seguintes chaves: 'description' (descrição do conteúdo da imagem), 'date' (data mais provável da imagem ter sido gerada), formato YYYY-MM-DD", img
    ])
    return response.text

def process_file(file_path):
    if file_path.endswith('.txt'):
        return process_text_file(file_path)
    elif file_path.endswith('.pdf'):
        return process_pdf_file(file_path)
    elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        return process_image_file(file_path)
    else:
        return None

def main():
    data_dir = './data'
    results = {}
    for root, _, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            result = process_file(file_path)
            if result:
                try:
                    result = re.sub(r'```json|```', '', result).strip()
                except Exception as e:
                    print(f"Failed to strip the json tag from {result}: {e}")

                print(result)
                results[file] = result
            else:
                print(f"Unsupported file type: {file_path}")
            # wait to not exceed gemini API rate limit
            sleep(1)

    with open("results.json", "w") as outfile:
        json.dump(results, outfile)


if __name__ == "__main__":
    main()