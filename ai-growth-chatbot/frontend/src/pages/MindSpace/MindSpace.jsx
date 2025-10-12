import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  Play, 
  Pause, 
  Heart,
  Zap,
  Moon,
  Sun,
  Wind,
  Waves,
  History,
  Star,
  Loader2,
  TrendingUp,
  Clock
} from 'lucide-react';
import MediaPlayer from '../../components/MediaPlayer/MediaPlayer';
import apiService from '../../services/api';
import './MindSpace.css';

const MindSpace = () => {
  const [currentSession, setCurrentSession] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sessions, setSessions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [userProgress, setUserProgress] = useState({
    total_sessions_completed: 0,
    total_minutes_practiced: 0,
    streak_days: 0,
    favorite_category: null
  });
  const [sessionHistory, setSessionHistory] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Icon mapping for categories
  const iconMap = {
    'brain': Brain,
    'heart': Heart,
    'zap': Zap,
    'moon': Moon,
    'sun': Sun,
    'wind': Wind,
    'waves': Waves
  };

  // Load data on component mount
  useEffect(() => {
    loadInitialData();
  }, []);

  // Load sessions when category changes
  useEffect(() => {
    if (categories.length > 0) {
      loadSessions();
    }
  }, [selectedCategory]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      
      // Load categories first
      const categoriesResponse = await apiService.getMindSpaceCategories();
      if (categoriesResponse.success) {
        setCategories(categoriesResponse.categories);
      }

      // Load user progress if authenticated
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const [progressResponse, historyResponse, recommendationsResponse] = await Promise.all([
            apiService.getUserProgress(),
            apiService.getSessionHistory(5),
            apiService.getPersonalizedRecommendations()
          ]);

          if (progressResponse.success) {
            setUserProgress(progressResponse.progress);
          }

          if (historyResponse.success) {
            setSessionHistory(historyResponse.history);
          }

          if (recommendationsResponse.success) {
            setRecommendations(recommendationsResponse.recommendations);
          }
        } catch (authError) {
          console.log('User not authenticated, showing default progress');
        }
      }

      // Load initial sessions
      await loadSessions();
      
    } catch (err) {
      console.error('Error loading initial data:', err);
      setError('Failed to load MindSpace data');
    } finally {
      setLoading(false);
    }
  };

  const loadSessions = async () => {
    try {
      const response = await apiService.getMindSpaceSessions(selectedCategory);
      if (response.success) {
        setSessions(response.sessions);
      }
    } catch (err) {
      console.error('Error loading sessions:', err);
      setError('Failed to load sessions');
    }
  };

  const handlePlayPause = async (session) => {
    if (currentSession?.id === session.id) {
      setIsPlaying(!isPlaying);
    } else {
      setCurrentSession(session);
      setIsPlaying(true);
      
      // Start session tracking if user is authenticated
      const token = localStorage.getItem('token');
      if (token) {
        try {
          await apiService.startMindSpaceSession(session.id);
        } catch (err) {
          console.log('Could not start session tracking:', err);
        }
      }
    }
  };

  const handleProgressUpdate = async (sessionId, progressSeconds) => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        await apiService.updateSessionProgress(sessionId, progressSeconds);
      } catch (err) {
        console.log('Could not update progress:', err);
      }
    }
  };

  const handleSessionComplete = async (sessionId) => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        await apiService.completeSession(sessionId, 5); // Default 5-star rating
        
        // Refresh user progress
        const progressResponse = await apiService.getUserProgress();
        if (progressResponse.success) {
          setUserProgress(progressResponse.progress);
        }
        
        // Refresh session history
        const historyResponse = await apiService.getSessionHistory(5);
        if (historyResponse.success) {
          setSessionHistory(historyResponse.history);
        }
        
      } catch (err) {
        console.log('Could not complete session:', err);
      }
    }
    
    // Stop playback
    setIsPlaying(false);
  };

  const filteredSessions = sessions;

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Beginner': return 'difficulty-beginner';
      case 'Intermediate': return 'difficulty-intermediate';
      case 'Advanced': return 'difficulty-advanced';
      default: return '';
    }
  };

  if (loading) {
    return (
      <div className="mind-space">
        <div className="loading-container">
          <Loader2 className="spinner-icon" size={48} />
          <p>Loading your mindfulness journey...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mind-space">
        <div className="error-container">
          <Brain className="error-icon" size={48} />
          <p>{error}</p>
          <button onClick={loadInitialData} className="retry-btn">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="mind-space">
      <div className="mind-space-header">
        <div className="header-content">
          <h1>Mind Space</h1>
          <p>Guided meditations, focus sessions, and relaxation experiences</p>
        </div>
        <div className="stats">
          <div className="stat-item">
            <TrendingUp className="stat-icon" />
            <span className="stat-value">{userProgress.total_sessions_completed}</span>
            <span className="stat-label">Sessions Completed</span>
          </div>
          <div className="stat-item">
            <Clock className="stat-icon" />
            <span className="stat-value">{userProgress.total_minutes_practiced}</span>
            <span className="stat-label">Minutes Practiced</span>
          </div>
          <div className="stat-item">
            <Star className="stat-icon" />
            <span className="stat-value">{userProgress.streak_days}</span>
            <span className="stat-label">Day Streak</span>
          </div>
        </div>
      </div>

      {/* Personalized Recommendations */}
      {recommendations.length > 0 && (
        <div className="recommendations-section">
          <h2>Recommended for You</h2>
          <div className="recommendations-grid">
            {recommendations.map((session) => (
              <div key={session.id} className="recommendation-card">
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
                  <h4 className="session-title">{session.title}</h4>
                  <p className="session-instructor">by {session.instructor}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="categories">
        {categories.map((category) => {
          const IconComponent = iconMap[category.icon] || Brain;
          return (
            <button
              key={category.id}
              className={`category-btn ${selectedCategory === category.id ? 'active' : ''}`}
              onClick={() => setSelectedCategory(category.id)}
            >
              <IconComponent className="category-icon" />
              <span>{category.name}</span>
            </button>
          );
        })}
      </div>

      {currentSession && (
        <MediaPlayer
          session={currentSession}
          isPlaying={isPlaying}
          onPlayPause={() => setIsPlaying(!isPlaying)}
          onProgressUpdate={handleProgressUpdate}
          onSessionComplete={handleSessionComplete}
        />
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

      {/* Session History */}
      {sessionHistory.length > 0 && localStorage.getItem('token') && (
        <div className="history-section">
          <div className="section-header">
            <h2>Recent Sessions</h2>
            <History className="section-icon" />
          </div>
          <div className="history-list">
            {sessionHistory.map((historyItem) => (
              <div key={historyItem.id} className="history-item">
                <div className="history-info">
                  <h4 className="history-title">{historyItem.session_title}</h4>
                  <p className="history-meta">
                    {historyItem.category} • {historyItem.duration_minutes} min
                    {historyItem.is_completed && <span className="completed-badge">✓ Completed</span>}
                  </p>
                  <span className="history-date">
                    {new Date(historyItem.started_at).toLocaleDateString()}
                  </span>
                </div>
                {historyItem.rating && (
                  <div className="history-rating">
                    ★ {historyItem.rating}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MindSpace;