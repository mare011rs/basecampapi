import requests
import json

class Chatbot:
    def __init__(self, client, chatbot_key: str):
        '''
        Interacts with Basecamp chatbots.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md
        
        Parameters:
            client: The Basecamp client instance.
            chatbot_key (str): The key part of the lines_url from the chatbot.
                              Example: If lines_url is "https://3.basecampapi.com/195539477/integrations/yFU7K9oKrcZyvYLDw4GfLU89/buckets/2085958496/chats/9007199254741045/lines",
                                       then chatbot_key is "yFU7K9oKrcZyvYLDw4GfLU89"
        '''
        self.client = client
        self.chatbot_key = chatbot_key
    
    def write(self, project_id: int, campfire_id: int, data: dict, content_param: str = None, headers=None) -> bool:
        '''
        Posts a message as a chatbot.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#create-a-line
        
        Parameters:
            project_id (int): The ID of the Basecamp project containing the chat.
            campfire_id (int): ID of the chat (campfire) where the message will be posted.
            data (dict): Complete payload to send to the API.
                         Example: {"content": "Good morning"}
            content_param (str, optional): Modifies the name of the required content param to support webhooks from a third-party.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            bool: True if post was successful
        '''
        post_url = f"{self.client.base_url}/integrations/{self.chatbot_key}/buckets/{project_id}/chats/{campfire_id}/lines.json"
        
        # Add content_param as a query parameter if provided
        if content_param:
            post_url += f"?content_param={content_param}"
        
        # Use custom headers or default headers
        request_headers = {
            'Content-Type': 'application/json'
        }
        if headers:
            request_headers.update(headers)
        
        payload = json.dumps(data)
        response = requests.post(post_url, headers=request_headers, data=payload)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            print("Message posted successfully!")
            return True