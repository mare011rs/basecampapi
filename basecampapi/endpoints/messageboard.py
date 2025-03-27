import requests

from ..basecamp import Basecamp

class MessageBoard(Basecamp):

    def __init__(self, project_id: int, message_board_id: int):
        '''
        Interacts with Message Boards, Messages and Message comments.

        Parameters:
            project_id (int): The ID the Basecamp project containing the Message Board.
            message_board_id (int): ID of the Message Board you wish to target.
        '''

        self.__base_url = Basecamp._Basecamp__base_url
        self.__credentials = Basecamp._Basecamp__credentials
        self.project_id = project_id
        self.message_board_id = message_board_id

        self.__headers = {
            'Authorization': 'Bearer '+ self.__credentials['access_token'],
            "Content-Type": "application/json"
        }

        get_all_messages_url = f"{self.__base_url}/buckets/{self.project_id}/message_boards/{self.message_board_id}/messages.json"
        response = requests.get(get_all_messages_url, headers=self.__headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            self.__messages = response.json()

    def get_all_messages(self) -> list:
        '''
        Returns:
            list: A list of all messages posted on the Message Board
        '''
        return self.__messages

    def get_message(self, message_id: int) -> dict:
        '''
        Returns all information about a message, together with its content.

        Parameters:
            message_id (int): The ID of the message that you wish to read.
        '''
        self.message_id = message_id
        get_message_url = f"{self.__base_url}/buckets/{self.project_id}/messages/{self.message_id}.json"
        response = requests.get(get_message_url, headers=self.__headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()

    def create_message(self, subject: str, content: str):
        '''
        Creates a new Message Board post (a new message). Messages can contain files and rich text.

        Parameters:
            subject (str): Message title.
            content (str): Message body.
        '''
        import json

        create_message_url = f"{self.__base_url}/buckets/{self.project_id}/message_boards/{self.message_board_id}/messages.json"

        payload = json.dumps({
            "subject": subject,
            "content": content,
            "status": "active"
        })

        response = requests.post(create_message_url, headers=self.__headers, data=payload)

        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            print("Message created successfully!")

    def update_message(self, message_id: int, subject: str, content: str):
        '''
        Replaces the content and/or subject of an already existing message.

        Parameters:
            message_id (int): The ID of the message to update.
            subject (str): Updated subject.
            content (str): Updated content.
        '''
        import json

        update_message_url = f"{self.__base_url}/buckets/{self.project_id}/messages/{message_id}.json"

        payload = json.dumps({
            "subject": subject,
            "content": content
        })

        response = requests.put(update_message_url, headers=self.__headers, data=payload)

        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            print("Message updated successfully!")

    def get_all_comments(self, message_id: int) -> list:
        '''
        Gets a list of all the comments on a selected message board post.

        Parameters:
            message_id (int): The ID of the message to return the comments for.

        Returns:
            list: A list of comments on the message.
        '''
        get_all_comments_url = f"{self.__base_url}/buckets/{self.project_id}/recordings/{message_id}/comments.json"
        response = requests.get(get_all_comments_url, headers=self.__headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()

    def get_comment(self, comment_id: int) -> dict:
        '''
        Gets information and content of a specific comment.

        Parameters:
            comment_id (int): The ID of the comment to return the information for.

        Returns:
            dict: Information about the comment.
        '''
        self.comment_id = comment_id
        get_comment_url = f"{self.__base_url}/buckets/{self.project_id}/comments/{self.comment_id}.json"
        response = requests.get(get_comment_url, headers=self.__headers)
        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            return response.json()

    def create_comment(self, message_id: int, content: str):
        '''
        Creates a new comment on a message board post. Comments can contain files and rich text.

        Parameters:
            message_id (int): The ID of the message on Basecamp to comment on.
            content (str): The body of the comment.
        '''
        import json

        create_comment_url = f"{self.__base_url}/buckets/{self.project_id}/recordings/{message_id}/comments.json"

        # Use json.dumps to properly encode the content as JSON
        payload = json.dumps({"content": content})

        response = requests.post(create_comment_url, headers=self.__headers, data=payload)

        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            print("Comment created successfully!")

    def update_comment(self, comment_id: int, content: str):
        '''
        Updates an existing comment on a message board post.

        Parameters:
            comment_id (int): The ID of the comment to update.
            content (str): The updated body of the comment.
        '''
        import json

        update_comment_url = f"{self.__base_url}/buckets/{self.project_id}/comments/{comment_id}.json"

        # Use json.dumps for proper JSON encoding
        payload = json.dumps({"content": content})

        response = requests.put(update_comment_url, headers=self.__headers, data=payload)

        if not response.ok:
            raise Exception(f"Status code: {response.status_code}. {response.reason}. Error text: {response.text}.")
        else:
            print("Comment updated successfully!")