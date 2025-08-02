import React, { useState } from 'react';
import { Users, MessageCircle, Calendar, Clock, Plus, Search } from 'lucide-react';
import './Roundtable.css';

const Roundtable = () => {
  const [activeTab, setActiveTab] = useState('ongoing');

  const sessions = {
    ongoing: [
      {
        id: 1,
        title: 'Anxiety Support Group',
        description: 'A safe space to discuss anxiety management techniques and share experiences.',
        participants: 12,
        maxParticipants: 15,
        moderator: 'Dr. Sarah Johnson',
        time: '2:00 PM - 3:30 PM',
        date: 'Today',
        status: 'live',
        category: 'Mental Health'
      },
      {
        id: 2,
        title: 'Mindfulness & Meditation',
        description: 'Weekly guided meditation and mindfulness practice session.',
        participants: 8,
        maxParticipants: 20,
        moderator: 'Michael Chen',
        time: '6:00 PM - 7:00 PM',
        date: 'Today',
        status: 'starting-soon',
        category: 'Wellness'
      }
    ],
    upcoming: [
      {
        id: 3,
        title: 'Depression Recovery Circle',
        description: 'Peer support group for individuals dealing with depression.',
        participants: 0,
        maxParticipants: 12,
        moderator: 'Dr. Emily Rodriguez',
        time: '10:00 AM - 11:30 AM',
        date: 'Tomorrow',
        status: 'scheduled',
        category: 'Mental Health'
      },
      {
        id: 4,
        title: 'Stress Management Workshop',
        description: 'Learn practical techniques for managing workplace and daily stress.',
        participants: 5,
        maxParticipants: 25,
        moderator: 'James Wilson',
        time: '3:00 PM - 4:30 PM',
        date: 'Dec 28',
        status: 'scheduled',
        category: 'Wellness'
      }
    ],
    past: [
      {
        id: 5,
        title: 'Self-Care Sunday',
        description: 'Weekly self-care practices and wellness tips sharing.',
        participants: 18,
        maxParticipants: 20,
        moderator: 'Lisa Thompson',
        time: '11:00 AM - 12:00 PM',
        date: 'Dec 22',
        status: 'completed',
        category: 'Wellness'
      }
    ]
  };

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
          <button className="create-session-btn">
            <Plus className="icon" />
            Create Session
          </button>
        </div>
      </div>

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
              {session.status === 'live' && (
                <button className="join-btn live">
                  <MessageCircle className="icon" />
                  Join Now
                </button>
              )}
              {session.status === 'starting-soon' && (
                <button className="join-btn soon">
                  <MessageCircle className="icon" />
                  Join Session
                </button>
              )}
              {session.status === 'scheduled' && (
                <button className="join-btn scheduled">
                  <Plus className="icon" />
                  Register
                </button>
              )}
              {session.status === 'completed' && (
                <button className="join-btn completed" disabled>
                  <MessageCircle className="icon" />
                  View Summary
                </button>
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
          <button className="create-session-btn">
            <Plus className="icon" />
            Create New Session
          </button>
        </div>
      )}
    </div>
  );
};

export default Roundtable;