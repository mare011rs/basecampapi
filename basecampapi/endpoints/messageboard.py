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