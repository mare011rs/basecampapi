class Basecamp:
    
    def __init__(self, account_id, credentials):
        self.account_id = account_id
        self.credentials = credentials
        self.client_id = credentials["client_id"]
        self.client_secret = credentials["client_secret"]
        self.redirect_uri = credentials["redirect_uri"]
        self.refresh_token = credentials["refresh_token"]
        self.basecamp_account_id = account_id
        self.access_url = f"https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token={self.refresh_token}&client_id={self.client_id}&redirect_uri={self.redirect_uri}&client_secret={self.client_secret}"
        self.access_token = requests.post(self.access_url).json()['access_token']
        self.base_url = f"https://3.basecampapi.com/{self.basecamp_account_id}"
        self.files = []
        
    def upload_file(self, path):
        attachments_url = f"{self.base_url}/attachments.json?name={path}"
        file_size = os.path.getsize(path)
        mime = MimeTypes().guess_type(path)[0]
        headers = {
            'Authorization': 'Bearer '+ self.access_token,
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