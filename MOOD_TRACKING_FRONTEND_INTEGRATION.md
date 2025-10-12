# 🎭 Frontend Integration Guide for Mood Tracking Feature

## 📋 Overview
This guide shows how to integrate the mood tracking feature into your frontend application. The feature includes daily mood prompts, suggestion popups, and dashboard integration.

## 🔧 Frontend Implementation Steps

### 1. Dashboard Component Updates

#### A. Add Mood Prompt Check on Dashboard Load

```javascript
// In your main Dashboard component
import React, { useState, useEffect } from 'react';
import MoodPromptModal from './components/MoodPromptModal';
import MoodSuggestionPopup from './components/MoodSuggestionPopup';

const Dashboard = () => {
  const [showMoodPrompt, setShowMoodPrompt] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [moodData, setMoodData] = useState(null);

  useEffect(() => {
    checkMoodPrompt();
    checkMoodSuggestions();
  }, []);

  const checkMoodPrompt = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/mood/check-prompt', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      
      if (data.success && data.show_prompt) {
        setShowMoodPrompt(true);
      }
    } catch (error) {
      console.error('Error checking mood prompt:', error);
    }
  };

  const checkMoodSuggestions = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/mood/dashboard-status', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      
      if (data.success) {
        setMoodData(data.mood);
        if (data.show_suggestions && data.suggestions.length > 0) {
          setSuggestions(data.suggestions);
          // Show suggestions popup after a delay (e.g., 5 seconds)
          setTimeout(() => setShowSuggestions(true), 5000);
        }
      }
    } catch (error) {
      console.error('Error checking mood suggestions:', error);
    }
  };

  const handleMoodSubmit = (moodData) => {
    setShowMoodPrompt(false);
    // Refresh mood data after submission
    checkMoodSuggestions();
  };

  const handleSuggestionClose = () => {
    setShowSuggestions(false);
  };

  return (
    <div className="dashboard">
      {/* Existing dashboard content */}
      <div className="dashboard-header">
        <h1>Welcome to Your Dashboard</h1>
        {moodData && <MoodStatusWidget moodData={moodData} />}
      </div>

      {/* Your existing dashboard components */}
      
      {/* Mood Prompt Modal */}
      {showMoodPrompt && (
        <MoodPromptModal 
          onSubmit={handleMoodSubmit}
          onClose={() => setShowMoodPrompt(false)}
        />
      )}

      {/* Mood Suggestions Popup */}
      {showSuggestions && (
        <MoodSuggestionPopup 
          suggestions={suggestions}
          onClose={handleSuggestionClose}
        />
      )}
    </div>
  );
};

export default Dashboard;
```

### 2. Mood Prompt Modal Component

```javascript
// components/MoodPromptModal.jsx
import React, { useState } from 'react';
import './MoodPromptModal.css';

const MoodPromptModal = ({ onSubmit, onClose }) => {
  const [formData, setFormData] = useState({
    mood_score: 5,
    mood_label: '',
    energy_level: 5,
    stress_level: 5,
    anxiety_level: 5,
    sleep_quality: 5,
    notes: '',
    factors: []
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const moodLabels = {
    1: 'Very Sad', 2: 'Sad', 3: 'Low', 4: 'Okay', 5: 'Neutral',
    6: 'Good', 7: 'Happy', 8: 'Very Happy', 9: 'Excited', 10: 'Euphoric'
  };

  const factorOptions = [
    'work', 'relationships', 'health', 'finances', 'sleep', 
    'exercise', 'weather', 'social', 'family', 'achievement'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/mood/submit', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...formData,
          mood_label: moodLabels[formData.mood_score]
        })
      });

      const data = await response.json();
      
      if (data.success) {
        onSubmit(data.mood_entry);
        // Optionally show suggestions immediately
        if (data.suggestions && data.suggestions.length > 0) {
          showSuggestions(data.suggestions);
        }
      } else {
        alert('Error submitting mood: ' + data.message);
      }
    } catch (error) {
      console.error('Error submitting mood:', error);
      alert('Failed to submit mood data');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleFactorToggle = (factor) => {
    setFormData(prev => ({
      ...prev,
      factors: prev.factors.includes(factor)
        ? prev.factors.filter(f => f !== factor)
        : [...prev.factors, factor]
    }));
  };

  return (
    <div className="mood-modal-overlay">
      <div className="mood-modal">
        <div className="mood-modal-header">
          <h2>How are you feeling today?</h2>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>

        <form onSubmit={handleSubmit} className="mood-form">
          {/* Mood Score */}
          <div className="form-group">
            <label>Overall Mood (1-10)</label>
            <input
              type="range"
              min="1"
              max="10"
              value={formData.mood_score}
              onChange={(e) => setFormData({...formData, mood_score: parseInt(e.target.value)})}
            />
            <div className="mood-display">
              {formData.mood_score}/10 - {moodLabels[formData.mood_score]}
            </div>
          </div>

          {/* Energy Level */}
          <div className="form-group">
            <label>Energy Level (1-10)</label>
            <input
              type="range"
              min="1"
              max="10"
              value={formData.energy_level}
              onChange={(e) => setFormData({...formData, energy_level: parseInt(e.target.value)})}
            />
            <div className="slider-value">{formData.energy_level}/10</div>
          </div>

          {/* Stress Level */}
          <div className="form-group">
            <label>Stress Level (1-10)</label>
            <input
              type="range"
              min="1"
              max="10"
              value={formData.stress_level}
              onChange={(e) => setFormData({...formData, stress_level: parseInt(e.target.value)})}
            />
            <div className="slider-value">{formData.stress_level}/10</div>
          </div>

          {/* Sleep Quality */}
          <div className="form-group">
            <label>Sleep Quality (1-10)</label>
            <input
              type="range"
              min="1"
              max="10"
              value={formData.sleep_quality}
              onChange={(e) => setFormData({...formData, sleep_quality: parseInt(e.target.value)})}
            />
            <div className="slider-value">{formData.sleep_quality}/10</div>
          </div>

          {/* Factors */}
          <div className="form-group">
            <label>What's affecting your mood today?</label>
            <div className="factors-grid">
              {factorOptions.map(factor => (
                <button
                  key={factor}
                  type="button"
                  className={`factor-btn ${formData.factors.includes(factor) ? 'selected' : ''}`}
                  onClick={() => handleFactorToggle(factor)}
                >
                  {factor}
                </button>
              ))}
            </div>
          </div>

          {/* Notes */}
          <div className="form-group">
            <label>Additional Notes (Optional)</label>
            <textarea
              value={formData.notes}
              onChange={(e) => setFormData({...formData, notes: e.target.value})}
              placeholder="Anything specific you'd like to note about today..."
              rows="3"
            />
          </div>

          <div className="form-actions">
            <button type="button" onClick={onClose} className="btn-secondary">
              Skip for today
            </button>
            <button type="submit" disabled={isSubmitting} className="btn-primary">
              {isSubmitting ? 'Submitting...' : 'Submit Mood'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MoodPromptModal;
```

### 3. Mood Suggestion Popup Component

```javascript
// components/MoodSuggestionPopup.jsx
import React, { useState, useEffect } from 'react';
import './MoodSuggestionPopup.css';

const MoodSuggestionPopup = ({ suggestions, onClose }) => {
  const [selectedSuggestion, setSelectedSuggestion] = useState(null);

  useEffect(() => {
    // Log that suggestions were viewed
    logSuggestionAction('viewed');
  }, []);

  const logSuggestionAction = async (action, suggestion = null) => {
    try {
      const token = localStorage.getItem('token');
      await fetch('/api/mood/suggestion-action', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          action,
          type: suggestion?.type,
          title: suggestion?.title
        })
      });
    } catch (error) {
      console.error('Error logging suggestion action:', error);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setSelectedSuggestion(suggestion);
    logSuggestionAction('clicked', suggestion);
  };

  const handleMarkCompleted = (suggestion) => {
    logSuggestionAction('completed', suggestion);
    // Optionally remove the suggestion or show completion feedback
    alert('Great job completing this wellness activity! 🎉');
  };

  return (
    <div className="suggestion-popup-overlay">
      <div className="suggestion-popup">
        <div className="suggestion-header">
          <h3>💡 Wellness Suggestions</h3>
          <p>Based on your mood today, here are some activities that might help:</p>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>

        <div className="suggestions-list">
          {suggestions.map((suggestion, index) => (
            <div key={index} className="suggestion-card">
              <div className="suggestion-icon">{suggestion.icon}</div>
              <div className="suggestion-content">
                <h4>{suggestion.title}</h4>
                <p>{suggestion.description}</p>
                <div className="suggestion-actions">
                  <button 
                    className="btn-try"
                    onClick={() => handleSuggestionClick(suggestion)}
                  >
                    Try This
                  </button>
                  <button 
                    className="btn-completed"
                    onClick={() => handleMarkCompleted(suggestion)}
                  >
                    Mark Done
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="popup-footer">
          <button onClick={onClose} className="btn-dismiss">
            I'll check these later
          </button>
        </div>
      </div>
    </div>
  );
};

export default MoodSuggestionPopup;
```

### 4. Mood Status Widget for Dashboard

```javascript
// components/MoodStatusWidget.jsx
import React, { useState, useEffect } from 'react';
import './MoodStatusWidget.css';

const MoodStatusWidget = ({ moodData }) => {
  const [weeklyChart, setWeeklyChart] = useState([]);

  useEffect(() => {
    fetchWeeklyChart();
  }, []);

  const fetchWeeklyChart = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/mood/weekly-chart', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      
      if (data.success) {
        setWeeklyChart(data.chart_data);
      }
    } catch (error) {
      console.error('Error fetching weekly chart:', error);
    }
  };

  const getMoodColor = (score) => {
    if (score >= 8) return '#4CAF50'; // Green
    if (score >= 6) return '#FFC107'; // Yellow
    if (score >= 4) return '#FF9800'; // Orange
    return '#F44336'; // Red
  };

  const getMoodEmoji = (score) => {
    if (score >= 8) return '😊';
    if (score >= 6) return '🙂';
    if (score >= 4) return '😐';
    return '😔';
  };

  return (
    <div className="mood-widget">
      <div className="mood-current">
        <h3>Today's Mood</h3>
        {moodData ? (
          <div className="mood-display">
            <span className="mood-emoji">{getMoodEmoji(moodData.score)}</span>
            <span className="mood-score" style={{color: getMoodColor(moodData.score)}}>
              {moodData.score}/10
            </span>
            <span className="mood-label">{moodData.label}</span>
          </div>
        ) : (
          <div className="no-mood">
            <span>No mood recorded today</span>
          </div>
        )}
      </div>

      <div className="mood-chart">
        <h4>This Week</h4>
        <div className="chart-container">
          {weeklyChart.map((day, index) => (
            <div key={index} className="chart-bar">
              <div 
                className="bar" 
                style={{
                  height: day.mood ? `${(day.mood / 10) * 100}%` : '10%',
                  backgroundColor: day.mood ? getMoodColor(day.mood) : '#ddd'
                }}
              ></div>
              <span className="day-label">{day.day}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MoodStatusWidget;
```

### 5. CSS Styles

```css
/* MoodPromptModal.css */
.mood-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.mood-modal {
  background: white;
  border-radius: 12px;
  padding: 24px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.mood-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input[type="range"] {
  width: 100%;
  margin-bottom: 5px;
}

.mood-display, .slider-value {
  text-align: center;
  font-weight: 500;
  color: #333;
}

.factors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 8px;
}

.factor-btn {
  padding: 8px 12px;
  border: 2px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.factor-btn.selected {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
}

/* MoodSuggestionPopup.css */
.suggestion-popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.suggestion-popup {
  background: white;
  border-radius: 12px;
  padding: 24px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.suggestion-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 12px;
}

.suggestion-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.suggestion-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.btn-try {
  background: #28a745;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-completed {
  background: #17a2b8;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

/* MoodStatusWidget.css */
.mood-widget {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.mood-display {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.mood-emoji {
  font-size: 32px;
}

.mood-score {
  font-size: 24px;
  font-weight: bold;
}

.chart-container {
  display: flex;
  gap: 8px;
  height: 80px;
  align-items: flex-end;
  margin-top: 12px;
}

.chart-bar {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bar {
  width: 100%;
  border-radius: 4px 4px 0 0;
  transition: height 0.3s ease;
}

.day-label {
  font-size: 12px;
  margin-top: 4px;
  color: #666;
}
```

## 🔄 Usage Flow

1. **User opens dashboard** → Check for mood prompt needed
2. **First daily visit** → Show mood input modal
3. **User submits mood** → Store data and check for suggestions
4. **Low mood/high stress detected** → Show suggestion popup after delay
5. **User interacts with suggestions** → Log interactions
6. **Dashboard updates** → Show current mood status and weekly chart

## 📱 Mobile Considerations

- Make modals responsive with proper viewport handling
- Use touch-friendly button sizes (minimum 44px)
- Consider gesture support for sliders
- Implement proper focus management for accessibility

## 🎯 Key Integration Points

1. **Authentication**: All API calls require JWT token
2. **Error Handling**: Gracefully handle API failures
3. **Loading States**: Show loading indicators during API calls
4. **Accessibility**: Ensure keyboard navigation and screen reader support
5. **Performance**: Use React.memo() for components that don't need frequent updates

This integration will provide a seamless mood tracking experience that helps users monitor their mental health and receive personalized wellness suggestions directly in their dashboard.