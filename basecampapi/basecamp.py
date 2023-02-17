import requests
import os
from mimetypes import MimeTypes

class Authorization:
    def __init__(self, credentials: dict) -> str:
        '''
        Begins the initial authorization of the app in order to retrieve the refresh token.

        Parameters
            credentials (dict): A dictionary containing client_id, client_secret and redirect_uri.

        Returns:
            str: Opens the authorization page or prints its link upon execution.
        '''
        self.__credentials = credentials
        self.client_id = credentials["client_id"] 
        self.client_secret = credentials["client_secret"]
        self.redirect_uri = credentials["redirect_uri"]
        self.__authorize_app_url = f"https://launchpad.37signals.com/authorization/new?type=web_server\&client_id={self.client_id}\&redirect_uri={self.redirect_uri}"
        open_string = "open \"\" {}".format(self.__authorize_app_url)
        os.system(open_string)
        print("If authorization dialigue wasn't opened automatically, visit: " + self.__authorize_app_url)
    
    def verify(self, code: str) -> str:
        '''Exchanges verification code for refresh token.

        Parameters:
            code (str): Verification code from the apendage to redirect uri.
        
        Returns
            str: Refresh token.
        '''
        self.verification_code = code
        verification_url = f"https://launchpad.37signals.com/authorization/token?type=web_server&client_id={self.client_id}&redirect_uri={self.redirect_uri}&client_secret={self.client_secret}&code={self.verification_code}"
        response = requests.post(verification_url)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            print(response.json()["refresh_token"])
            
        self.refresh_token = response.json()["refresh_token"]

class Basecamp:
    def __init__(self, account_id: int, credentials: dict):
        '''
        Initializes a Basecamp session.

        Parameters:
            account_id (int): ID number for the Basecamp account.
            credentials (dict): A dictionary containing client_id, client_secret, redirect_uri and refresh_token.
        ''' 
        self.account_id = account_id
        self.__credentials = credentials
        self.client_id = credentials["client_id"] 
        self.client_secret = credentials["client_secret"]
        self.redirect_uri = credentials["redirect_uri"]
        self.refresh_token = credentials["refresh_token"]
        self.basecamp_account_id = account_id
        self.__access_url = f"https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token={self.refresh_token}&client_id={self.client_id}&redirect_uri={self.redirect_uri}&client_secret={self.client_secret}"
        response = requests.post(self.__access_url)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            self.__access_token = response.json()['access_token']
        self.__base_url = f"https://3.basecampapi.com/{self.basecamp_account_id}"
        self.files = {}
        
    def upload_file(self, path: str, filename):
        '''
        Uploads a file to Basecamp's servers and saves the file sgid in Basecamp().files.

        Parameters:
            path (str): Path to file you wish to upload.
            filename
        '''
        attachments_url = f"{self.__base_url}/attachments.json?name={path}"
        file_size = os.path.getsize(path)
        mime = MimeTypes().guess_type(path)[0]
        headers = {
            'Authorization': 'Bearer '+ self.__access_token,
            "Content-Type": mime,
            "Content-Length": str(file_size)
            }

        with open(path, "rb") as file_bytes:
            response = requests.post(attachments_url, headers=headers, data=file_bytes)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            sgid = response.json()['attachable_sgid']
        self.files[filename] = {
            "filename": filename,
            "file_size": str(file_size),
            "content-type": mime,
            "sgid": sgid
        }