import requests

class TodoSet:
    def __init__(self, client, project_id: int, todoset_id: int):
        '''
        Interacts with a To-do set, which contains To-do lists and To-do list groups.
        
        Parameters:
            client: The Basecamp client instance.
            project_id (int): The ID of the Basecamp project containing the To-do set.
            todoset_id (int): ID of the To-do set you wish to target.
        '''
        self.client = client
        self.project_id = project_id
        self.todoset_id = todoset_id
        
        get_todoset_url = f"{client.base_url}/buckets/{self.project_id}/todosets/{self.todoset_id}.json"
        response = requests.get(get_todoset_url, headers=client.get_headers())
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            self.info = response.json()
    
    def get_todolists(self, status=None, headers=None) -> list:
        '''
        Returns a list of to-do lists in the to-do set.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#get-to-do-lists
        
        Parameters:
            status (str, optional): Filter by status ('archived' or 'trashed'). If not provided, returns active to-do lists.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            list: A list of to-do lists in the to-do set
        '''
        get_todolists_url = f"{self.client.base_url}/buckets/{self.project_id}/todosets/{self.todoset_id}/todolists.json"
        
        # Add status parameter if provided
        params = {}
        if status:
            params['status'] = status
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
            
        response = requests.get(get_todolists_url, params=params, headers=request_headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()
    
    def get_todolist_groups(self, headers=None) -> list:
        '''
        Returns a list of to-do list groups in the to-do set.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md#list-to-do-list-groups
        
        Parameters:
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            list: A list of to-do list groups in the to-do set
        '''
        get_groups_url = f"{self.client.base_url}/buckets/{self.project_id}/todosets/{self.todoset_id}/groups.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
            
        response = requests.get(get_groups_url, headers=request_headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()
    
    def get_todolist_group(self, group_id: int, headers=None) -> dict:
        '''
        Returns information about a specific to-do list group.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md#get-to-do-list-group
        
        Parameters:
            group_id (int): The ID of the to-do list group.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: Information about the to-do list group
        '''
        get_group_url = f"{self.client.base_url}/buckets/{self.project_id}/todosets/groups/{group_id}.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
            
        response = requests.get(get_group_url, headers=request_headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()
    
    def create_todolist_group(self, data: dict, headers=None) -> dict:
        '''
        Creates a new to-do list group in the to-do set.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md#create-a-to-do-list-group
        
        Parameters:
            data (dict): Complete payload to send to the API.
                         Example: {"name": "Strategy"}
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The created to-do list group data
        '''
        import json
        
        create_group_url = f"{self.client.base_url}/buckets/{self.project_id}/todosets/{self.todoset_id}/groups.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        payload = json.dumps(data)
        response = requests.post(create_group_url, headers=request_headers, data=payload)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            # Extract the web URL from the response and print it
            if 'app_url' in response_data:
                print(f"To-do list group created successfully! View it at: {response_data['app_url']}")
            else:
                print("To-do list group created successfully!")
            return response_data
    
    def reposition_todolist_group(self, group_id: int, data: dict, headers=None) -> dict:
        '''
        Changes the position of a to-do list group.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md#reposition-a-to-do-list-group
        
        Parameters:
            group_id (int): The ID of the to-do list group to reposition.
            data (dict): Complete payload to send to the API.
                         Example: {"position": 3}
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The updated to-do list group data
        '''
        import json
        
        reposition_url = f"{self.client.base_url}/buckets/{self.project_id}/todosets/groups/{group_id}/position.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        payload = json.dumps(data)
        response = requests.put(reposition_url, headers=request_headers, data=payload)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            print("To-do list group repositioned successfully!")
            return response_data
    
    def create_todolist(self, data: dict, headers=None) -> dict:
        '''
        Creates a new to-do list in the to-do set.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#create-a-to-do-list
        
        Parameters:
            data (dict): Complete payload to send to the API.
                         Example: {"name": "Launch checklist", "description": "What we need to do before launch"}
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The created to-do list data
        '''
        import json
        
        create_todolist_url = f"{self.client.base_url}/buckets/{self.project_id}/todosets/{self.todoset_id}/todolists.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        payload = json.dumps(data)
        response = requests.post(create_todolist_url, headers=request_headers, data=payload)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            # Extract the web URL from the response and print it
            if 'app_url' in response_data:
                print(f"To-do list created successfully! View it at: {response_data['app_url']}")
            else:
                print("To-do list created successfully!")
            return response_data