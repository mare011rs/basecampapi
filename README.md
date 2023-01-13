


# Basecamp API

This package allows simple interaction with [Basecamp API](https://github.com/basecamp/bc3-api) using Python.

## Table of contents

1. [Installation](https://github.com/mare011rs/basecampapi#1-installation)
2. [Initial authentication: Getting your refresh token](https://github.com/mare011rs/basecampapi#2-initial-authentication-getting-your-refresh-token)
3. [Generating and using Basecamp sessions](https://github.com/mare011rs/basecampapi#3-generating-and-using-basecamp-sessions)
4. [Uploading files](https://github.com/mare011rs/basecampapi#4-uploading-files)
5. [Additional information](https://github.com/mare011rs/basecampapi#5-additional-information)

## 1. Installation
The package can be installed from your terminal by typing:

    pip install basecampapi
or

    pip3 install basecampapi


## 2. Initial authentication: Getting your refresh token

To be able to interact with Basecamp's API, we need to provide an access token upon each API request. Basecamp's access tokens are set to expire 2 weeks after being generated, which is why we need to generate a refresh token.

Refresh token allows us to automate the process of generating an access token. We only have to generate the refresh token once and after that we can use it to gain access to Basecamp each time we run our script.

To gain access you need a developer app on Basecamp. App can be created on https://launchpad.37signals.com/integrations, after which you need to use the generated Client ID, Client Secret and the Redirect URI which you provided for initial authentication. You can read more about the authentication process on [Basecamp API Authentication](https://github.com/basecamp/api/blob/master/sections/authentication.md) page.

To begin the authentication process, you need to create a dictionary with your app credentials and use it in the `Authorization` object:

```python
import basecampapi as bc

credentials = {
	client_id: "your-client-id",
	client_secret: "your-client-secret",
	redirect_uri: "your-redirect-uri"
}

auth = bc.Authorization(credentials=credentials)
```

This will open a verification page in your browser. Click on "Yes, I'll allow access":

![Verification page](https://user-images.githubusercontent.com/24939829/209202366-bae05d01-5f8d-4ca6-a0f8-5e1eb9088acd.png  "Verification page")

It will redirect you to the link you provided as Redirect URI, but it will have the verification code in the url address. Save that verification code:

![Verification code](https://user-images.githubusercontent.com/24939829/209202400-d2aa342b-70e1-4fd1-9787-2f3dc1280a57.png  "Verification code")

Use the the `verify()` method on the previously created `Authorization` object and add your verification code to generate the refresh token:

```python
# Verification code variable 
my_verification_code = "17beb4cd"

auth.verify(code=my_verification_code)
```

`verify()` method will print out your refresh token. Make sure to save it and don't share it with anyone because it allows access to your personal Basecamp account and anyone with this information would be able to impersonate you on Basecamp. You will use this refresh token each time you access the Basecamp API, so make sure you save it somewhere safe.




## 3. Generating and using Basecamp sessions
To interact with objects on Basecamp you have to initialize a session object. This object will generate your access token and allow you to interact with other Basecamp objects. To do this, you need to pass your credentials and account ID to the `Basecamp` object.

Your account ID can be found on your Basecamp home page, in the URL address:
- https:<SPAN></SPAN>//3.basecamp.com/<b>YOUR-ACCOUNT-ID</b>/projects

```python
import basecampapi as bc

credentials = {
	"client_id": "your-client-id",
	"client_secret": "your-client-secret",
	"redirect_uri": "your-redirect-uri",
	"refresh_token": "your-refresh-token"
}

basecamp_session = bc.Basecamp(account_id="your-account-id", credentials=credentials)
```
After that you will be able to use your session object within other Basecamp objects.

```python
# Initiates a Campfire object using previously created session
my_campfire = bc.Campfire(campfire_id='your-campfire-id', project_id='your-project-id', session=basecamp_session)
# Sends a campfire message with desired content
my_campfire.write(content="Hello from Python!") 
```


## 4. Uploading files

When attaching images or other files to Basecamp posts we do this by using [Rich text](https://github.com/basecamp/bc3-api/blob/3f71ee57b278be6e71f51488c71197f600395a2b/sections/rich_text.md), which means that we will be sending HTML as content to the Basecamp object we want to interact with. 

Sending rich text through API is not allowed on all Basecamp objects that have rich text by themselves. Best example are Campfires, when interacting with Basecamp you can upload images and files to a campfire or edit the text style, but Basecamp API does not allow this to be done programatically. Here is a [list](https://github.com/basecamp/bc3-api/blob/3f71ee57b278be6e71f51488c71197f600395a2b/sections/rich_text.md#rich-text-content-attributes) of Basecamp endpoints that can accept rich text.


To upload a file to Basecamp, first we need upload the file to Basecamp's server and get its `attachable_sgid`. We can do this by passing the file path to the `upload_file()` method on our `Basecamp` session object:

```python
basecamp_session.upload_file("folder/image.png")
```
After this the file will be on Basecamp's server and it will have an automatically generated `attachable_sgid` Uploaded files can be accessed through session:
```python
print(basecamp_session.files)
```
This returns a list of dictionaries that contain information about the files you uploaded:
```python
[{'filename': 'image.png',
  'file_size': '155291',
  'content-type': 'image/png',
  'sgid': 'your-file-sgid'}]
```
To attach a file inside a Basecamp post, comment or any other object where rich text is accessible through API, we need to send an HTML string  as the content parameter of the object we are interacting with, and we need to use the `<bc-attachment>` tag for any file attachments.

```python
"<bc-attachment sgid='your-file-sgid'></bc-attachment>"
```

Creating a new Message Board post on Basecamp with our uploaded image will look like this:
```python
# Constructing the content string
content = "Hello world! <br> / 
<bc-attachment sgid='#######'></bc-attachment> <br> /
This is an image sent from python."

# Initiating the message board object (using the previously created session object)
message_board = MessageBoard(project_id=123456, message_board_id=123456, session=basecamp_session)

# Creating a message
message_board.create_message(subject="Test message", content=content)
```

## 5. Additional information

Currently available endpoints:
- Campfire - allows reading campfire messages and writing to campfires
- MessageBoard - allows reading, creating and updating messages, as well as reading, creating and updating comments on messages

Future upgrades:
- Vaults (Docs & Files)
- To-dos

