import React, { useState } from 'react';
import { 
  Plus, 
  Calendar, 
  Clock, 
  Bell, 
  Trash2, 
  Edit3,
  CheckCircle,
  Circle,
  AlertCircle
} from 'lucide-react';
import './Reminders.css';

const Reminders = () => {
  const [reminders, setReminders] = useState([
    {
      id: 1,
      title: 'Morning Meditation',
      description: 'Start the day with 10 minutes of mindfulness',
      time: '07:00',
      date: '2024-01-15',
      priority: 'high',
      completed: false,
      recurring: 'daily'
    },
    {
      id: 2,
      title: 'Drink Water',
      description: 'Stay hydrated throughout the day',
      time: '10:00',
      date: '2024-01-15',
      priority: 'medium',
      completed: true,
      recurring: 'hourly'
    },
    {
      id: 3,
      title: 'Evening Reflection',
      description: 'Journal about the day and set tomorrow\'s goals',
      time: '21:00',
      date: '2024-01-15',
      priority: 'high',
      completed: false,
      recurring: 'daily'
    }
  ]);

  const [showAddForm, setShowAddForm] = useState(false);
  const [newReminder, setNewReminder] = useState({
    title: '',
    description: '',
    time: '',
    date: '',
    priority: 'medium',
    recurring: 'none'
  });

  const handleAddReminder = (e) => {
    e.preventDefault();
    if (newReminder.title && newReminder.time && newReminder.date) {
      const reminder = {
        id: Date.now(),
        ...newReminder,
        completed: false
      };
      setReminders([...reminders, reminder]);
      setNewReminder({
        title: '',
        description: '',
        time: '',
        date: '',
        priority: 'medium',
        recurring: 'none'
      });
      setShowAddForm(false);
    }
  };

  const toggleComplete = (id) => {
    setReminders(reminders.map(reminder => 
      reminder.id === id 
        ? { ...reminder, completed: !reminder.completed }
        : reminder
    ));
  };

  const deleteReminder = (id) => {
    setReminders(reminders.filter(reminder => reminder.id !== id));
  };

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high':
        return <AlertCircle className="priority-icon high" />;
      case 'medium':
        return <Clock className="priority-icon medium" />;
      case 'low':
        return <Bell className="priority-icon low" />;
      default:
        return <Bell className="priority-icon" />;
    }
  };

  const completedCount = reminders.filter(r => r.completed).length;
  const totalCount = reminders.length;
  const completionRate = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  return (
    <div className="reminders-page">
      <div className="reminders-header">
        <div className="header-content">
          <h1>Daily Reminders</h1>
          <p>Stay on track with your daily tasks and goals</p>
        </div>
        <div className="header-stats">
          <div className="stat-card">
            <div className="stat-value">{completedCount}/{totalCount}</div>
            <div className="stat-label">Completed Today</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{completionRate}%</div>
            <div className="stat-label">Completion Rate</div>
          </div>
        </div>
      </div>

      <div className="reminders-actions">
        <button 
          className="add-reminder-btn"
          onClick={() => setShowAddForm(true)}
        >
          <Plus className="btn-icon" />
          Add New Reminder
        </button>
      </div>

      {showAddForm && (
        <div className="add-reminder-form">
          <div className="form-header">
            <h3>Create New Reminder</h3>
            <button 
              className="close-btn"
              onClick={() => setShowAddForm(false)}
            >
              ×
            </button>
          </div>
          <form onSubmit={handleAddReminder}>
            <div className="form-row">
              <div className="form-group">
                <label>Title</label>
                <input
                  type="text"
                  value={newReminder.title}
                  onChange={(e) => setNewReminder({...newReminder, title: e.target.value})}
                  placeholder="Enter reminder title"
                  required
                />
              </div>
              <div className="form-group">
                <label>Priority</label>
                <select
                  value={newReminder.priority}
                  onChange={(e) => setNewReminder({...newReminder, priority: e.target.value})}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>
            
            <div className="form-group">
              <label>Description</label>
              <textarea
                value={newReminder.description}
                onChange={(e) => setNewReminder({...newReminder, description: e.target.value})}
                placeholder="Enter reminder description"
                rows="3"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Date</label>
                <input
                  type="date"
                  value={newReminder.date}
                  onChange={(e) => setNewReminder({...newReminder, date: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Time</label>
                <input
                  type="time"
                  value={newReminder.time}
                  onChange={(e) => setNewReminder({...newReminder, time: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Recurring</label>
                <select
                  value={newReminder.recurring}
                  onChange={(e) => setNewReminder({...newReminder, recurring: e.target.value})}
                >
                  <option value="none">None</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>
            </div>

            <div className="form-actions">
              <button type="button" onClick={() => setShowAddForm(false)}>
                Cancel
              </button>
              <button type="submit">
                Create Reminder
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="reminders-list">
        {reminders.map((reminder) => (
          <div 
            key={reminder.id} 
            className={`reminder-card ${reminder.completed ? 'completed' : ''} ${reminder.priority}`}
          >
            <div className="reminder-main">
              <button 
                className="complete-btn"
                onClick={() => toggleComplete(reminder.id)}
              >
                {reminder.completed ? 
                  <CheckCircle className="complete-icon completed" /> : 
                  <Circle className="complete-icon" />
                }
              </button>
              
              <div className="reminder-content">
                <div className="reminder-title-row">
                  <h3 className="reminder-title">{reminder.title}</h3>
                  {getPriorityIcon(reminder.priority)}
                </div>
                <p className="reminder-description">{reminder.description}</p>
                <div className="reminder-meta">
                  <span className="reminder-time">
                    <Clock className="meta-icon" />
                    {reminder.time}
                  </span>
                  <span className="reminder-date">
                    <Calendar className="meta-icon" />
                    {new Date(reminder.date).toLocaleDateString()}
                  </span>
                  {reminder.recurring !== 'none' && (
                    <span className="reminder-recurring">
                      <Bell className="meta-icon" />
                      {reminder.recurring}
                    </span>
                  )}
                </div>
              </div>
            </div>
            
            <div className="reminder-actions">
              <button className="action-btn edit">
                <Edit3 className="action-icon" />
              </button>
              <button 
                className="action-btn delete"
                onClick={() => deleteReminder(reminder.id)}
              >
                <Trash2 className="action-icon" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {reminders.length === 0 && (
        <div className="empty-state">
          <Bell className="empty-icon" />
          <h3>No reminders yet</h3>
          <p>Create your first reminder to get started</p>
        </div>
      )}
    </div>
  );
};

export default Reminders;