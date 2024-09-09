import requests
from ..basecamp import Basecamp

class Campfire(Basecamp):
    
    def __init__(self, project_id: int, campfire_id: int):
        '''
        Interacts with Basecamp campfires.

        Parameters:
            project_id (int): The ID the Basecamp project containing the Campfire.
            campfire_id (int): ID of the Campfire you wish to target.
        '''
        self.__base_url = Basecamp._Basecamp__base_url
        self.__credentials = Basecamp._Basecamp__credentials
        self.project_id = project_id
        self.campfire_id = campfire_id
        self.__headers = {
            'Authorization': 'Bearer '+ self.__credentials['access_token'],
            "Content-Type": "application/json"
        } 
        
        get_campfire_url = f"{self.__base_url}/buckets/{self.project_id}/chats/{self.campfire_id}.json"
        response = requests.get(get_campfire_url, headers=self.__headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            self.info = response.json()
    
    def get_lines(self) -> list:
        '''
        Returns:
            list: A list of all campfire messages.
        '''
        get_lines_url = f"{self.__base_url}/buckets/{self.project_id}/chats/{self.campfire_id}/lines.json"
        response = requests.get(get_lines_url, headers=self.__headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()
    
    def write(self, content: str):
        '''
        Sends a message to campfire.

        Parameters:
            content (str): Message to be sent to campfire. Unable to send rich text, files or images from API to campfire.
        '''
        write_url = f"{self.__base_url}/buckets/{self.project_id}/chats/{self.campfire_id}/lines.json"

        payload = {
            "content": content
        }

        response = requests.post(write_url, headers=self.__headers, json=payload)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            print("Sent to campfire successfully!")