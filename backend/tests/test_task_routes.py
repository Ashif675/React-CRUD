"""Tests for task CRUD APIs (for reference and completeness)."""
import json
import pytest
from backend import db
from backend.models import Task

class TestTaskRoutes:
    """Test suite for task routes."""
    
    def test_get_tasks_empty(self, client):
        """Test getting tasks when none exist."""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_create_task_success(self, client):
        """Test creating a new task."""
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'pending'
        }
        
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'Test Task'
        assert data['description'] == 'Test Description'
        assert data['status'] == 'pending'
        assert 'id' in data
    
    def test_get_task_by_id(self, client, sample_task):
        """Test getting a single task by ID."""
        response = client.get(f'/api/tasks/{sample_task.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == sample_task.id
        assert data['title'] == sample_task.title
    
    def test_update_task(self, client, sample_task):
        """Test updating a task."""
        update_data = {
            'title': 'Updated Task',
            'status': 'completed'
        }
        
        response = client.put(
            f'/api/tasks/{sample_task.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Updated Task'
        assert data['status'] == 'completed'
    
    def test_delete_task(self, client, sample_task):
        """Test deleting a task."""
        task_id = sample_task.id
        
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        
        # Verify it was deleted
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 404

