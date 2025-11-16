import React from 'react';
import './TaskList.css';

const TaskList = ({ tasks, onEdit, onDelete }) => {
  if (tasks.length === 0) {
    return (
      <div className="empty-state">
        <p>No tasks yet. Create your first task above!</p>
      </div>
    );
  }

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'completed':
        return 'status-badge status-completed';
      case 'in_progress':
        return 'status-badge status-in-progress';
      default:
        return 'status-badge status-pending';
    }
  };

  const formatStatus = (status) => {
    return status.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  return (
    <div className="task-list">
      <h2>Your Tasks ({tasks.length})</h2>
      <div className="tasks-grid">
        {tasks.map(task => (
          <div key={task.id} className="task-card">
            <div className="task-header">
              <h3 className="task-title">{task.title}</h3>
              <span className={getStatusBadgeClass(task.status)}>
                {formatStatus(task.status)}
              </span>
            </div>
            
            {task.description && (
              <p className="task-description">{task.description}</p>
            )}
            
            <div className="task-meta">
              <span className="task-date">
                Created: {new Date(task.created_at).toLocaleDateString()}
              </span>
              {task.comments_count > 0 && (
                <span className="task-comments">
                  {task.comments_count} comment{task.comments_count !== 1 ? 's' : ''}
                </span>
              )}
            </div>
            
            <div className="task-actions">
              <button
                onClick={() => onEdit(task)}
                className="btn-action btn-edit"
                aria-label="Edit task"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="btn-action btn-delete"
                aria-label="Delete task"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskList;

