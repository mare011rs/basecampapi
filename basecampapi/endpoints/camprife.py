class Campfire:
        
    def __init__(self, project_id, campfire_id, session):
        self.__project_id = project_id
        self.__campfire_id = campfire_id
        self.__access_token = session._Basecamp__access_token
        self.__base_url = session._Basecamp__base_url
        self.__headers = {
            'Authorization': 'Bearer '+ self.__access_token,
            "Content-Type": "application/json"
        }        

    def info(self):
        get_campfire_url = f"{self.__base_url}/buckets/{self.__project_id}/chats/{self.__campfire_id}.json"
        return requests.get(get_campfire_url, headers=self.__headers).json()
    
    def get_lines(self):
        get_lines_url = f"{self.__base_url}/buckets/{self.__project_id}/chats/{self.__campfire_id}/lines.json"
        return requests.get(get_lines_url, headers=self.__headers).json()
    
    def write(self, content):
        write_url = f"{self.__base_url}/buckets/{self.__project_id}/chats/{self.__campfire_id}/lines.json"
        requests.post(write_url, headers=self.__headers, data='{"content": "'+content+'"}')
        print("Sent to campfire successfully!")