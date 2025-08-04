import os
from mimetypes import MimeTypes

import filetype
import requests

class Attachments:
    def __init__(self, client):
        '''
        Handles file attachments for Basecamp.
        
        Parameters:
            client: The Basecamp client instance.
        '''
        self.client = client
        self.files = {}
    
    def upload_file(self, file_path: str, name: str, headers: dict = None) -> dict:
        '''
        Uploads a file to Basecamp's servers and saves the file sgid in Attachment().files.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/attachments.md#create-an-attachment

        Parameters:
            file_path (str): Path to file you wish to upload.
            name (str): Name to identify the file in the files dictionary.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The uploaded file data
        '''
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        filename = os.path.basename(file_path)
        attachments_url = f"{self.client.base_url}/attachments.json"
        
        # Add filename to query parameters
        params = {"name": filename}
        
        file_size = os.path.getsize(file_path)
        mime = MimeTypes().guess_type(file_path)[0]
        
        # Create default headers for file upload
        request_headers = {
            'Authorization': f"Bearer {self.client.credentials['access_token']}",
            "Content-Type": mime,
            "Content-Length": str(file_size)
        }
        
        # Use custom headers if provided
        if headers:
            request_headers.update(headers)

        with open(file_path, "rb") as file:
            response = requests.post(
                attachments_url, 
                params=params, 
                headers=request_headers, 
                data=file
            )
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            sgid = response_data['attachable_sgid']
            
            # Extract the web URL from the response and print it
            if 'url' in response_data:
                print(f"File uploaded successfully! View it at: {response_data['url']}")
            else:
                print("File uploaded successfully!")
        
        self.files[name] = {
            "filename": filename,
            "file_size": str(file_size),
            "content-type": mime,
            "sgid": sgid,
            "id": response_data.get('id'),
            "url": response_data.get('url'),
            "created_at": response_data.get('created_at')
        }
        
        return response_data
    
    def upload_from_bytes(self, file_bytes: bytes, name: str, mime_type: str = None, headers: dict = None) -> dict:
        '''
        Uploads a file from bytes to Basecamp's servers and saves the file sgid in Attachment().files.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/attachments.md#create-an-attachment

        Parameters:
            file_bytes (bytes): Bytes content of the file to upload.
            name (str): Name to identify the file in the files dictionary.
            mime_type (str, optional): MIME type of the file. If not provided, will be guessed.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The uploaded file data
        '''
        attachments_url = f"{self.client.base_url}/attachments.json"
        
        # Add filename to query parameters
        params = {"name": name}
        
        file_size = len(file_bytes)
        
        # Try to guess the MIME type, or use the provided one, or default to text/plain
        if mime_type:
            mime = mime_type
        else:
            guess = filetype.guess(file_bytes)
            mime = guess.mime if guess else 'text/plain'
        
        # Create default headers for file upload
        request_headers = {
            'Authorization': f"Bearer {self.client.credentials['access_token']}",
            "Content-Type": mime,
            "Content-Length": str(file_size)
        }
        
        # Use custom headers if provided
        if headers:
            request_headers.update(headers)

        response = requests.post(
            attachments_url, 
            params=params, 
            headers=request_headers, 
            data=file_bytes
        )
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            sgid = response_data['attachable_sgid']
            
            # Extract the web URL from the response and print it
            if 'url' in response_data:
                print(f"File uploaded successfully! View it at: {response_data['url']}")
            else:
                print("File uploaded successfully!")
        
        self.files[name] = {
            "filename": name,
            "file_size": str(file_size),
            "content-type": mime,
            "sgid": sgid,
            "id": response_data.get('id'),
            "url": response_data.get('url'),
            "created_at": response_data.get('created_at')
        }
        
        return response_data
    
    def get_file(self, name: str) -> dict:
        '''
        Retrieves file information from the files dictionary.

        Parameters:
            name (str): Name of the file in the files dictionary.
            
        Returns:
            dict: File information or None if not found
        '''
        return self.files.get(name)
    
    def remove_file(self, name: str) -> bool:
        '''
        Removes a file from the files dictionary (does not delete from Basecamp).

        Parameters:
            name (str): Name of the file in the files dictionary.
            
        Returns:
            bool: True if file was removed, False if not found
        '''
        if name in self.files:
            del self.files[name]
            return True
        return False
    
    def list_files(self) -> list:
        '''
        Returns a list of all file names in the files dictionary.
        
        Returns:
            list: List of file names
        '''
        return list(self.files.keys())
    
    def clear_files(self):
        '''
        Clears the files dictionary without deleting the actual attachments.
        '''
        self.files = {}
    
    def create_attachment_html(self, name: str, caption: str = None) -> str:
        '''
        Creates HTML for embedding an attachment in rich text content.

        Parameters:
            name (str): Name of the file in the files dictionary.
            caption (str, optional): Caption to display with the attachment.
            
        Returns:
            str: HTML string for the attachment
        '''
        if name not in self.files:
            raise Exception(f"File '{name}' not found in attachments.")
        
        sgid = self.files[name]['sgid']
        caption_attr = f' caption="{caption}"' if caption else ''
        
        return f'<bc-attachment sgid="{sgid}"{caption_attr}></bc-attachment>'