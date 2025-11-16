"""Comment CRUD routes for tasks."""
from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Task, Comment

comment_bp = Blueprint('comments', __name__)

@comment_bp.route('/<int:task_id>/comments', methods=['GET'])
def get_comments(task_id):
    """Get all comments for a specific task."""
    # Verify task exists
    task = Task.query.get_or_404(task_id)
    
    comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.desc()).all()
    return jsonify([comment.to_dict() for comment in comments]), 200

@comment_bp.route('/<int:task_id>/comments/<int:comment_id>', methods=['GET'])
def get_comment(task_id, comment_id):
    """Get a single comment by ID."""
    # Verify task exists
    Task.query.get_or_404(task_id)
    
    comment = Comment.query.filter_by(id=comment_id, task_id=task_id).first_or_404()
    return jsonify(comment.to_dict()), 200

@comment_bp.route('/<int:task_id>/comments', methods=['POST'])
def create_comment(task_id):
    """Create a new comment for a task."""
    # Verify task exists
    task = Task.query.get_or_404(task_id)
    
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400
    
    comment = Comment(
        task_id=task_id,
        content=data['content']
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify(comment.to_dict()), 201

@comment_bp.route('/<int:task_id>/comments/<int:comment_id>', methods=['PUT'])
def update_comment(task_id, comment_id):
    """Update an existing comment."""
    # Verify task exists
    Task.query.get_or_404(task_id)
    
    comment = Comment.query.filter_by(id=comment_id, task_id=task_id).first_or_404()
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400
    
    comment.content = data['content']
    
    db.session.commit()
    
    return jsonify(comment.to_dict()), 200

@comment_bp.route('/<int:task_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(task_id, comment_id):
    """Delete a comment."""
    # Verify task exists
    Task.query.get_or_404(task_id)
    
    comment = Comment.query.filter_by(id=comment_id, task_id=task_id).first_or_404()
    
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment deleted successfully'}), 200

