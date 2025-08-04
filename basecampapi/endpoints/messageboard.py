import requests

class MessageBoard:

    def __init__(self, client, project_id: int, message_board_id: int):
        '''
        Interacts with Message Boards, Messages and Message comments.

        Parameters:
            client: The Basecamp client instance.
            project_id (int): The ID the Basecamp project containing the Message Board.
            message_board_id (int): ID of the Message Board you wish to target.
        '''

        self.client = client
        self.project_id = project_id
        self.message_board_id = message_board_id

        get_all_messages_url = f"{client.base_url}/buckets/{self.project_id}/message_boards/{self.message_board_id}/messages.json"
        response = requests.get(get_all_messages_url, headers=client.get_headers())
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            self.__messages = response.json()

    def get_all_messages(self, headers=None) -> list:
        '''
        Returns a list of all messages posted on the Message Board.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/messages.md#get-messages
            
        Parameters:
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            list: A list of all messages posted on the Message Board
        '''
        return self.__messages

    def get_message(self, message_id: int, headers=None) -> dict:
        '''
        Returns all information about a message, together with its content.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/messages.md#get-a-message

        Parameters:
            message_id (int): The ID of the message that you wish to read.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The message data
        '''
        get_message_url = f"{self.client.base_url}/buckets/{self.project_id}/messages/{message_id}.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
            
        response = requests.get(get_message_url, headers=request_headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()

    def create_message(self, data: dict, headers=None) -> dict:
        '''
        Creates a new Message Board post (a new message). Messages can contain files and rich text.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/messages.md#create-a-message

        Parameters:
            data (dict): Complete payload to send to the API.
                         Example: {"subject": "Meeting notes", "content": "<p>Notes here</p>", "status": "active"}
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The created message data
        '''
        import json

        create_message_url = f"{self.client.base_url}/buckets/{self.project_id}/message_boards/{self.message_board_id}/messages.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        payload = json.dumps(data)
        response = requests.post(create_message_url, headers=request_headers, data=payload)

        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            # Extract the web URL from the response and print it
            if 'app_url' in response_data:
                print(f"Message created successfully! View it at: {response_data['app_url']}")
            else:
                print("Message created successfully!")
            return response_data

    def update_message(self, message_id: int, data: dict, headers=None) -> dict:
        '''
        Replaces the content and/or subject of an already existing message.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/messages.md#update-a-message

        Parameters:
            message_id (int): The ID of the message to update.
            data (dict): Complete payload to send to the API.
                         Example: {"subject": "Updated title", "content": "<p>Updated content</p>"}
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The updated message data
        '''
        import json

        update_message_url = f"{self.client.base_url}/buckets/{self.project_id}/messages/{message_id}.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        payload = json.dumps(data)
        response = requests.put(update_message_url, headers=request_headers, data=payload)

        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            # Extract the web URL from the response and print it
            if 'app_url' in response_data:
                print(f"Message updated successfully! View it at: {response_data['app_url']}")
            else:
                print("Message updated successfully!")
            return response_data
