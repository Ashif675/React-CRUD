"""Tests for comment CRUD APIs."""
import json
import pytest
from backend import db
from backend.models import Task, Comment

class TestCommentRoutes:
    """Test suite for comment routes."""
    
    def test_get_comments_empty(self, client, sample_task):
        """Test getting comments when none exist."""
        response = client.get(f'/api/tasks/{sample_task.id}/comments')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_get_comments_with_data(self, client, sample_task):
        """Test getting comments when they exist."""
        # Create a comment
        comment = Comment(task_id=sample_task.id, content='First Comment')
        db.session.add(comment)
        db.session.commit()
        
        response = client.get(f'/api/tasks/{sample_task.id}/comments')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['content'] == 'First Comment'
        assert data[0]['task_id'] == sample_task.id
    
    def test_get_comments_task_not_found(self, client):
        """Test getting comments for non-existent task."""
        response = client.get('/api/tasks/999/comments')
        assert response.status_code == 404
    
    def test_get_single_comment(self, client, sample_task, sample_comment):
        """Test getting a single comment by ID."""
        response = client.get(f'/api/tasks/{sample_task.id}/comments/{sample_comment.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == sample_comment.id
        assert data['content'] == 'Test Comment'
        assert data['task_id'] == sample_task.id
    
    def test_get_single_comment_not_found(self, client, sample_task):
        """Test getting a non-existent comment."""
        response = client.get(f'/api/tasks/{sample_task.id}/comments/999')
        assert response.status_code == 404
    
    def test_get_single_comment_wrong_task(self, client, sample_task):
        """Test getting a comment that belongs to a different task."""
        # Create another task
        task2 = Task(title='Task 2', description='Description 2')
        db.session.add(task2)
        db.session.commit()
        
        # Create comment for task2
        comment2 = Comment(task_id=task2.id, content='Comment for Task 2')
        db.session.add(comment2)
        db.session.commit()
        
        # Try to get comment2 using task1's ID
        response = client.get(f'/api/tasks/{sample_task.id}/comments/{comment2.id}')
        assert response.status_code == 404
    
    def test_create_comment_success(self, client, sample_task):
        """Test creating a new comment."""
        comment_data = {
            'content': 'New Comment'
        }
        
        response = client.post(
            f'/api/tasks/{sample_task.id}/comments',
            data=json.dumps(comment_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['content'] == 'New Comment'
        assert data['task_id'] == sample_task.id
        assert 'id' in data
        assert 'created_at' in data
    
    def test_create_comment_missing_content(self, client, sample_task):
        """Test creating a comment without content."""
        comment_data = {}
        
        response = client.post(
            f'/api/tasks/{sample_task.id}/comments',
            data=json.dumps(comment_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_comment_empty_content(self, client, sample_task):
        """Test creating a comment with empty content."""
        comment_data = {'content': ''}
        
        response = client.post(
            f'/api/tasks/{sample_task.id}/comments',
            data=json.dumps(comment_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_create_comment_task_not_found(self, client):
        """Test creating a comment for non-existent task."""
        comment_data = {'content': 'Comment for non-existent task'}
        
        response = client.post(
            '/api/tasks/999/comments',
            data=json.dumps(comment_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_update_comment_success(self, client, sample_task, sample_comment):
        """Test updating an existing comment."""
        update_data = {
            'content': 'Updated Comment Content'
        }
        
        response = client.put(
            f'/api/tasks/{sample_task.id}/comments/{sample_comment.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['content'] == 'Updated Comment Content'
        assert data['id'] == sample_comment.id
        
        # Verify it was actually updated in the database
        updated_comment = Comment.query.get(sample_comment.id)
        assert updated_comment.content == 'Updated Comment Content'
    
    def test_update_comment_missing_content(self, client, sample_task, sample_comment):
        """Test updating a comment without providing content."""
        update_data = {}
        
        response = client.put(
            f'/api/tasks/{sample_task.id}/comments/{sample_comment.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_comment_not_found(self, client, sample_task):
        """Test updating a non-existent comment."""
        update_data = {'content': 'Updated Content'}
        
        response = client.put(
            f'/api/tasks/{sample_task.id}/comments/999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_update_comment_wrong_task(self, client, sample_task):
        """Test updating a comment that belongs to a different task."""
        # Create another task and comment
        task2 = Task(title='Task 2', description='Description 2')
        db.session.add(task2)
        db.session.commit()
        
        comment2 = Comment(task_id=task2.id, content='Comment for Task 2')
        db.session.add(comment2)
        db.session.commit()
        
        # Try to update comment2 using task1's ID
        update_data = {'content': 'Hacked Content'}
        response = client.put(
            f'/api/tasks/{sample_task.id}/comments/{comment2.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_delete_comment_success(self, client, sample_task, sample_comment):
        """Test deleting a comment."""
        comment_id = sample_comment.id
        
        response = client.delete(f'/api/tasks/{sample_task.id}/comments/{comment_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Comment deleted successfully'
        
        # Verify it was actually deleted
        deleted_comment = Comment.query.get(comment_id)
        assert deleted_comment is None
    
    def test_delete_comment_not_found(self, client, sample_task):
        """Test deleting a non-existent comment."""
        response = client.delete(f'/api/tasks/{sample_task.id}/comments/999')
        assert response.status_code == 404
    
    def test_delete_comment_wrong_task(self, client, sample_task):
        """Test deleting a comment that belongs to a different task."""
        # Create another task and comment
        task2 = Task(title='Task 2', description='Description 2')
        db.session.add(task2)
        db.session.commit()
        
        comment2 = Comment(task_id=task2.id, content='Comment for Task 2')
        db.session.add(comment2)
        db.session.commit()
        
        # Try to delete comment2 using task1's ID
        response = client.delete(f'/api/tasks/{sample_task.id}/comments/{comment2.id}')
        assert response.status_code == 404
    
    def test_multiple_comments_for_task(self, client, sample_task):
        """Test that a task can have multiple comments."""
        # Create multiple comments
        comments_data = [
            {'content': 'First Comment'},
            {'content': 'Second Comment'},
            {'content': 'Third Comment'}
        ]
        
        for comment_data in comments_data:
            response = client.post(
                f'/api/tasks/{sample_task.id}/comments',
                data=json.dumps(comment_data),
                content_type='application/json'
            )
            assert response.status_code == 201
        
        # Get all comments
        response = client.get(f'/api/tasks/{sample_task.id}/comments')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 3

