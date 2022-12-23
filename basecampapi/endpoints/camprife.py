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