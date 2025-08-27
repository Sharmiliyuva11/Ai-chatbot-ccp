import React, { useRef, useState } from 'react';
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
  Heart,
  Paperclip
} from 'lucide-react';
import api from '../../services/api';
import './SpeakUp.css';

const SpeakUp = () => {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [activeTab, setActiveTab] = useState('chat');
  const [isSending, setIsSending] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);
  // Voice recording refs
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const streamRef = useRef(null);

  // Chat history state (initialize with welcome message)
  const [chatHistory, setChatHistory] = useState([
    {
      id: 1,
      type: 'bot',
      message:
        "Hello! I'm here to listen and support you. How are you feeling today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);

  const getTimestamp = () =>
    new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const handleSendMessage = async () => {
    const text = message.trim();
    if (!text || isSending) return;

    // Optimistically add user message
    const userMsg = {
      id: Date.now(),
      type: 'user',
      message: text,
      timestamp: getTimestamp()
    };
    setChatHistory((prev) => [...prev, userMsg]);
    setMessage('');

    try {
      setIsSending(true);
      const res = await api.sendMessage(text);
      const botText = res?.response || res?.message || 'Sorry, I could not generate a response right now.';
      const botMsg = {
        id: Date.now() + 1,
        type: 'bot',
        message: botText,
        timestamp: getTimestamp()
      };
      setChatHistory((prev) => [...prev, botMsg]);
    } catch (err) {
      const errMsg = {
        id: Date.now() + 2,
        type: 'bot',
        message: `Sorry, I ran into an error: ${err.message}`,
        timestamp: getTimestamp()
      };
      setChatHistory((prev) => [...prev, errMsg]);
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleRecording = async () => {
    try {
      if (!isRecording) {
        // Start recording
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        streamRef.current = stream;
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;
        audioChunksRef.current = [];

        mediaRecorder.ondataavailable = (e) => {
          if (e.data && e.data.size > 0) audioChunksRef.current.push(e.data);
        };

        mediaRecorder.onstop = async () => {
          // Build a Blob (webm) and send it to grammar endpoint
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          const file = new File([audioBlob], `voice-${Date.now()}.webm`, { type: 'audio/webm' });

          setChatHistory((prev) => [
            ...prev,
            {
              id: Date.now() + 7,
              type: 'user',
              message: `[Voice message recorded: ${file.name}]`,
              timestamp: getTimestamp()
            }
          ]);

          try {
            const res = await api.evaluateGrammar(file);
            if (res?.success) {
              const score = res.grammar_score ?? 'N/A';
              setChatHistory((prev) => [
                ...prev,
                {
                  id: Date.now() + 8,
                  type: 'bot',
                  message: `Grammar analysis score: ${score}. Issues: ${res.issues_found}.`,
                  timestamp: getTimestamp()
                }
              ]);
            } else {
              setChatHistory((prev) => [
                ...prev,
                {
                  id: Date.now() + 9,
                  type: 'bot',
                  message: `Grammar check failed: ${res?.message || res?.error || 'Unknown error'}`,
                  timestamp: getTimestamp()
                }
              ]);
            }
          } catch (err) {
            setChatHistory((prev) => [
              ...prev,
              {
                id: Date.now() + 10,
                type: 'bot',
                message: `Grammar check error: ${err.message}`,
                timestamp: getTimestamp()
              }
            ]);
          }

          // Cleanup stream
          streamRef.current?.getTracks().forEach((t) => t.stop());
          streamRef.current = null;
        };

        mediaRecorder.start();
        setIsRecording(true);
      } else {
        // Stop recording
        mediaRecorderRef.current?.stop();
        setIsRecording(false);
      }
    } catch (err) {
      setIsRecording(false);
      setChatHistory((prev) => [
        ...prev,
        {
          id: Date.now() + 11,
          type: 'bot',
          message: `Microphone error: ${err.message}. Please allow mic permissions.`,
          timestamp: getTimestamp()
        }
      ]);
    }
  };

  const handleFileButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setSelectedFile(file);

    // Show a small message in chat to confirm file selection
    setChatHistory((prev) => [
      ...prev,
      {
        id: Date.now() + 3,
        type: 'user',
        message: `[Selected file: ${file.name}]`,
        timestamp: getTimestamp()
      }
    ]);

    try {
      const res = await api.uploadFile(file);
      if (res?.success) {
        setChatHistory((prev) => [
          ...prev,
          {
            id: Date.now() + 4,
            type: 'bot',
            message: `File “${res.filename}” uploaded successfully.`,
            timestamp: getTimestamp()
          }
        ]);
      } else {
        setChatHistory((prev) => [
          ...prev,
          {
            id: Date.now() + 5,
            type: 'bot',
            message: `Upload failed: ${res?.message || 'Unknown error'}`,
            timestamp: getTimestamp()
          }
        ]);
      }
    } catch (err) {
      setChatHistory((prev) => [
        ...prev,
        {
          id: Date.now() + 6,
          type: 'bot',
          message: `Upload error: ${err.message}`,
          timestamp: getTimestamp()
        }
      ]);
    }
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
                  <h3>Coby AI Counselor</h3>
                  <span className="status online">Online • Always here for you</span>
                </div>
              </div>
              <div className="chat-actions">
                <button className="action-btn" title="Voice call (coming soon)">
                  <Phone className="icon" />
                </button>
                <button className="action-btn" title="Video call (coming soon)">
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
                  onKeyDown={handleKeyDown}
                  placeholder="Share what's on your mind... Your conversation is completely confidential."
                  rows="3"
                />
                <div className="input-actions">
                  {/* File upload button */}
                  <button
                    className="voice-btn"
                    onClick={handleFileButtonClick}
                    title="Upload a file"
                  >
                    <Paperclip className="icon" />
                  </button>
                  <input
                    type="file"
                    ref={fileInputRef}
                    style={{ display: 'none' }}
                    onChange={handleFileChange}
                  />

                  {/* Voice toggle button */}
                  <button
                    className={`voice-btn ${isRecording ? 'recording' : ''}`}
                    onClick={toggleRecording}
                    title={isRecording ? 'Stop recording' : 'Start voice message'}
                  >
                    {isRecording ? <MicOff className="icon" /> : <Mic className="icon" />}
                  </button>

                  {/* Send button */}
                  <button
                    className="send-btn"
                    onClick={handleSendMessage}
                    disabled={!message.trim() || isSending}
                    title="Send"
                  >
                    <Send className="icon" />
                  </button>
                </div>
              </div>
              {/* Show selected file name below input */}
              {selectedFile && (
                <div style={{ marginTop: '0.5rem', fontSize: '0.85rem', color: '#334155' }}>
                  Selected file: {selectedFile.name}
                </div>
              )}
            </div>
          </div>

          <div className="chat-sidebar">
            <div className="privacy-notice">
              <Shield className="privacy-icon" />
              <h4>Your Privacy Matters</h4>
              <p>
                All conversations are encrypted and confidential. We never store personal
                information without your consent.
              </p>
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
            {[
              {
                id: 1,
                name: 'Dr. Sarah Johnson',
                specialty: 'Anxiety & Depression',
                rating: 4.9,
                experience: '8 years',
                image:
                  'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=100&h=100&fit=crop&crop=face',
                available: true,
                nextSlot: 'Today 3:00 PM'
              },
              {
                id: 2,
                name: 'Dr. Michael Chen',
                specialty: 'Stress Management',
                rating: 4.8,
                experience: '12 years',
                image:
                  'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=100&h=100&fit=crop&crop=face',
                available: false,
                nextSlot: 'Tomorrow 10:00 AM'
              },
              {
                id: 3,
                name: 'Dr. Emily Rodriguez',
                specialty: 'Relationship Counseling',
                rating: 4.9,
                experience: '10 years',
                image:
                  'https://images.unsplash.com/photo-1594824388853-d0c2b8e8e8e8?w=100&h=100&fit=crop&crop=face',
                available: true,
                nextSlot: 'Today 4:30 PM'
              }
            ].map((counselor) => (
              <div key={counselor.id} className="counselor-card">
                <div className="counselor-header">
                  <img
                    src={counselor.image}
                    alt={counselor.name}
                    className="counselor-image"
                  />
                  <div
                    className={`availability-indicator ${counselor.available ? 'available' : 'busy'}`}
                  >
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