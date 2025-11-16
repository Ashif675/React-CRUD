"""Task CRUD routes."""
from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Task

task_bp = Blueprint('tasks', __name__)

@task_bp.route('', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@task_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task by ID."""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

@task_bp.route('', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'pending')
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task."""
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data.get('description')
    if 'status' in data:
        task.status = data['status']
    
    db.session.commit()
    
    return jsonify(task.to_dict()), 200

@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    task = Task.query.get_or_404(task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'}), 200

