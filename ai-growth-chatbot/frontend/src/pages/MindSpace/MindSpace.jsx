import React, { useState } from 'react';
import { 
  Brain, 
  Play, 
  Pause, 
  SkipForward, 
  Volume2, 
  Heart,
  Zap,
  Moon,
  Sun,
  Wind,
  Waves
} from 'lucide-react';
import './MindSpace.css';

const MindSpace = () => {
  const [currentSession, setCurrentSession] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [selectedCategory, setSelectedCategory] = useState('all');

  const categories = [
    { id: 'all', name: 'All', icon: Brain },
    { id: 'meditation', name: 'Meditation', icon: Heart },
    { id: 'focus', name: 'Focus', icon: Zap },
    { id: 'sleep', name: 'Sleep', icon: Moon },
    { id: 'energy', name: 'Energy', icon: Sun },
    { id: 'nature', name: 'Nature', icon: Wind }
  ];

  const sessions = [
    {
      id: 1,
      title: 'Morning Mindfulness',
      description: 'Start your day with clarity and intention through guided mindfulness practice.',
      duration: '10 min',
      category: 'meditation',
      difficulty: 'Beginner',
      instructor: 'Sarah Chen',
      image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop',
      audio: '/audio/morning-mindfulness.mp3',
      plays: 1250,
      rating: 4.8
    },
    {
      id: 2,
      title: 'Deep Focus Flow',
      description: 'Enhance concentration and productivity with binaural beats and ambient sounds.',
      duration: '25 min',
      category: 'focus',
      difficulty: 'Intermediate',
      instructor: 'Michael Torres',
      image: 'https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=300&h=200&fit=crop',
      audio: '/audio/deep-focus.mp3',
      plays: 890,
      rating: 4.9
    },
    {
      id: 3,
      title: 'Peaceful Sleep Journey',
      description: 'Drift into restful sleep with calming narration and gentle soundscapes.',
      duration: '30 min',
      category: 'sleep',
      difficulty: 'Beginner',
      instructor: 'Emma Wilson',
      image: 'https://images.unsplash.com/photo-1517147177326-b37599372b73?w=300&h=200&fit=crop',
      audio: '/audio/sleep-journey.mp3',
      plays: 2100,
      rating: 4.7
    },
    {
      id: 4,
      title: 'Energy Boost Meditation',
      description: 'Revitalize your mind and body with energizing breathing techniques.',
      duration: '15 min',
      category: 'energy',
      difficulty: 'Intermediate',
      instructor: 'David Kim',
      image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop',
      audio: '/audio/energy-boost.mp3',
      plays: 675,
      rating: 4.6
    },
    {
      id: 5,
      title: 'Forest Sounds Relaxation',
      description: 'Immerse yourself in the tranquil sounds of nature for deep relaxation.',
      duration: '45 min',
      category: 'nature',
      difficulty: 'Beginner',
      instructor: 'Nature Sounds',
      image: 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=300&h=200&fit=crop',
      audio: '/audio/forest-sounds.mp3',
      plays: 1800,
      rating: 4.9
    },
    {
      id: 6,
      title: 'Ocean Waves Meditation',
      description: 'Let the rhythmic sounds of ocean waves guide you to inner peace.',
      duration: '20 min',
      category: 'nature',
      difficulty: 'Beginner',
      instructor: 'Ocean Sounds',
      image: 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=300&h=200&fit=crop',
      audio: '/audio/ocean-waves.mp3',
      plays: 1450,
      rating: 4.8
    }
  ];

  const filteredSessions = selectedCategory === 'all' 
    ? sessions 
    : sessions.filter(session => session.category === selectedCategory);

  const handlePlayPause = (session) => {
    if (currentSession?.id === session.id) {
      setIsPlaying(!isPlaying);
    } else {
      setCurrentSession(session);
      setIsPlaying(true);
      setCurrentTime(0);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Beginner': return 'difficulty-beginner';
      case 'Intermediate': return 'difficulty-intermediate';
      case 'Advanced': return 'difficulty-advanced';
      default: return '';
    }
  };

  return (
    <div className="mind-space">
      <div className="mind-space-header">
        <div className="header-content">
          <h1>Mind Space</h1>
          <p>Guided meditations, focus sessions, and relaxation experiences</p>
        </div>
        <div className="stats">
          <div className="stat-item">
            <span className="stat-value">24</span>
            <span className="stat-label">Sessions Completed</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">180</span>
            <span className="stat-label">Minutes Practiced</span>
          </div>
        </div>
      </div>

      <div className="categories">
        {categories.map((category) => (
          <button
            key={category.id}
            className={`category-btn ${selectedCategory === category.id ? 'active' : ''}`}
            onClick={() => setSelectedCategory(category.id)}
          >
            <category.icon className="category-icon" />
            <span>{category.name}</span>
          </button>
        ))}
      </div>

      {currentSession && (
        <div className="current-player">
          <div className="player-content">
            <img 
              src={currentSession.image} 
              alt={currentSession.title}
              className="player-image"
            />
            <div className="player-info">
              <h3>{currentSession.title}</h3>
              <p>by {currentSession.instructor}</p>
            </div>
          </div>
          <div className="player-controls">
            <button className="control-btn">
              <SkipForward className="icon" style={{ transform: 'rotate(180deg)' }} />
            </button>
            <button 
              className="play-pause-btn"
              onClick={() => setIsPlaying(!isPlaying)}
            >
              {isPlaying ? <Pause className="icon" /> : <Play className="icon" />}
            </button>
            <button className="control-btn">
              <SkipForward className="icon" />
            </button>
          </div>
          <div className="player-progress">
            <span className="time">{formatTime(currentTime)}</span>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: '35%' }}
              ></div>
            </div>
            <span className="time">{currentSession.duration}</span>
          </div>
          <div className="volume-control">
            <Volume2 className="volume-icon" />
            <div className="volume-bar">
              <div className="volume-fill" style={{ width: '70%' }}></div>
            </div>
          </div>
        </div>
      )}

      <div className="sessions-grid">
        {filteredSessions.map((session) => (
          <div key={session.id} className="session-card">
            <div className="session-image">
              <img src={session.image} alt={session.title} />
              <div className="session-overlay">
                <button 
                  className="play-btn"
                  onClick={() => handlePlayPause(session)}
                >
                  {currentSession?.id === session.id && isPlaying ? 
                    <Pause className="icon" /> : 
                    <Play className="icon" />
                  }
                </button>
              </div>
              <div className="session-duration">{session.duration}</div>
            </div>
            
            <div className="session-content">
              <div className="session-header">
                <h3 className="session-title">{session.title}</h3>
                <div className={`difficulty-badge ${getDifficultyColor(session.difficulty)}`}>
                  {session.difficulty}
                </div>
              </div>
              
              <p className="session-description">{session.description}</p>
              
              <div className="session-meta">
                <span className="instructor">by {session.instructor}</span>
                <div className="session-stats">
                  <span className="plays">{session.plays.toLocaleString()} plays</span>
                  <div className="rating">
                    <span className="rating-value">★ {session.rating}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredSessions.length === 0 && (
        <div className="empty-state">
          <Brain className="empty-icon" />
          <h3>No sessions found</h3>
          <p>Try selecting a different category or check back later for new content.</p>
        </div>
      )}
    </div>
  );
};

export default MindSpace;