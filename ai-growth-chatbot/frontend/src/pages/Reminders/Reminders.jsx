
import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Bell, Plus, Trash2, Clock, Calendar } from 'lucide-react';
import './Reminders.css';


const Reminders = () => {
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingReminder, setEditingReminder] = useState(null);
  const [newReminder, setNewReminder] = useState({
    title: '',
    description: '',
    time: '',
    date: '',
    priority: 'medium',
    recurring: 'one-time',
  });
  const [userEmail, setUserEmail] = useState('');


  useEffect(() => {
    const fetchReminders = async () => {
      setLoading(true);
      try {
        const res = await api.getReminders();
        // API returns {success, reminders}
        if (res && res.success && Array.isArray(res.reminders)) {
          setReminders(res.reminders.map(r => ({
            ...r,
            id: r._id || r.id,
            date: r.remind_at ? r.remind_at.split(' ')[0] : '',
            time: r.remind_at ? r.remind_at.split(' ')[1]?.slice(0,5) : '',
            priority: r.priority || 'medium',
            recurring: r.recurring || 'one-time',
          })));
        } else {
          setReminders([]);
        }
      } catch (err) {
        setReminders([]);
      }
      setLoading(false);
    };
    // Get user email from localStorage if available
    const user = localStorage.getItem('user');
    if (user) {
      try {
        setUserEmail(JSON.parse(user).email || '');
      } catch {}
    }
    fetchReminders();
  }, []);


  const handleAddReminder = async (e) => {
    e.preventDefault();
    if (newReminder.title && newReminder.time && newReminder.date) {
      const remind_at = `${newReminder.date} ${newReminder.time}:00`;
      try {
        let res;
        if (editingReminder) {
          // Update existing reminder
          res = await api.updateReminder(editingReminder.id, {
            title: newReminder.title,
            description: newReminder.description,
            remind_at,
            priority: newReminder.priority,
            recurring: newReminder.recurring,
            email: userEmail,
          });
        } else {
          // Add new reminder
          res = await api.addReminder({
            title: newReminder.title,
            description: newReminder.description,
            remind_at,
            priority: newReminder.priority,
            recurring: newReminder.recurring,
            email: userEmail,
          });
        }
        if (res && res.success) {
          if (editingReminder) {
            // Update UI for edited reminder
            setReminders(reminders.map(r => r.id === editingReminder.id ? {
              ...r,
              title: newReminder.title,
              description: newReminder.description,
              date: newReminder.date,
              time: newReminder.time,
              priority: newReminder.priority,
              recurring: newReminder.recurring,
            } : r));
          } else {
            // Add to UI immediately
            const added = {
              ...res.reminder,
              id: res.reminder?._id || res.reminder?.id || Math.random().toString(),
              date: newReminder.date,
              time: newReminder.time,
              priority: newReminder.priority,
              recurring: newReminder.recurring,
            };
            setReminders([...reminders, added]);
          }
        } else {
          // fallback: refetch
          const all = await api.getReminders();
          setReminders(Array.isArray(all.reminders) ? all.reminders : []);
        }
      } catch (err) {}
      setNewReminder({
        title: '',
        description: '',
        time: '',
        date: '',
        priority: 'medium',
        recurring: 'one-time',
      });
      setEditingReminder(null);
      setShowAddForm(false);
    }
  };


  const deleteReminder = async (id) => {
    try {
      await api.deleteReminder(id);
      setReminders(reminders.filter(reminder => reminder.id !== id && reminder._id !== id));
    } catch (err) {}
  };

  const handleEdit = (reminder) => {
    setEditingReminder(reminder);
    setNewReminder({
      title: reminder.title,
      description: reminder.description,
      time: reminder.time,
      date: reminder.date,
      priority: reminder.priority,
      recurring: reminder.recurring,
    });
    setShowAddForm(true);
  };


  return (
    <div className="reminders-container">
      <div className="reminders-header">
        <h2>Reminders</h2>
        <button className="add-reminder-btn" onClick={() => {
          setShowAddForm(true);
          setEditingReminder(null);
          setNewReminder({
            title: '',
            description: '',
            time: '',
            date: '',
            priority: 'medium',
            recurring: 'one-time',
          });
        }}>
          <Plus /> Add Reminder
        </button>
      </div>
      {showAddForm && (
        <div className="modal-overlay" role="dialog" aria-modal="true">
          <div className="add-reminder-modal">
            <div className="modal-header" style={{background: 'linear-gradient(90deg, #ff5e00, #ff7a1a)'}}>
              <button className="modal-back" type="button" onClick={() => setShowAddForm(false)} aria-label="Close">←</button>
              <h2 className="modal-title">{editingReminder ? 'Edit Reminder' : 'Add Reminder'}</h2>
              <button className="modal-menu" type="button" aria-label="Menu">≡</button>
            </div>
            <div className="modal-card">
              <form onSubmit={handleAddReminder}>
                <div className="modal-field">
                  <label>Title<span className="req">*</span></label>
                  <input
                    type="text"
                    value={newReminder.title}
                    onChange={e => setNewReminder({ ...newReminder, title: e.target.value })}
                    required
                    placeholder="Enter reminder title"
                  />
                </div>
                <div className="modal-field">
                  <label>Description</label>
                  <textarea
                    value={newReminder.description}
                    onChange={e => setNewReminder({ ...newReminder, description: e.target.value })}
                    placeholder="Describe the reminder"
                    rows="3"
                  />
                </div>
                <div className="modal-row">
                  <div className="modal-field">
                    <label>Date<span className="req">*</span></label>
                    <input
                      type="date"
                      value={newReminder.date}
                      onChange={e => setNewReminder({ ...newReminder, date: e.target.value })}
                      required
                    />
                  </div>
                  <div className="modal-field">
                    <label>Time<span className="req">*</span></label>
                    <input
                      type="time"
                      value={newReminder.time}
                      onChange={e => setNewReminder({ ...newReminder, time: e.target.value })}
                      required
                    />
                  </div>
                </div>
                <div className="modal-row">
                  <div className="modal-field">
                    <label>Priority<span className="req">*</span></label>
                    <select
                      value={newReminder.priority}
                      onChange={e => setNewReminder({ ...newReminder, priority: e.target.value })}
                      required
                    >
                      <option value="high">High Priority</option>
                      <option value="medium">Medium Priority</option>
                      <option value="low">Low Priority</option>
                    </select>
                  </div>
                  <div className="modal-field">
                    <label>Recurring<span className="req">*</span></label>
                    <select
                      value={newReminder.recurring}
                      onChange={e => setNewReminder({ ...newReminder, recurring: e.target.value })}
                      required
                    >
                      <option value="one-time">One Time</option>
                      <option value="daily">Daily</option>
                      <option value="weekly">Weekly</option>
                      <option value="monthly">Monthly</option>
                      <option value="custom">Custom</option>
                    </select>
                  </div>
                </div>
                <div className="modal-actions">
                  <button type="submit" className="primary">{editingReminder ? 'Save' : 'Add'}</button>
                  <button type="button" className="secondary" onClick={() => setShowAddForm(false)}>Cancel</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
      <div className="reminders-list">
        {loading ? (
          <div className="loading">Loading...</div>
        ) : reminders.length === 0 ? (
          <div className="empty-state">
            <Bell className="empty-icon" />
            <h3>No reminders yet</h3>
            <p>Create your first reminder to get started</p>
          </div>
        ) : (
          reminders.map(reminder => (
            <div key={reminder.id} className={`reminder-card ${reminder.priority}`}>
              <div className="reminder-main">
                <div className="reminder-content">
                  <div className="reminder-title-row">
                    <h3 className="reminder-title">{reminder.title}</h3>
                    <div className="reminder-badges">
                      <span className={`reminder-badge ${reminder.priority}`}>{reminder.priority.charAt(0).toUpperCase() + reminder.priority.slice(1)}</span>
                      <span className={`reminder-badge ${reminder.recurring}`}>{reminder.recurring.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                    </div>
                  </div>
                  <p className="reminder-description">{reminder.description}</p>
                  <div className="reminder-meta">
                    <span><Clock className="meta-icon" /> {reminder.time}</span>
                    <span><Calendar className="meta-icon" /> {reminder.date}</span>
                  </div>
                </div>
              </div>
              <div className="reminder-divider"></div>
              <div className="reminder-footer">
                {/* Removed Open, Share, and View Details buttons as per user request */}
                <button className="cta-btn secondary" onClick={() => handleEdit(reminder)}>
                  Edit
                </button>
                <button className="action-btn delete" onClick={() => deleteReminder(reminder.id)}>
                  <Trash2 />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Reminders;