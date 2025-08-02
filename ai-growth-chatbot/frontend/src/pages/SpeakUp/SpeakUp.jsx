import React, { useState } from 'react';
import { 
  MessageSquare, 
  Send, 
  Mic, 
  MicOff, 
  Phone, 
  Video, 
  Calendar,
  Clock,
  User,
  Shield,
  Heart
} from 'lucide-react';
import './SpeakUp.css';

const SpeakUp = () => {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [activeTab, setActiveTab] = useState('chat');

  const chatHistory = [
    {
      id: 1,
      type: 'bot',
      message: "Hello! I'm here to listen and support you. How are you feeling today?",
      timestamp: '2:30 PM'
    },
    {
      id: 2,
      type: 'user',
      message: "I've been feeling quite anxious lately about work and personal life.",
      timestamp: '2:32 PM'
    },
    {
      id: 3,
      type: 'bot',
      message: "I understand that anxiety can be overwhelming. It's completely normal to feel this way when dealing with multiple stressors. Would you like to talk about what specifically is causing you the most concern?",
      timestamp: '2:33 PM'
    },
    {
      id: 4,
      type: 'user',
      message: "It's mainly the pressure at work and feeling like I'm not doing enough.",
      timestamp: '2:35 PM'
    }
  ];

  const counselors = [
    {
      id: 1,
      name: 'Dr. Sarah Johnson',
      specialty: 'Anxiety & Depression',
      rating: 4.9,
      experience: '8 years',
      image: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=100&h=100&fit=crop&crop=face',
      available: true,
      nextSlot: 'Today 3:00 PM'
    },
    {
      id: 2,
      name: 'Dr. Michael Chen',
      specialty: 'Stress Management',
      rating: 4.8,
      experience: '12 years',
      image: 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=100&h=100&fit=crop&crop=face',
      available: false,
      nextSlot: 'Tomorrow 10:00 AM'
    },
    {
      id: 3,
      name: 'Dr. Emily Rodriguez',
      specialty: 'Relationship Counseling',
      rating: 4.9,
      experience: '10 years',
      image: 'https://images.unsplash.com/photo-1594824388853-d0c2b8e8e8e8?w=100&h=100&fit=crop&crop=face',
      available: true,
      nextSlot: 'Today 4:30 PM'
    }
  ];

  const handleSendMessage = () => {
    if (message.trim()) {
      // Add message sending logic here
      console.log('Sending message:', message);
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    // Add voice recording logic here
  };

  return (
    <div className="speak-up">
      <div className="speak-up-header">
        <div className="header-content">
          <h1>Speak Up</h1>
          <p>Your safe space for confidential conversations and professional support</p>
        </div>
        <div className="emergency-contact">
          <Shield className="shield-icon" />
          <div>
            <span className="emergency-text">Crisis Support</span>
            <span className="emergency-number">24/7: 1-800-273-8255</span>
          </div>
        </div>
      </div>

      <div className="speak-up-tabs">
        <button 
          className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          <MessageSquare className="tab-icon" />
          AI Chat Support
        </button>
        <button 
          className={`tab ${activeTab === 'counselors' ? 'active' : ''}`}
          onClick={() => setActiveTab('counselors')}
        >
          <User className="tab-icon" />
          Professional Counselors
        </button>
      </div>

      {activeTab === 'chat' && (
        <div className="chat-section">
          <div className="chat-container">
            <div className="chat-header">
              <div className="chat-info">
                <div className="bot-avatar">
                  <Heart className="bot-icon" />
                </div>
                <div>
                  <h3>Cally AI Counselor</h3>
                  <span className="status online">Online • Always here for you</span>
                </div>
              </div>
              <div className="chat-actions">
                <button className="action-btn">
                  <Phone className="icon" />
                </button>
                <button className="action-btn">
                  <Video className="icon" />
                </button>
              </div>
            </div>

            <div className="chat-messages">
              {chatHistory.map((chat) => (
                <div key={chat.id} className={`message ${chat.type}`}>
                  <div className="message-content">
                    <p>{chat.message}</p>
                    <span className="timestamp">{chat.timestamp}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="chat-input">
              <div className="input-container">
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Share what's on your mind... Your conversation is completely confidential."
                  rows="3"
                />
                <div className="input-actions">
                  <button 
                    className={`voice-btn ${isRecording ? 'recording' : ''}`}
                    onClick={toggleRecording}
                  >
                    {isRecording ? <MicOff className="icon" /> : <Mic className="icon" />}
                  </button>
                  <button 
                    className="send-btn"
                    onClick={handleSendMessage}
                    disabled={!message.trim()}
                  >
                    <Send className="icon" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="chat-sidebar">
            <div className="privacy-notice">
              <Shield className="privacy-icon" />
              <h4>Your Privacy Matters</h4>
              <p>All conversations are encrypted and confidential. We never store personal information without your consent.</p>
            </div>

            <div className="quick-topics">
              <h4>Quick Topics</h4>
              <div className="topic-buttons">
                <button className="topic-btn">Anxiety</button>
                <button className="topic-btn">Depression</button>
                <button className="topic-btn">Stress</button>
                <button className="topic-btn">Relationships</button>
                <button className="topic-btn">Work Issues</button>
                <button className="topic-btn">Sleep Problems</button>
              </div>
            </div>

            <div className="resources">
              <h4>Helpful Resources</h4>
              <ul className="resource-list">
                <li><a href="#">Breathing Exercises</a></li>
                <li><a href="#">Mindfulness Techniques</a></li>
                <li><a href="#">Crisis Support</a></li>
                <li><a href="#">Self-Care Tips</a></li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'counselors' && (
        <div className="counselors-section">
          <div className="section-header">
            <h2>Professional Counselors</h2>
            <p>Connect with licensed mental health professionals</p>
          </div>

          <div className="counselors-grid">
            {counselors.map((counselor) => (
              <div key={counselor.id} className="counselor-card">
                <div className="counselor-header">
                  <img 
                    src={counselor.image} 
                    alt={counselor.name}
                    className="counselor-image"
                  />
                  <div className={`availability-indicator ${counselor.available ? 'available' : 'busy'}`}>
                    {counselor.available ? 'Available' : 'Busy'}
                  </div>
                </div>

                <div className="counselor-info">
                  <h3>{counselor.name}</h3>
                  <p className="specialty">{counselor.specialty}</p>
                  
                  <div className="counselor-stats">
                    <div className="stat">
                      <span className="stat-value">★ {counselor.rating}</span>
                      <span className="stat-label">Rating</span>
                    </div>
                    <div className="stat">
                      <span className="stat-value">{counselor.experience}</span>
                      <span className="stat-label">Experience</span>
                    </div>
                  </div>

                  <div className="next-slot">
                    <Calendar className="slot-icon" />
                    <span>Next available: {counselor.nextSlot}</span>
                  </div>
                </div>

                <div className="counselor-actions">
                  <button className="book-btn primary">
                    <Calendar className="icon" />
                    Book Session
                  </button>
                  <button className="book-btn secondary">
                    <MessageSquare className="icon" />
                    Quick Chat
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="booking-info">
            <div className="info-card">
              <Clock className="info-icon" />
              <div>
                <h4>Session Duration</h4>
                <p>Standard sessions are 50 minutes. Emergency consultations available 24/7.</p>
              </div>
            </div>
            <div className="info-card">
              <Shield className="info-icon" />
              <div>
                <h4>Confidentiality</h4>
                <p>All sessions are completely confidential and HIPAA compliant.</p>
              </div>
            </div>
            <div className="info-card">
              <Heart className="info-icon" />
              <div>
                <h4>Specialized Care</h4>
                <p>Our counselors specialize in various areas to provide targeted support.</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SpeakUp;