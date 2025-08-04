import requests

class Basecamp:
    
    def __init__(self, credentials: dict, verification_code='Not available!'):
        '''
        Initializes a Basecamp session.

        Parameters:
            credentials (dict): A dictionary containing account_id, client_id, client_secret, redirect_uri and refresh_token.
            verification_code (str, optional): Verification code for OAuth flow if refresh_token is not available.
        ''' 
        
        self.credentials = credentials
        self.base_url = f"https://3.basecampapi.com/{credentials['account_id']}"
        
        if 'refresh_token' not in credentials:
            if verification_code == 'Not available!':
                self.verification_link = f"https://launchpad.37signals.com/authorization/new?type=web_server&client_id={self.credentials['client_id']}&redirect_uri={self.credentials['redirect_uri']}"
                raise Exception("Access denied. Please use the following url to allow access and get the code from the redirect page's url parameter \"code\", then pass it as verification_code parameter of the Basecamp object: " + self.verification_link)
            else:
                self.verification_code = verification_code
                verification_url = f"https://launchpad.37signals.com/authorization/token?type=web_server&client_id={self.credentials['client_id']}&redirect_uri={self.credentials['redirect_uri']}&client_secret={self.credentials['client_secret']}&code={self.verification_code}"
                response = requests.post(verification_url)

                if not response.ok:
                    raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
                else:
                    self.credentials['refresh_token'] = response.json()["refresh_token"]
                    self._get_access()
                    print('refresh_token and access_token added to credentials. ')
                    print('Please save your refresh_token for future access: ' + self.credentials['refresh_token'])
        else:
            self._get_access()

    
    def _get_access(self):
        """Get access token using refresh token"""
        access_url = f"https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token={self.credentials['refresh_token']}&client_id={self.credentials['client_id']}&redirect_uri={self.credentials['redirect_uri']}&client_secret={self.credentials['client_secret']}"
        response = requests.post(access_url)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            self.credentials['access_token'] = response.json()['access_token']
            print('Authentication successful!')
    
    def get_headers(self, custom_headers=None):
        """Return headers with authentication for API requests
        
        Parameters:
            custom_headers (dict, optional): Custom headers to merge with default headers
        """
        headers = {
            'Authorization': f"Bearer {self.credentials['access_token']}",
            'Content-Type': 'application/json'
        }
        
        if custom_headers:
            headers.update(custom_headers)
            
        return headers
    
    def message_board(self, project_id: int, message_board_id: int):
        """Create and return a MessageBoard resource
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/message_boards.md
        
        Parameters:
            project_id (int): The ID the Basecamp project containing the Message Board.
            message_board_id (int): ID of the Message Board you wish to target.
        """
        from .endpoints.messageboard import MessageBoard
        return MessageBoard(self, project_id, message_board_id)
    
    def campfire(self, project_id: int, campfire_id: int):
        """Create and return a Campfire resource
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/campfires.md
        
        Parameters:
            project_id (int): The ID the Basecamp project containing the Campfire.
            campfire_id (int): ID of the Campfire you wish to target.
        """
        from .endpoints.campfire import Campfire
        return Campfire(self, project_id, campfire_id)
    
    def attachments(self):
        """Create and return an Attachments resource
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/attachments.md
        """
        from .endpoints.attachments import Attachments
        return Attachments(self)
        
    def todoset(self, project_id: int, todoset_id: int):
        """Create and return a TodoSet resource
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#get-to-do-lists
        
        Parameters:
            project_id (int): The ID of the Basecamp project containing the To-do set.
            todoset_id (int): ID of the To-do set you wish to target.
        """
        from .endpoints.todoset import TodoSet
        return TodoSet(self, project_id, todoset_id)
    
    def todolist(self, project_id: int, todolist_id: int):
        """Create and return a TodoList resource
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#get-a-to-do-list
        
        Parameters:
            project_id (int): The ID of the Basecamp project containing the To-do list.
            todolist_id (int): ID of the To-do list you wish to target.
        """
        from .endpoints.todolist import TodoList
        return TodoList(self, project_id, todolist_id)
    
    def comments(self, project_id: int):
        """Create and return a Comments resource
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md
        
        Parameters:
            project_id (int): The ID of the Basecamp project containing the comments.
        """
        from .endpoints.comments import Comments
        return Comments(self, project_id)
    
    def chatbot(self, chatbot_key: str):
        """Create and return a Chatbot resource
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md
        
        Parameters:
            chatbot_key (str): The key part of the lines_url from the chatbot.
                              Example: If lines_url is "https://3.basecampapi.com/195539477/integrations/yFU7K9oKrcZyvYLDw4GfLU89/buckets/2085958496/chats/9007199254741045/lines",
                                       then chatbot_key is "yFU7K9oKrcZyvYLDw4GfLU89"
        """
        from .endpoints.chatbot import Chatbot
        return Chatbot(self, chatbot_key)
        
    def request(self, method: str, path: str, data: dict = None, params: dict = None, headers: dict = None):
        """
        Make a request to any Basecamp API endpoint.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api
        
        Parameters:
            method (str): HTTP method ('GET', 'POST', 'PUT', 'DELETE')
            path (str): API endpoint path (without the base URL)
            data (dict, optional): Request body for POST/PUT requests
            params (dict, optional): Query parameters for the request
            headers (dict, optional): Custom headers to use for this request
            
        Returns:
            dict or list: The response data from the API
            
        Example:
            # Get all to-dos in a to-do list
            todos = client.request(
                method='GET',
                path=f'/buckets/{project_id}/todolists/{todolist_id}/todos.json'
            )
            
            # Create a new to-do
            new_todo = client.request(
                method='POST',
                path=f'/buckets/{project_id}/todolists/{todolist_id}/todos.json',
                data={
                    "content": "Finish the report",
                    "description": "Complete the quarterly report by Friday",
                    "assignee_ids": [1234567],
                    "due_on": "2023-12-31"
                }
            )
        """
        # Ensure path starts with a slash
        if not path.startswith('/'):
            path = '/' + path
        
        # Build the full URL
        url = f"{self.base_url}{path}"
        
        # Get headers with authentication
        request_headers = self.get_headers()
        if headers:
            request_headers.update(headers)
        
        # Make the request based on the method
        method = method.upper()
        
        if method == 'GET':
            response = requests.get(url, params=params, headers=request_headers)
        elif method == 'POST':
            response = requests.post(url, params=params, json=data, headers=request_headers)
        elif method == 'PUT':
            response = requests.put(url, params=params, json=data, headers=request_headers)
        elif method == 'DELETE':
            response = requests.delete(url, params=params, headers=request_headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # Handle the response
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        
        # Return the response data if it's JSON, otherwise return the response object
        if response.headers.get('Content-Type', '').startswith('application/json'):
            return response.json()
        else:
            return response