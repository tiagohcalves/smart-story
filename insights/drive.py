import base64
from io import BytesIO
import os
import logging

import PIL.Image
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive, GoogleDriveFile
from pypdf import PdfReader

from database.models.document import Document
from database.repositories.document_repository import DocumentRepository
from database.connections.sqlite import SQLiteConnection

# TODO get from settings
folder_id = '14pQp9K1V4g5t1uu9O_lIIrKKkcO0l2FsuozFR8bvsEy80VyxLdZ0cdf5NpwBXu_eZpJrH5Gb'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Authenticate and create the PyDrive client
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and automatically handles authentication.
drive = GoogleDrive(gauth)

db = DocumentRepository(SQLiteConnection())

# Function to download all files from a folder
def download_folder(folder_id):
    # List all files in the folder
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    downloaded_documents = set(db.get_all_document_ids())
    
    for file in file_list:
        file: GoogleDriveFile
        file_id = file['id']
        # Skip files that have already been downloaded
        if file_id in downloaded_documents:
            logging.info(f"Skipping {file['title']}")
            continue

        file_title = file['title']
        file_path = file_id+"-"+file_title
        
        # Check if the file is a folder
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            # Recursively download the folder
            download_folder(file_id)
        else:
            # Download the file
            logging.info(f'Downloading {file_title} to {file_path}')
            if 'image' in file['mimeType']:
                # Download image file content
                file.GetContentFile(file_path)
                buff = BytesIO()
                img = PIL.Image.open(file_path)
                img.save(buff, format='PNG')
                img_str = base64.b64encode(buff.getvalue()).decode('ascii')

                db.create(Document(file_id, img_str, None, file['createdDate'], "img"))
                os.remove(file_path)  # Remove the file after storing in the database
            elif 'pdf' in file['mimeType']:
                # Download PDF file content
                file.GetContentFile(file_path)
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                db.create(Document(file_id, text, None, file['createdDate'], "pdf"))
                os.remove(file_path)  # Remove the file after storing in the database
            else:
                # Download other file types as string content
                file_content = file.GetContentString()
                db.create(Document(file_id, file_content, None, file['createdDate'], "txt"))

# Replace 'your_folder_id' with the actual folder ID
download_folder(folder_id)