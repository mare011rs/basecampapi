"""
Test script to verify that the updated Comments class works correctly with the new verbose method names.
"""

from basecampapi import Basecamp

def test_comments_verbose_methods():
    """
    Test the verbose method names in the Comments class.
    
    This is a mock test that doesn't actually make API calls but demonstrates
    how to use the new verbose method names.
    """
    # Initialize the client (with mock credentials)
    client = Basecamp({
        'client_id': 'mock_client_id',
        'redirect_uri': 'mock_redirect_uri',
        'client_secret': 'mock_client_secret',
        'type': 'web_server',
        'refresh_token': 'mock_refresh_token',
        'access_token': 'mock_access_token',
        'expires_at': 9999999999,
        'account_id': '12345678'  # Added missing account_id parameter
    })
    
    # Get a project's comments module
    project_id = 12345678
    comments = client.comments(project_id)
    
    # Example usage of the new verbose method names
    print("Example usage of the new verbose method names:")
    
    # Get all comments on a message
    print("\n1. Get all comments on a message:")
    print("comments.get_all_comments(message_id)")
    
    # Get a specific comment
    print("\n2. Get a specific comment:")
    print("comments.get_comment(comment_id)")
    
    # Create a comment
    print("\n3. Create a comment:")
    print("comments.create_comment(recording_id, data={'content': '<p>This is a comment</p>'})")
    
    # Update a comment
    print("\n4. Update a comment:")
    print("comments.update_comment(comment_id, data={'content': '<p>This is an updated comment</p>'})")
    
    # Trash a comment
    print("\n5. Trash a comment:")
    print("comments.trash_comment(comment_id)")
    
    print("\nAll methods are now using more verbose names for consistency across the package.")

if __name__ == "__main__":
    test_comments_verbose_methods()