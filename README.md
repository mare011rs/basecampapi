
# Basecamp API integration

  

This module allows you to interact with Basecamp through python.

  

## Table of contents

1. [Requirements](https://github.com/markostefanovic1/basecamp_api#1-requirements "Requirements")
2. [Installation](https://github.com/markostefanovic1/basecamp_api#2-installation "Installation")
3. [How to use](https://github.com/markostefanovic1/basecamp_api#3--how-to-use "How to use")
	- Initial authentication - getting your refresh token
	- Generating and using Basecamp sessions
	- 



## 1. Requirements
- Python 3.7 or higher
- Compatible "requests" library

## 2. Installation

-

  

## 3.  How to use

### Initial authentication - Acquiring your refresh token

To be able to interact with Basecamp's API, you need to provide an access token upon each API request. Basecamp's access tokens are set to expire 2 weeks after being generated, which is why you actually need to acquire a refresh token.

Refresh tokens allow us to automate the process of generating an access token. Generating it requires some manual work, but you only have to do it once and after that you can use it to gain access to Basecamp each time you run your script.

To gain access you need a developer app on Basecamp. App can be created on https://launchpad.37signals.com/integrations, after which you need to use the generated Client ID, Client Secret and the Redirect URI which you provided for initial authentication.

To begin the authentication process, first you need to create a link for acquiring a short-term verification code and go to that link. Use your Client ID and Redirect URI inside of the link:

```python
# Enter your credentials
client_id = "your-client-id"
redirect_uri = "your-redirect-uri"

url = f"https://launchpad.37signals.com/authorization/new?type=web_server&client_id={client_id}&redirect_uri={redirect_uri}"
print(url)
```

Open the link that you printed, it will take you to the verification page. Click on "Yes, I'll allow access":

[![Verification page](https://user-images.githubusercontent.com/105298890/208861486-3faa5a4d-93aa-4523-90d1-632d67334975.png  "Verification page")](https://user-images.githubusercontent.com/105298890/208861486-3faa5a4d-93aa-4523-90d1-632d67334975.png  "Verification page")

It will redirect you to the link you provided as Redirect URI, but it will have the verification code in the url address. Save that verification code:

[![Verification code](https://user-images.githubusercontent.com/105298890/208861435-012c3328-3c41-4489-b57d-436106886fcf.png  "Verification code")](https://user-images.githubusercontent.com/105298890/208861435-012c3328-3c41-4489-b57d-436106886fcf.png  "Verification code")

Use the verification code together with other credentials to send a POST request to the following link (you will need to use the "requests" library for this):

```python
# Enter your credentials
client_id = "your-client-id"
client_secret = "your-client-secret"
redirect_uri = "your-redirect-uri"
verification_code = "your-verification-code"

url = f"https://launchpad.37signals.com/authorization/token?type=web_server&client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={verification_code}"
response = requests.post(url)
refresh_token = response.json()["refresh_token"]
print(refresh_token)
```

Once you do that you will get your refresh token. Make sure to save it and don't share it with anyone because it will grant them access to your basecamp account to do whatever they want while logged in as YOU. You will use this refresh token each time you access the Basecamp API, so make sure you save it somewhere safe.

------------



### Generating and using Basecamp sessions
To interact with objects on Basecamp you have to initialize a session object. This object will generate your access token and allow you to interact with other Basecamp objects. To do this, you need to pass your credentials and account ID to the Basecamp session object.

Your account ID can be found on your Basecamp home page, in the URL address:
- https:<SPAN></SPAN>//3.basecamp.com/<b>YOUR-ACCOUNT-ID</b>/projects

```python
credentials = {
	"client_id": "your-client-id",
	"client_secret": "your-client-secret",
	"redirect_uri": "your-redirect-uri",
	"refresh_token": "your-refresh-token"
}

basecamp_session = Basecamp(account_id="your-account-id", credentials=credentials)
```
After that you will be able to use your session object within other Basecamp objects.

```python
my_campfire = Campfire(campfire_id='your-campfire-id', project_id='your-project-id', session=basecamp_session)
my_campfire.info() # Shows basic information about the campfire
my_campfire.write(content="Hello from Python!") # Sends a campfire message with desired content
```

------------

