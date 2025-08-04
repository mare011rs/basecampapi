import requests
import json

class Comments:
    def __init__(self, client, project_id: int):
        '''
        Interacts with comments on any commentable Basecamp resource.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md
        
        Parameters:
            client: The Basecamp client instance.
            project_id (int): The ID of the Basecamp project containing the comments.
        '''
        self.client = client
        self.project_id = project_id
    
    def get_all_comments(self, recording_id: int, headers=None) -> list:
        '''
        Gets a list of all comments on a recording.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#get-comments
        
        Parameters:
            recording_id (int): The ID of the recording (message, to-do, etc.) to get comments for.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            list: A list of comments on the recording.
        '''
        get_comments_url = f"{self.client.base_url}/buckets/{self.project_id}/recordings/{recording_id}/comments.json"
        
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
            
        response = requests.get(get_comments_url, headers=request_headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()
    
    def get_comment(self, comment_id: int, headers=None) -> dict:
        '''
        Gets information and content of a specific comment.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#get-a-comment
        
        Parameters:
            comment_id (int): The ID of the comment to return the information for.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: Information about the comment.
        '''
        get_comment_url = f"{self.client.base_url}/buckets/{self.project_id}/comments/{comment_id}.json"
        
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
            
        response = requests.get(get_comment_url, headers=request_headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()
    
    def create_comment(self, recording_id: int, data: dict, headers=None) -> dict:
        '''
        Creates a new comment on a recording.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#create-a-comment
        
        Parameters:
            recording_id (int): The ID of the recording (message, to-do, etc.) to comment on.
            data (dict): Complete payload to send to the API.
                         Example: {"content": "<p>My comment</p>"}
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The created comment data
        '''
        create_comment_url = f"{self.client.base_url}/buckets/{self.project_id}/recordings/{recording_id}/comments.json"
        
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        payload = json.dumps(data)
        response = requests.post(create_comment_url, headers=request_headers, data=payload)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            # Extract the web URL from the response and print it
            if 'app_url' in response_data:
                print(f"Comment created successfully! View it at: {response_data['app_url']}")
            else:
                print("Comment created successfully!")
            return response_data
    
    def update_comment(self, comment_id: int, data: dict, headers=None) -> dict:
        '''
        Updates an existing comment.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#update-a-comment
        
        Parameters:
            comment_id (int): The ID of the comment to update.
            data (dict): Complete payload to send to the API.
                         Example: {"content": "<p>Updated comment</p>"}
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The updated comment data
        '''
        update_comment_url = f"{self.client.base_url}/buckets/{self.project_id}/comments/{comment_id}.json"
        
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        payload = json.dumps(data)
        response = requests.put(update_comment_url, headers=request_headers, data=payload)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            # Extract the web URL from the response and print it
            if 'app_url' in response_data:
                print(f"Comment updated successfully! View it at: {response_data['app_url']}")
            else:
                print("Comment updated successfully!")
            return response_data
    
    def trash_comment(self, comment_id: int, headers=None) -> bool:
        '''
        Moves a comment to the trash.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/recordings.md#trash-a-recording
        
        Parameters:
            comment_id (int): The ID of the comment to trash.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            bool: True if the comment was trashed successfully
        '''
        trash_url = f"{self.client.base_url}/buckets/{self.project_id}/recordings/{comment_id}/status/trashed.json"
        
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        response = requests.put(trash_url, headers=request_headers)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            print("Comment moved to trash successfully!")
            return True