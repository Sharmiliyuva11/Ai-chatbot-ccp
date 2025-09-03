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
        <div className="modal-overlay" role="dialog" aria-modal="true">
          <div className="add-reminder-modal">
            <div className="modal-header">
              <button
                className="modal-back"
                type="button"
                onClick={() => setShowAddForm(false)}
                aria-label="Close"
              >
                ←
              </button>
              <h2 className="modal-title">Reminders</h2>
              <button
                className="modal-menu"
                type="button"
                aria-label="Menu"
              >
                ≡
              </button>
            </div>

            <div className="modal-card">
              <form onSubmit={handleAddReminder}>
                <div className="modal-field">
                  <label>Task Title<span className="req">*</span></label>
                  <input
                    type="text"
                    value={newReminder.title}
                    onChange={(e) => setNewReminder({ ...newReminder, title: e.target.value })}
                    placeholder="Enter task title"
                    required
                  />
                </div>

                <div className="modal-row">
                  <div className="modal-field">
                    <label>Reminder Date<span className="req">*</span></label>
                    <input
                      type="date"
                      value={newReminder.date}
                      onChange={(e) => setNewReminder({ ...newReminder, date: e.target.value })}
                      required
                    />
                  </div>
                  <div className="modal-field">
                    <label>Reminder Time<span className="req">*</span></label>
                    <input
                      type="time"
                      value={newReminder.time}
                      onChange={(e) => setNewReminder({ ...newReminder, time: e.target.value })}
                      required
                    />
                    <div className="ampm-group">
                      <label className="check">
                        <input
                          type="radio"
                          name="ampm"
                          checked={(newReminder.ampm || 'AM') === 'AM'}
                          onChange={() => setNewReminder({ ...newReminder, ampm: 'AM' })}
                        />
                        <span>AM</span>
                      </label>
                      <label className="check">
                        <input
                          type="radio"
                          name="ampm"
                          checked={newReminder.ampm === 'PM'}
                          onChange={() => setNewReminder({ ...newReminder, ampm: 'PM' })}
                        />
                        <span>PM</span>
                      </label>
                    </div>
                  </div>
                </div>

                <div className="modal-field">
                  <label>Note <span className="optional">(optional)</span></label>
                  <textarea
                    value={newReminder.description}
                    onChange={(e) => setNewReminder({ ...newReminder, description: e.target.value })}
                    placeholder="Add a note"
                    rows="3"
                  />
                </div>

                <div className="modal-field">
                  <label>Reminder Frequency<span className="req">*</span></label>
                  <div className="frequency-group">
                    {['one-time','daily','weekly','monthly','custom'].map((opt) => (
                      <label key={opt} className={`check pill ${newReminder.recurring === opt ? 'active' : ''}`}>
                        <input
                          type="radio"
                          name="recurring"
                          checked={newReminder.recurring === opt}
                          onChange={() => setNewReminder({ ...newReminder, recurring: opt })}
                        />
                        <span>{
                          opt === 'one-time' ? 'One time' : opt.charAt(0).toUpperCase() + opt.slice(1)
                        }</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div className="modal-actions">
                  <button type="submit" className="primary">Save</button>
                  <button type="button" className="secondary" onClick={() => setNewReminder({ title:'', description:'', time:'', date:'', priority:'medium', recurring:'none' })}>Clear</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      <div className="reminders-list">
        {reminders.map((reminder) => (
          <div 
            key={reminder.id} 
            className={`reminder-card ${reminder.completed ? 'completed' : ''} ${reminder.priority}`}
          >
            {/* Badges Row */}
            <div className="reminder-badges">
              <span className={`reminder-badge ${reminder.priority}`}>{reminder.priority.charAt(0).toUpperCase() + reminder.priority.slice(1)}</span>
              <span className={`reminder-badge ${reminder.completed ? 'completed' : 'pending'}`}>{reminder.completed ? 'Completed' : 'Pending'}</span>
              {reminder.recurring !== 'none' && (
                <span className={`reminder-badge ${reminder.recurring}`}>{reminder.recurring.charAt(0).toUpperCase() + reminder.recurring.slice(1)}</span>
              )}
            </div>
            <div className="reminder-main">
              <button 
                className="complete-btn"
                onClick={() => toggleComplete(reminder.id)}
                title={reminder.completed ? 'Mark as Incomplete' : 'Mark as Complete'}
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
                      {reminder.recurring.charAt(0).toUpperCase() + reminder.recurring.slice(1)}
                    </span>
                  )}
                </div>
              </div>
            </div>
            <div className="reminder-divider" />
            <div className="reminder-footer">
              <div className="reminder-actions">
                <button className="action-btn edit" title="Edit Reminder">
                  <Edit3 className="action-icon" />
                </button>
                <button 
                  className="action-btn delete"
                  onClick={() => deleteReminder(reminder.id)}
                  title="Delete Reminder"
                >
                  <Trash2 className="action-icon" />
                </button>
              </div>
              <button 
                className={`cta-btn ${reminder.completed ? 'secondary' : 'primary'}`}
                onClick={() => toggleComplete(reminder.id)}
              >
                {reminder.completed ? 'Mark Incomplete' : 'Mark Complete'}
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