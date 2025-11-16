"""Pytest configuration and fixtures."""
import pytest
from backend.app import create_app
from backend import db
from backend.models import Task, Comment

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def sample_task(app):
    """Create a sample task for testing."""
    with app.app_context():
        task = Task(title='Test Task', description='Test Description', status='pending')
        db.session.add(task)
        db.session.commit()
        return task

@pytest.fixture
def sample_comment(app, sample_task):
    """Create a sample comment for testing."""
    with app.app_context():
        comment = Comment(task_id=sample_task.id, content='Test Comment')
        db.session.add(comment)
        db.session.commit()
        return comment

