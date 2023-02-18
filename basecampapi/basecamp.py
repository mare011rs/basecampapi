import requests

class Basecamp:
    
    __credentials = {}
    __base_url = ""
    
    def __init__(self, credentials: dict, verification_code='Not available!'):
        '''
        Initializes a Basecamp session.

        Parameters:
            account_id (int): ID number for the Basecamp account.
            credentials (dict): A dictionary containing client_id, client_secret, redirect_uri and refresh_token.
        ''' 
        
        Basecamp.__base_url = f"https://3.basecampapi.com/{credentials['account_id']}"
        Basecamp.__credentials = credentials
        
        self.credentials = credentials
        
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
                    Basecamp.__credentials['refresh_token'] = response.json()["refresh_token"]
                    self.credentials['refresh_token'] = response.json()["refresh_token"]
                    self.__get_access()
                    print('refresh_token and access_token added to credentials. ')
                    print('Please save your refresh_token for future access: ' + self.credentials['refresh_token'])
        else:
            self.__get_access()

    
    def __get_access(self):
        self.__access_url = f"https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token={self.credentials['refresh_token']}&client_id={self.credentials['client_id']}&redirect_uri={self.credentials['redirect_uri']}&client_secret={self.credentials['client_secret']}"
        response = requests.post(self.__access_url)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            Basecamp.__credentials['access_token'] = response.json()['access_token']
            print('Authentication successful!')