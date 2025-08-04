import requests

class Campfire:
    
    def __init__(self, client, project_id: int, campfire_id: int):
        '''
        Interacts with Basecamp campfires.

        Parameters:
            client: The Basecamp client instance.
            project_id (int): The ID the Basecamp project containing the Campfire.
            campfire_id (int): ID of the Campfire you wish to target.
        '''
        self.client = client
        self.project_id = project_id
        self.campfire_id = campfire_id
        
        get_campfire_url = f"{client.base_url}/buckets/{self.project_id}/chats/{self.campfire_id}.json"
        response = requests.get(get_campfire_url, headers=client.get_headers())
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            self.info = response.json()
    
    def get_lines(self, headers=None) -> list:
        '''
        Returns a list of all campfire messages.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/campfires.md#get-lines
            
        Parameters:
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            list: A list of all campfire messages.
        '''
        get_lines_url = f"{self.client.base_url}/buckets/{self.project_id}/chats/{self.campfire_id}/lines.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
            
        response = requests.get(get_lines_url, headers=request_headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()
    
    def write(self, data: dict, headers=None) -> dict:
        '''
        Sends a message to campfire.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/campfires.md#create-a-line

        Parameters:
            data (dict): Complete payload to send to the API.
                         Example: {"content": "Hello team!"}
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The created message data
        '''
        write_url = f"{self.client.base_url}/buckets/{self.project_id}/chats/{self.campfire_id}/lines.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        response = requests.post(write_url, headers=request_headers, json=data)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            # Extract the web URL from the response and print it
            if 'app_url' in response_data:
                print(f"Sent to campfire successfully! View it at: {response_data['app_url']}")
            else:
                print("Sent to campfire successfully!")
            return response_data