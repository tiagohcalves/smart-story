import os

import PIL.Image
import google.generativeai as genai
from pypdf import PdfReader
import base64


API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# reader = PdfReader("example.pdf")
# text = ""
# for page in reader.pages:
#     text += page.extract_text() + "\n"

# print(text)

# response = model.generate_content("Resuma de forma clara e sucinta o seguinte texto: " + text)

# print("---------------------------------------------------")

image_path = "data/1fA2jX7qH67Ma5te4aNrvBTP246Dpavxz-image - Ingrid Magalhães.jpg"
img = PIL.Image.open(image_path)
response = model.generate_content([
    "Descreva o conteudo desta imagem e a data do documento contido nela.", img
])

print(response.text.encode("utf-8"))