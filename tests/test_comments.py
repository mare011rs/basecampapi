"""
Test script for the Comments module.

This script tests the standalone Comments class, including:
- Creating a Comments instance
- Getting comments for different resource types
- Creating comments on different resource types
- Updating comments
- Comparing with resource-specific comment methods
"""

import os
from basecampapi import Basecamp

def test_comments():
    """Test the Comments module."""
    print("Testing Comments module...")
    
    # Replace with your own credentials or use environment variables
    credentials = {
        "account_id": '3694081',
        "client_id": os.environ.get('BASECAMP_CLIENT_ID'),
        "client_secret": os.environ.get('BASECAMP_CLIENT_SECRET'),
        "redirect_uri": os.environ.get('BASECAMP_REDIRECT_URL'),
        "refresh_token": os.environ.get('BASECAMP_REFRESH_TOKEN')
    }
    
    # Create a Basecamp client
    client = Basecamp(credentials=credentials)
    print("Basecamp client created successfully!")
    
    # Test parameters - replace with your own
    project_id = 41622623
    message_board_id = 8470424782
    
    # Test 1: Create a Comments instance
    print("\nTest 1: Creating a Comments instance...")
    comments = client.comments(project_id=project_id)
    print("✅ Comments instance created successfully!")
    
    # Test 2: Compare with MessageBoard comment methods
    print("\nTest 2: Comparing with MessageBoard comment methods...")
    
    # Create a MessageBoard instance
    message_board = client.message_board(project_id=project_id, message_board_id=message_board_id)
    
    # Get all messages
    messages = message_board.get_all_messages()
    if len(messages) > 0:
        message_id = messages[0]['id']
        print(f"Found message with ID: {message_id}")
        
        # Get comments using MessageBoard method
        print("\nGetting comments using MessageBoard.get_all_comments()...")
        mb_comments = message_board.get_all_comments(message_id=message_id)
        print(f"Retrieved {len(mb_comments)} comments using MessageBoard method")
        
        # Get comments using Comments class
        print("\nGetting comments using Comments.get_all()...")
        standalone_comments = comments.get_all(recording_id=message_id)
        print(f"Retrieved {len(standalone_comments)} comments using Comments class")
        
        # Verify that both methods return the same results
        if len(mb_comments) == len(standalone_comments):
            print("✅ Both methods returned the same number of comments")
        else:
            print("❌ Methods returned different numbers of comments")
        
        # Test 3: Create a comment using both methods
        print("\nTest 3: Creating comments using both methods...")
        
        # Create a comment using MessageBoard method
        try:
            print("\nCreating comment using MessageBoard.create_comment()...")
            mb_comment = message_board.create_comment(
                message_id=message_id,
                data={"content": "<p>Test comment from MessageBoard method</p>"}
            )
            print(f"✅ Comment created with ID: {mb_comment['id']}")
            
            # Get the comment using Comments class
            print("\nGetting the comment using Comments.get()...")
            standalone_comment = comments.get(comment_id=mb_comment['id'])
            print(f"✅ Retrieved comment with ID: {standalone_comment['id']}")
            
            # Create a comment using Comments class
            print("\nCreating comment using Comments.create()...")
            new_comment = comments.create(
                recording_id=message_id,
                data={"content": "<p>Test comment from Comments class</p>"}
            )
            print(f"✅ Comment created with ID: {new_comment['id']}")
            
            # Update the comment using Comments class
            print("\nUpdating comment using Comments.update()...")
            updated_comment = comments.update(
                comment_id=new_comment['id'],
                data={"content": "<p>Updated test comment from Comments class</p>"}
            )
            print(f"✅ Comment updated with ID: {updated_comment['id']}")
            
            # Test 4: Test with a different resource type (To-do)
            print("\nTest 4: Testing with a To-do resource...")
            
            # Find a To-do set
            print("\nFinding a To-do set...")
            try:
                project = client.request(
                    method='GET',
                    path=f'/buckets/{project_id}.json'
                )
                
                # Find the to-do set in the project's dock items
                todoset_id = None
                for dock in project.get('dock', []):
                    if dock.get('name') == 'todoset':
                        todoset_id = dock.get('id')
                        break
                
                if todoset_id:
                    print(f"✅ Found To-do set with ID: {todoset_id}")
                    
                    # Get To-do lists
                    todoset = client.todoset(project_id=project_id, todoset_id=todoset_id)
                    todolists = todoset.get_todolists()
                    
                    if len(todolists) > 0:
                        todolist_id = todolists[0]['id']
                        print(f"✅ Found To-do list with ID: {todolist_id}")
                        
                        # Create a To-do list instance
                        todolist = client.todolist(project_id=project_id, todolist_id=todolist_id)
                        
                        # Get To-dos
                        todos = todolist.get_todos()
                        
                        if len(todos) > 0:
                            todo_id = todos[0]['id']
                            print(f"✅ Found To-do with ID: {todo_id}")
                            
                            # Create a comment on the To-do using Comments class
                            print("\nCreating comment on To-do using Comments.create()...")
                            todo_comment = comments.create(
                                recording_id=todo_id,
                                data={"content": "<p>Test comment on a To-do</p>"}
                            )
                            print(f"✅ Comment created on To-do with ID: {todo_comment['id']}")
                            
                            # Get comments on the To-do
                            print("\nGetting comments on To-do using Comments.get_all()...")
                            todo_comments = comments.get_all(recording_id=todo_id)
                            print(f"✅ Retrieved {len(todo_comments)} comments on To-do")
                        else:
                            print("❌ No To-dos found in the To-do list")
                    else:
                        print("❌ No To-do lists found in the To-do set")
                else:
                    print("❌ No To-do set found in the project")
            except Exception as e:
                print(f"❌ Error testing with To-do resource: {str(e)}")
            
            # Test 5: Trash a comment
            print("\nTest 5: Trashing a comment...")
            try:
                trashed = comments.trash(comment_id=new_comment['id'])
                print(f"✅ Comment trashed successfully: {trashed}")
            except Exception as e:
                print(f"❌ Error trashing comment: {str(e)}")
            
        except Exception as e:
            print(f"❌ Error creating or updating comments: {str(e)}")
    else:
        print("❌ No messages found in the message board")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_comments()