import requests

class TodoList:
    def __init__(self, client, project_id: int, todolist_id: int):
        '''
        Interacts with a To-do list, which contains To-dos.
        
        Parameters:
            client: The Basecamp client instance.
            project_id (int): The ID of the Basecamp project containing the To-do list.
            todolist_id (int): ID of the To-do list you wish to target.
        '''
        self.client = client
        self.project_id = project_id
        self.todolist_id = todolist_id
        
        get_todolist_url = f"{client.base_url}/buckets/{self.project_id}/todolists/{self.todolist_id}.json"
        response = requests.get(get_todolist_url, headers=client.get_headers())
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            self.info = response.json()
    
    def get_todos(self, status=None, completed=None, headers=None) -> list:
        '''
        Returns a list of to-dos in the to-do list.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#get-to-dos
        
        Parameters:
            status (str, optional): Filter by status ('archived' or 'trashed'). If not provided, returns active to-dos.
            completed (bool, optional): When set to True, returns only completed to-dos. Can be combined with status.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            list: A list of to-dos in the to-do list
        '''
        get_todos_url = f"{self.client.base_url}/buckets/{self.project_id}/todolists/{self.todolist_id}/todos.json"
        
        # Add query parameters if provided
        params = {}
        if status:
            params['status'] = status
        if completed is not None:
            params['completed'] = str(completed).lower()
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
            
        response = requests.get(get_todos_url, params=params, headers=request_headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()
    
    def get_todo(self, todo_id: int, headers=None) -> dict:
        '''
        Returns information about a specific to-do.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#get-a-to-do
        
        Parameters:
            todo_id (int): The ID of the to-do.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: Information about the to-do
        '''
        get_todo_url = f"{self.client.base_url}/buckets/{self.project_id}/todos/{todo_id}.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
            
        response = requests.get(get_todo_url, headers=request_headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()
    
    def create_todo(self, data: dict, headers=None) -> dict:
        '''
        Creates a new to-do in the to-do list.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#create-a-to-do
        
        Parameters:
            data (dict): Complete payload to send to the API.
                         Example: {
                           "content": "Design signup form",
                           "description": "Make it simple and clean",
                           "assignee_ids": [1007299144],
                           "completion_subscriber_ids": [1007299144],
                           "notify": true,
                           "due_on": "2022-12-31",
                           "starts_on": "2022-12-01"
                         }
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The created to-do data
        '''
        import json
        
        create_todo_url = f"{self.client.base_url}/buckets/{self.project_id}/todolists/{self.todolist_id}/todos.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        payload = json.dumps(data)
        response = requests.post(create_todo_url, headers=request_headers, data=payload)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            # Extract the web URL from the response and print it
            if 'app_url' in response_data:
                print(f"To-do created successfully! View it at: {response_data['app_url']}")
            else:
                print("To-do created successfully!")
            return response_data
    
    def update_todo(self, todo_id: int, data: dict, headers=None) -> dict:
        '''
        Updates an existing to-do.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#update-a-to-do
        
        Parameters:
            todo_id (int): The ID of the to-do to update.
            data (dict): Complete payload to send to the API.
                         Example: {
                           "content": "Updated task name",
                           "description": "Updated description",
                           "assignee_ids": [1007299144],
                           "completion_subscriber_ids": [1007299144],
                           "notify": true,
                           "due_on": "2022-12-31",
                           "starts_on": "2022-12-01"
                         }
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The updated to-do data
        '''
        import json
        
        update_todo_url = f"{self.client.base_url}/buckets/{self.project_id}/todos/{todo_id}.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        payload = json.dumps(data)
        response = requests.put(update_todo_url, headers=request_headers, data=payload)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            # Extract the web URL from the response and print it
            if 'app_url' in response_data:
                print(f"To-do updated successfully! View it at: {response_data['app_url']}")
            else:
                print("To-do updated successfully!")
            return response_data
    
    def complete_todo(self, todo_id: int, headers=None) -> dict:
        '''
        Marks a to-do as completed.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#complete-a-to-do
        
        Parameters:
            todo_id (int): The ID of the to-do to complete.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The completed to-do data
        '''
        complete_todo_url = f"{self.client.base_url}/buckets/{self.project_id}/todos/{todo_id}/completion.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        response = requests.post(complete_todo_url, headers=request_headers)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            print("To-do completed successfully!")
            return response_data
    
    def uncomplete_todo(self, todo_id: int, headers=None) -> dict:
        '''
        Marks a to-do as uncompleted.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#uncomplete-a-to-do
        
        Parameters:
            todo_id (int): The ID of the to-do to uncomplete.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The uncompleted to-do data
        '''
        uncomplete_todo_url = f"{self.client.base_url}/buckets/{self.project_id}/todos/{todo_id}/completion.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        response = requests.delete(uncomplete_todo_url, headers=request_headers)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            print("To-do uncompleted successfully!")
            return response_data
    
    def reposition_todo(self, todo_id: int, data: dict, headers=None) -> dict:
        '''
        Changes the position of a to-do.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#reposition-a-to-do
        
        Parameters:
            todo_id (int): The ID of the to-do to reposition.
            data (dict): Complete payload to send to the API.
                         Example: {"position": 3}
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The repositioned to-do data
        '''
        import json
        
        reposition_url = f"{self.client.base_url}/buckets/{self.project_id}/todos/{todo_id}/position.json"
        
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
            print("To-do repositioned successfully!")
            return response_data
    
    def trash_todo(self, todo_id: int, headers=None) -> dict:
        '''
        Moves a to-do to the trash.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#trash-a-to-do
        
        Parameters:
            todo_id (int): The ID of the to-do to trash.
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The trashed to-do data
        '''
        trash_url = f"{self.client.base_url}/buckets/{self.project_id}/recordings/{todo_id}/status/trashed.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        response = requests.put(trash_url, headers=request_headers)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            print("To-do moved to trash successfully!")
            return response_data
    
    def update(self, data: dict, headers=None) -> dict:
        '''
        Updates the to-do list.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#update-a-to-do-list
        
        Parameters:
            data (dict): Complete payload to send to the API.
                         Example: {"name": "Updated checklist", "description": "Updated description"}
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The updated to-do list data
        '''
        import json
        
        update_url = f"{self.client.base_url}/buckets/{self.project_id}/todolists/{self.todolist_id}.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        payload = json.dumps(data)
        response = requests.put(update_url, headers=request_headers, data=payload)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            # Extract the web URL from the response and print it
            if 'app_url' in response_data:
                print(f"To-do list updated successfully! View it at: {response_data['app_url']}")
            else:
                print("To-do list updated successfully!")
            return response_data
    
    def trash(self, headers=None) -> dict:
        '''
        Moves the to-do list to the trash.
        
        Basecamp API Documentation:
        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#trash-a-to-do-list
        
        Parameters:
            headers (dict, optional): Custom headers to use for this request.
            
        Returns:
            dict: The trashed to-do list data
        '''
        trash_url = f"{self.client.base_url}/buckets/{self.project_id}/recordings/{self.todolist_id}/status/trashed.json"
        
        # Use custom headers or default headers
        request_headers = self.client.get_headers()
        if headers:
            request_headers.update(headers)
        
        response = requests.put(trash_url, headers=request_headers)
        
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            response_data = response.json()
            print("To-do list moved to trash successfully!")
            return response_data