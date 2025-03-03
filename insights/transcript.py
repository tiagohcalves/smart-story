import base64
from io import BytesIO
import json
import os
import re
import logging

import PIL.Image

from llm.model import LLM
from database.models.document import Document
from database.connections.sqlite import SQLiteConnection
from database.repositories.document_repository import DocumentRepository

logging.basicConfig(level=logging.INFO)

model = LLM()
db = DocumentRepository(SQLiteConnection())

def process_text_file(text: str):
    response = model.generate_content(f"Retorne um objeto JSON contendo as seguintes chaves: 'description' (resumo do conteudo), 'date' (data mais provável da imagem ter sido gerada, formato YYYY-MM-DD) sobre o seguinte texto: {text}")
    return response.text

def process_pdf_file(text: str):
    response = model.generate_content(f"Retorne um objeto JSON contendo as seguintes chaves: 'description' (resumo do conteudo), 'date' (data mais provável da imagem ter sido gerada, formato YYYY-MM-DD) sobre o seguinte texto: {text}")
    return response.text

def process_image_file(img_text: str):
    # Decode the image
    img = BytesIO(base64.b64decode(img_text.encode('ascii')))
    img = PIL.Image.open(img)
    response = model.generate_content([
        "Retorne um objeto JSON contendo as seguintes chaves: 'description' (descrição do conteúdo da imagem), 'date' (data mais provável da imagem ter sido gerada), formato YYYY-MM-DD", img
    ])
    return response.text

def process_file(content, file_type):
    if file_type == 'txt':
        return process_text_file(content)
    elif file_type == 'pdf':
        return process_pdf_file(content)
    elif file_type == "img":
        return process_image_file(content)
    else:
        return None

def transcribe_file(content: str, filetype: str) -> str:
    result = process_file(content, filetype)
    if result:
        try:
            result = re.sub(r'```json|```', '', result).strip()
        except Exception as e:
            logging.error(f"Failed to strip the json tag from {result}: {e}")

        logging.info(result)
        return result
    
    logging.warning(f"Unsupported file type: {filetype}")
    return None

def main():
    files_to_process = db.get_documents_without_description()
    logging.info(f"Found {len(files_to_process)} files to process.")

    for document in files_to_process:
        logging.info(f"Processing file: {document.id}")
        description = transcribe_file(document.content, document.filetype)
        if description is not None:
            document.description = description
            db.update(document)

if __name__ == "__main__":
    main()