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

OUTPUT_FILE = '../data/results.json'
DATA_DIR = '../data/drive_raw_data'

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    response = model.generate_content(f"Retorne um objeto JSON contendo as seguintes chaves: 'description' (resumo do conteudo), 'date' (data mais provável da imagem ter sido gerada, formato YYYY-MM-DD) sobre o seguinte texto: {text}")
    return response.text, text, "txt"

def process_pdf_file(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    response = model.generate_content(f"Retorne um objeto JSON contendo as seguintes chaves: 'description' (resumo do conteudo), 'date' (data mais provável da imagem ter sido gerada, formato YYYY-MM-DD) sobre o seguinte texto: {text}")
    return response.text, text, "pdf"

def process_image_file(file_path):
    img = PIL.Image.open(file_path)
    response = model.generate_content([
        "Retorne um objeto JSON contendo as seguintes chaves: 'description' (descrição do conteúdo da imagem), 'date' (data mais provável da imagem ter sido gerada), formato YYYY-MM-DD", img
    ])
    return response.text, "", "img"

def process_file(file_path):
    if file_path.endswith('.txt'):
        return process_text_file(file_path)
    elif file_path.endswith('.pdf'):
        return process_pdf_file(file_path)
    elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        return process_image_file(file_path)
    else:
        return None
        
def load_results():
    # reads the existing results from the output file
    # and saves the files that have already been processed
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as infile:
            return json.load(infile)
    return {}


def main():
    results = load_results()
    processed_files = results.keys()
    for i, (root, _, files) in enumerate(os.walk(DATA_DIR)):
        for file in files:
            if file in processed_files:
                continue
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            result, raw, ftype = process_file(file_path)
            if result:
                try:
                    result = json.loads(re.sub(r'```json|```', '', result).strip())
                    result['raw'] = raw
                    result['type'] = ftype
                    result = json.dumps(result)
                except Exception as e:
                    print(f"Failed to strip the json tag from {result}: {e}")

                print(result)
                results[file] = result
            else:
                print(f"Unsupported file type: {file_path}")
            # wait to not exceed gemini API rate limit
            sleep(2)
        
        if i+1 % 10 == 0:
            with open(OUTPUT_FILE, "w") as outfile:
                json.dump(results, outfile)

    # TODO add checkpoint
    with open(OUTPUT_FILE, "w") as outfile:
        json.dump(results, outfile)


if __name__ == "__main__":
    main()