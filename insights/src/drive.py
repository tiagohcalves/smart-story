from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Authenticate and create the PyDrive client
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and automatically handles authentication.
drive = GoogleDrive(gauth)

# Function to download all files from a folder
def download_folder(folder_id, destination):
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination):
        os.makedirs(destination)

    # List all files in the folder
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    
    for file in file_list:
        file_id = file['id']
        file_title = file['title']
        file_path = os.path.join(destination, file_id+"-"+file_title)
        
        # Check if the file is a folder
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            # Recursively download the folder
            download_folder(file_id, file_path)
        else:
            # Download the file
            print(f'Downloading {file_title} to {file_path}')
            file.GetContentFile(file_path)

# Replace 'your_folder_id' with the actual folder ID and 'destination_path' with the desired download path
folder_id = '14pQp9K1V4g5t1uu9O_lIIrKKkcO0l2FsuozFR8bvsEy80VyxLdZ0cdf5NpwBXu_eZpJrH5Gb'
destination_path = '../data/drive_raw_data/'

download_folder(folder_id, destination_path)