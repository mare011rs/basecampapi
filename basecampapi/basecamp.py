import requests
import os
import datetime
import json
from mimetypes import MimeTypes

class Basecamp:
    
    def __init__(self, account_id, credentials):
        self.account_id = account_id
        self.credentials = credentials
        self.client_id = credentials["client_id"]
        self.client_secret = credentials["client_secret"]
        self.redirect_uri = credentials["redirect_uri"]
        self.refresh_token = credentials["refresh_token"]
        self.basecamp_account_id = account_id
        self.access_url = f"https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token={self.refresh_token}&client_id={self.client_id}&redirect_uri={self.redirect_uri}&client_secret={self.client_secret}"
        self.access_token = requests.post(self.access_url).json()['access_token']
        self.base_url = f"https://3.basecampapi.com/{self.basecamp_account_id}"
        self.files = []
        
    def upload_file(self, path):
        attachments_url = f"{self.base_url}/attachments.json?name={path}"
        file_size = os.path.getsize(path)
        mime = MimeTypes().guess_type(path)[0]
        headers = {
            'Authorization': 'Bearer '+ self.access_token,
            "Content-Type": mime,
            "Content-Length": str(file_size)
            }

        with open(path, "rb") as content:
            sgid = requests.post(attachments_url, headers=headers, data=content).json()['attachable_sgid']
        file = {
            "filename": os.path.basename(path),
            "file_size": str(file_size),
            "content-type": mime,
            "sgid": sgid
        }
        self.files.append(file)

class Campfire:
        
    def __init__(self, project_id, campfire_id, session):
        self.project_id = project_id
        self.campfire_id = campfire_id
        self.files = session.files
        self.access_token = session.access_token
        self.base_url = session.base_url
        self.headers = {
            'Authorization': 'Bearer '+ self.access_token,
            "Content-Type": "application/json"
        }        

    def info(self):
        get_campfire_url = f"{self.base_url}/buckets/{self.project_id}/chats/{self.campfire_id}.json"
        return requests.get(get_campfire_url, headers=self.headers).json()
    
    def get_lines(self):
        get_lines_url = f"{self.base_url}/buckets/{self.project_id}/chats/{self.campfire_id}/lines.json"
        return requests.get(get_lines_url, headers=self.headers).json()
    
    def write(self, content):
        write_url = f"{self.base_url}/buckets/{self.project_id}/chats/{self.campfire_id}/lines.json"
        requests.post(write_url, headers=self.headers, data='{"content": "'+content+'"}')
        print("Sent to campfire successfully!")
        

class MessageBoard:
    
    def __init__(self, project_id, message_board_id, session):
        self.project_id = project_id
        self.message_board_id = message_board_id
        self.files = session.files
        self.access_token = session.access_token
        self.base_url = session.base_url
        self.headers = {
            'Authorization': 'Bearer '+ self.access_token,
            "Content-Type": "application/json"
        }
    
    def get_all_messages(self):
        get_all_messages_url = f"{self.base_url}/buckets/{self.project_id}/message_boards/{self.message_board_id}/messages.json"
        return requests.get(get_all_messages_url, headers=self.headers).json()
    
    def get_message(self, message_id):
        self.message_id = message_id
        get_message_url = f"{self.base_url}/buckets/{self.project_id}/messages/{self.message_id}.json"
        return requests.get(get_message_url, headers=self.headers).json()
    
    def create_message(self, subject, content):
        self.subject = subject
        self.content = content
        create_message_url = f"{self.base_url}/buckets/{self.project_id}/message_boards/{self.message_board_id}/messages.json"
        requests.post(create_message_url, headers=self.headers, data=str('{"subject": "'+self.subject+'", "content": "'+self.content+'", "status": "active"}').encode())
        print("Message created successfully!")
    
    def update_message(self, message_id, subject, content):
        update_message_url = f"{self.base_url}/buckets/{self.project_id}/messages/{message_id}.json"
        requests.put(update_message_url, headers=self.headers, data=str('{"subject": "'+subject+'", "content": "'+content+'"}').encode())
        print("Message updated successfully!")
        
    def get_all_comments(self, message_id):
        get_all_comments_url = f"{self.base_url}/buckets/{self.project_id}/recordings/{message_id}/comments.json"
        return requests.get(get_all_comments_url, headers=self.headers).json()
    
    def get_comment(self, comment_id):
        self.comment_id = comment_id
        get_comment_url = f"{self.base_url}/buckets/{self.project_id}/comments/{self.comment_id}.json"
        return requests.get(get_comment_url, headers=self.headers).json()
    
    def create_comment(self, message_id, content):
        create_comment_url = f"{self.base_url}/buckets/{self.project_id}/recordings/{message_id}/comments.json"
        requests.post(create_comment_url, headers=self.headers, data='{"content": "'+content+'"}')
        print("Comment created successfully!")
    
    def update_comment(self, comment_id, content):
        update_comment_url = f"{self.base_url}/buckets/{self.project_id}/comments/{comment_id}.json"
        requests.put(update_comment_url, headers=self.headers, data='{"content": "'+content+'"}')
        print("Comment updated successfully!")