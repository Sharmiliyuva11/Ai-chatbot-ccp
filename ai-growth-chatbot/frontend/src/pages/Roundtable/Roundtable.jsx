import React, { useState } from 'react';
import { Users, MessageCircle, Calendar, Clock, Plus, Search } from 'lucide-react';
import api from '../../services/api';
import './Roundtable.css';

const Roundtable = () => {
  const [activeTab, setActiveTab] = useState('ongoing');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newSession, setNewSession] = useState({
    title: '',
    description: '',
    date: '',
    time: '',
    maxParticipants: 10,
    moderator: '',
    category: ''
  });

  const [sessions, setSessions] = useState({ ongoing: [], upcoming: [], past: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [joiningSessionId, setJoiningSessionId] = useState(null);

  // Handler to open the create session modal
  const openCreateSessionModal = () => setShowCreateModal(true);

  // Get user info from localStorage
  const user = React.useMemo(() => {
    try {
      return JSON.parse(localStorage.getItem('user')) || {};
    } catch {
      return {};
    }
  }, []);

  React.useEffect(() => {
    const fetchSessions = async () => {
      setLoading(true);
      setError('');
      try {
        // Use new API endpoint for all sessions
        const response = await api.getAllSessions();
        const allSessions = response.sessions || [];
        // Group sessions by status for tabs
        const grouped = { ongoing: [], upcoming: [], past: [] };
        allSessions.forEach(session => {
          if (session.status === 'live') grouped.ongoing.push(session);
          else if (session.status === 'starting-soon' || session.status === 'scheduled') grouped.upcoming.push(session);
          else grouped.past.push(session);
        });
        setSessions(grouped);
      } catch (err) {
        console.error('Error loading sessions:', err);
        setError('Failed to load sessions. ' + (err.message || 'Please try again.'));
        setSessions({ ongoing: [], upcoming: [], past: [] });
      }
      setLoading(false);
    };
    fetchSessions();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'live': return 'status-live';
      case 'starting-soon': return 'status-soon';
      case 'scheduled': return 'status-scheduled';
      case 'completed': return 'status-completed';
      default: return '';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'live': return 'Live Now';
      case 'starting-soon': return 'Starting Soon';
      case 'scheduled': return 'Scheduled';
      case 'completed': return 'Completed';
      default: return status;
    }
  };

  const handleJoinSession = async (sessionId) => {
    try {
      setJoiningSessionId(sessionId);
      const response = await api.joinSession(sessionId);
      if (response.success) {
        // Refresh sessions after joining
        const sessionsResponse = await api.getAllSessions();
        const allSessions = sessionsResponse.sessions || [];
        const grouped = { ongoing: [], upcoming: [], past: [] };
        allSessions.forEach(session => {
          if (session.status === 'live') grouped.ongoing.push(session);
          else if (session.status === 'starting-soon' || session.status === 'scheduled') grouped.upcoming.push(session);
          else grouped.past.push(session);
        });
        setSessions(grouped);
        alert('Successfully joined the session!');
      } else {
        alert('Failed to join session: ' + (response.message || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error joining session:', error);
      alert('Error joining session: ' + error.message);
    } finally {
      setJoiningSessionId(null);
    }
  };

  return (
    <div className="roundtable">
      <div className="roundtable-header">
        <div className="header-content">
          <h1>Roundtable Sessions</h1>
          <p>Join group discussions and peer support sessions</p>
        </div>
        <div className="header-actions">
          <div className="search-container">
            <Search className="search-icon" />
            <input type="text" placeholder="Search sessions..." />
          </div>
          <button className="create-session-btn" onClick={() => setShowCreateModal(true)}>
            <Plus className="icon" />
            Create Session
          </button>
        </div>
      </div>

      {showCreateModal && (
        <div className="modal-overlay" role="dialog" aria-modal="true">
          <div className="add-reminder-modal">
            <div className="modal-header" style={{background: 'linear-gradient(90deg, #ff9800, #ff5e00)'}}>
              <button className="modal-back" type="button" onClick={() => setShowCreateModal(false)} aria-label="Close">←</button>
              <h2 className="modal-title">Create Session</h2>
              <button className="modal-menu" type="button" aria-label="Menu">≡</button>
            </div>
            <div className="modal-card">
<form onSubmit={async e => {
  e.preventDefault();
  try {
    const response = await api.createSession(newSession);
    if (response.success) {
      // Refresh sessions list after creation
      const sessionsResponse = await api.getAllSessions();
      const allSessions = sessionsResponse.sessions || [];
      const grouped = { ongoing: [], upcoming: [], past: [] };
      allSessions.forEach(session => {
        if (session.status === 'live') grouped.ongoing.push(session);
        else if (session.status === 'starting-soon' || session.status === 'scheduled') grouped.upcoming.push(session);
        else grouped.past.push(session);
      });
      setSessions(grouped);
      setShowCreateModal(false);
      setNewSession({
        title: '',
        description: '',
        date: '',
        time: '',
        maxParticipants: 10,
        moderator: '',
        category: ''
      });
    } else {
      alert('Failed to create session: ' + (response.message || 'Unknown error'));
    }
  } catch (error) {
    alert('Error creating session: ' + error.message);
  }
}}>
  <div className="modal-field">
    <label>Session Title<span className="req">*</span></label>
    <input type="text" value={newSession.title} onChange={e => setNewSession({...newSession, title: e.target.value})} required placeholder="Enter session title" />
  </div>
  <div className="modal-field">
    <label>Description<span className="req">*</span></label>
    <textarea value={newSession.description} onChange={e => setNewSession({...newSession, description: e.target.value})} required placeholder="Describe the session" rows="3" />
  </div>
  <div className="modal-row">
    <div className="modal-field">
      <label>Date<span className="req">*</span></label>
      <input type="date" value={newSession.date} onChange={e => setNewSession({...newSession, date: e.target.value})} required />
    </div>
    <div className="modal-field">
      <label>Time<span className="req">*</span></label>
      <input type="time" value={newSession.time} onChange={e => setNewSession({...newSession, time: e.target.value})} required />
    </div>
  </div>
  <div className="modal-row">
    <div className="modal-field">
      <label>Max Participants<span className="req">*</span></label>
      <input type="number" min="2" max="100" value={newSession.maxParticipants} onChange={e => setNewSession({...newSession, maxParticipants: e.target.value})} required />
    </div>
    <div className="modal-field">
      <label>Moderator<span className="req">*</span></label>
      <input type="text" value={newSession.moderator} onChange={e => setNewSession({...newSession, moderator: e.target.value})} required placeholder="Moderator name" />
    </div>
  </div>
  <div className="modal-field">
    <label>Category<span className="req">*</span></label>
    <input type="text" value={newSession.category} onChange={e => setNewSession({...newSession, category: e.target.value})} required placeholder="e.g. Wellness, Mental Health" />
  </div>
  <div className="modal-actions">
    <button type="submit" className="primary">Save</button>
    <button type="button" className="secondary" onClick={() => setShowCreateModal(false)}>Cancel</button>
  </div>
</form>
            </div>
          </div>
        </div>
      )}

      <div className="session-tabs">
        <button 
          className={`tab ${activeTab === 'ongoing' ? 'active' : ''}`}
          onClick={() => setActiveTab('ongoing')}
        >
          Ongoing ({sessions.ongoing.length})
        </button>
        <button 
          className={`tab ${activeTab === 'upcoming' ? 'active' : ''}`}
          onClick={() => setActiveTab('upcoming')}
        >
          Upcoming ({sessions.upcoming.length})
        </button>
        <button 
          className={`tab ${activeTab === 'past' ? 'active' : ''}`}
          onClick={() => setActiveTab('past')}
        >
          Past ({sessions.past.length})
        </button>
      </div>

      <div className="sessions-grid">
        {sessions[activeTab].map((session) => (
          <div key={session.id} className="session-card">
            <div className="session-header">
              <div className="session-category">{session.category}</div>
              <div className={`session-status ${getStatusColor(session.status)}`}>
                {getStatusText(session.status)}
              </div>
            </div>
            
            <h3 className="session-title">{session.title}</h3>
            <p className="session-description">{session.description}</p>
            
            <div className="session-meta">
              <div className="meta-item">
                <Calendar className="meta-icon" />
                <span>{session.date}</span>
              </div>
              <div className="meta-item">
                <Clock className="meta-icon" />
                <span>{session.time}</span>
              </div>
              <div className="meta-item">
                <Users className="meta-icon" />
                <span>{session.participants}/{session.maxParticipants} participants</span>
              </div>
            </div>
            
            <div className="session-moderator">
              <span>Moderated by: <strong>{session.moderator}</strong></span>
            </div>
            
            <div className="session-progress">
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${(session.participants / session.maxParticipants) * 100}%` }}
                ></div>
              </div>
              <span className="progress-text">
                {session.maxParticipants - session.participants} spots left
              </span>
            </div>
            
            <div className="session-actions">
              {/* If user is the moderator, show 'You are hosting' */}
              {session.moderatorId === user.id ? (
                <span className="host-label">You are hosting</span>
              ) : (
                <>
                  {(session.status === 'live' || session.status === 'starting-soon' || session.status === 'scheduled') && (
                    <button
                      className={`join-btn ${session.status}`}
                      onClick={() => handleJoinSession(session._id)}
                      disabled={session.participants >= session.maxParticipants || joiningSessionId === session._id}
                    >
                      {joiningSessionId === session._id ? 'Joining...' : (
                        <>
                          <MessageCircle className="icon" />
                          {session.status === 'live' ? 'Join Now' : session.status === 'starting-soon' ? 'Join Session' : 'Register'}
                        </>
                      )}
                    </button>
                  )}
                  {session.status === 'completed' && (
                    <button className="join-btn completed" disabled>
                      <MessageCircle className="icon" />
                      View Summary
                    </button>
                  )}
                </>
              )}
            </div>
          </div>
        ))}
      </div>

      {sessions[activeTab].length === 0 && (
        <div className="empty-state">
          <Users className="empty-icon" />
          <h3>No sessions found</h3>
          <p>There are no {activeTab} sessions at the moment.</p>
          <button className="create-session-btn" onClick={openCreateSessionModal}>
            <Plus className="icon" />
            Create New Session
          </button>
        </div>
      )}
    </div>
  );
};

export default Roundtable;