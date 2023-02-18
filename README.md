# Basecamp API

This package allows simple interaction with [Basecamp API](https://github.com/basecamp/bc3-api) using Python.

## Table of contents

1. [Installation](https://github.com/mare011rs/basecampapi#1-installation)
2. [Initial authentication: Getting your refresh token](https://github.com/mare011rs/basecampapi#2-initial-authentication-getting-your-refresh-token)
3. [Authentication with Refresh token](https://github.com/mare011rs/basecampapi#3-authentication-with-refresh-token)
4. [Attachments](https://github.com/mare011rs/basecampapi#4-attachments)
5. [Additional information](https://github.com/mare011rs/basecampapi#5-additional-information)

## 1. Installation
The package can be installed from your terminal by typing:

    pip install basecampapi

You need to have python 3.7 or higher installed.


## 2. Initial authentication: Getting your refresh token

##### You only need to do this the first time. Once you get your Refresh token you should pass it with your credentials to gain access. 
##### If you already have a Refresh token you should skip this step.

To be able to interact with Basecamp's API, we need to provide an access token upon each API request. Basecamp's access tokens are set to expire 2 weeks after being generated, which is why we need to generate a refresh token.

Refresh token allows us to automate the process of generating an access token. We only have to generate the refresh token once and after that we can use it to gain access to Basecamp each time we run our script.

To gain access you need a developer app on Basecamp. App can be created on https://launchpad.37signals.com/integrations, after which you need to use the generated Client ID, Client Secret and the Redirect URI which you provided for initial authentication. You can read more about the authentication process on [Basecamp API Authentication](https://github.com/basecamp/api/blob/master/sections/authentication.md) page.

To begin the authentication process, you need to create a dictionary with your app credentials and use it in the `Basecamp` object:

```python
from basecampapi import Basecamp

your_credentials = {
	"account_id": "your-account-id",
	"client_id": "your-client-id",
	"client_secret": "your-client-secret",
	"redirect_uri": "your-redirect-uri"
}

bc = Basecamp(credentials=your_credentials)
```
Your account ID can be found on your Basecamp home page, in the URL address:
> https:<SPAN></SPAN>//3.basecamp.com/<b>YOUR-ACCOUNT-ID</b>/projects

If your credentials dictionary does not contain a "refresh_token", an error will be raised which contains a link for the authorization of your app. You need to open that link on the browser where you are logged into your Basecamp account and  click on "Yes, I'll allow access":

![Verification page](https://user-images.githubusercontent.com/24939829/209202366-bae05d01-5f8d-4ca6-a0f8-5e1eb9088acd.png  "Verification page")

Clicking that button will redirect you to the link you provided as Redirect URI in your credentials, but it will have the verification code in the url address. Save that verification code:

![Verification code](https://user-images.githubusercontent.com/24939829/209202400-d2aa342b-70e1-4fd1-9787-2f3dc1280a57.png  "Verification code")

Initiate the `Basecamp` object again, and provide the code you gathered via the `verification_code` parameter:

```python
# Verification code variable 
your_verification_code = "17beb4cd"

bc = Basecamp(credentials=your_credentials, verification_code=your_verification_code)
```

This will generate your Refresh token and use that token right away to generate the Access token for your current session. You need to generate your Refresh token only once, but that Refresh token will be used to generate Access token each time you initialize the `Basecamp` object.


## 3. Authentication with Refresh token

To interact with objects on Basecamp you have to initialize the `Basecamo` object. This object will generate your access token and allow you to interact with other Basecamp objects. 

```python
from basecampapi import Basecamp

your_credentials = {
	"account_id": "your-account-id",
	"client_id": "your-client-id",
	"client_secret": "your-client-secret",
	"redirect_uri": "your-redirect-uri",
	"refresh_token": "your-refresh-token"
}

bc = Basecamp(credentials=your_credentials)
```
This generates the Access token which is then used in object that interact with Basecamp.

```python
from basecampapi import Campfire

# Initiates a Campfire object using previously created session
your_campfire = Campfire(campfire_id='your-campfire-id', project_id='your-project-id')

# Sends a campfire message with desired content
your_campfire.write(content="Hello from Python!") 
```


## 4. Attachments

When attaching images or other files to Basecamp posts we do this by using [Rich text](https://github.com/basecamp/bc3-api/blob/3f71ee57b278be6e71f51488c71197f600395a2b/sections/rich_text.md), which means that we will be sending HTML as content to the Basecamp object we want to interact with. 

Sending rich text through API is not allowed on all Basecamp objects that have rich text by themselves. Best example are Campfires, when interacting with Basecamp you can upload images and files to a campfire or edit the text style, but Basecamp API does not allow this to be done programatically. Here is a [list](https://github.com/basecamp/bc3-api/blob/3f71ee57b278be6e71f51488c71197f600395a2b/sections/rich_text.md#rich-text-content-attributes) of Basecamp endpoints that can accept rich text.


To upload a file to Basecamp, first we need upload the file to Basecamp's server and get its `attachable_sgid`. You can do this by using the `Attachments` object and its `upload_file()` method:

```python
from basecampapi import Attachments

my_att = Attachments()
my_att.upload_file("folder/image.png", filename="my_image")
```
After this the file will be on Basecamp's server and it will have an automatically generated `attachable_sgid` Uploaded files can be accessed through `Attachments.files` dictionary:
```python
print(my_att.files)
```
This returns a dictionary of dictionaries which contain information about the files you uploaded:
```python
{
	"my_image": {
		'filename': 'my_image',
		'file_size': '155291',
		'content-type': 'image/png',
		'sgid': 'your-file-sgid'
		}
}
```
To attach a file inside a Basecamp post, comment or any other object where rich text is accessible through API, we need to send an HTML string  as the content parameter of the object we are interacting with, and we need to use the `<bc-attachment>` tag for any file attachments.

```python
"<bc-attachment sgid='your-file-sgid'></bc-attachment>"
```

Creating a new Message Board post on Basecamp with our uploaded image will look like this:
```python
from basecampapi import MessageBoard

# Constructing the content string
content = "Hello world! <br> \ 
	<bc-attachment sgid='#######' caption='My image'></bc-attachment> <br> \	
	This is an image sent from python."

# Initiating the message board object
message_board = MessageBoard(project_id=123456, message_board_id=123456)

# Creating a message
message_board.create_message(subject="Test message", content=content)
```

## 5. Additional information

Currently available endpoints:
- Campfire - allows reading campfire messages and writing to campfires
- MessageBoard - allows reading, creating and updating messages, as well as reading, creating and updating comments on messages
- Attachments - used for uploading files and attaching them to with other Basecamp objects

Future upgrades:
- Vaults (Docs & Files)
- To-dos

Request new features in [issues](https://github.com/mare011rs/basecampapi/issues).