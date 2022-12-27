class Authorization:
    def __init__(self, credentials):
        self.__credentials = credentials
        self.client_id = credentials["client_id"] 
        self.client_secret = credentials["client_secret"]
        self.redirect_uri = credentials["redirect_uri"]
        self.__authorize_app_url = f"https://launchpad.37signals.com/authorization/new?type=web_server\&client_id={self.client_id}\&redirect_uri={self.redirect_uri}"
        open_string = "open \"\" {}".format(self.__authorize_app_url)
        os.system(open_string)
        print("If authorization dialigue wasn't opened automatically, visit: " + self.__authorize_app_url)
    
    def verify(self, code):
        self.verification_code = code
        verification_url = f"https://launchpad.37signals.com/authorization/token?type=web_server&client_id={self.client_id}&redirect_uri={self.redirect_uri}&client_secret={self.client_secret}&code={self.verification_code}"
        response = requests.post(verification_url)
        self.refresh_token = response.json()["refresh_token"]
        print(self.refresh_token)

class Basecamp:
    
    def __init__(self, account_id, credentials):
        self.account_id = account_id
        self.__credentials = credentials
        self.client_id = credentials["client_id"] 
        self.client_secret = credentials["client_secret"]
        self.redirect_uri = credentials["redirect_uri"]
        self.refresh_token = credentials["refresh_token"]
        self.basecamp_account_id = account_id
        self.__access_url = f"https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token={self.refresh_token}&client_id={self.client_id}&redirect_uri={self.redirect_uri}&client_secret={self.client_secret}"
        self.__access_token = requests.post(self.__access_url).json()['access_token']
        self.__base_url = f"https://3.basecampapi.com/{self.basecamp_account_id}"
        self.files = []
        
    def upload_file(self, path):
        attachments_url = f"{self.__base_url}/attachments.json?name={path}"
        file_size = os.path.getsize(path)
        mime = MimeTypes().guess_type(path)[0]
        headers = {
            'Authorization': 'Bearer '+ self.__access_token,
            "Content-Type": mime,
            "Content-Length": str(file_size)
            }

        with open(path, "rb") as content:
            sgid = requests.post(attachments_url, headers=headers, data=content).json()['attachable_sgid']
        file = {
            "filename": os.path.basename(path),
            "file_size": str(file_size),
            "content-type": mime,
            "sgid": sgid
        }
        self.files.append(file)