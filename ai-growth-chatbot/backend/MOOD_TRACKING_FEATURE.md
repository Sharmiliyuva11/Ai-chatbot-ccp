# 🎭 Mood Tracking Feature

A comprehensive mood tracking and mental health monitoring system that prompts users once daily and provides personalized suggestions based on their mental state.

## 📋 Features

### 🔍 **Daily Mood Prompt**
- Shows mood prompt only once per day when user opens their account
- Prevents multiple prompts on the same day
- Tracks user's mental health consistently over time

### 📊 **Mood Data Collection**
- **Mood Score**: 1-10 scale rating
- **Mood Label**: Descriptive emotion (happy, sad, anxious, etc.)
- **Energy Level**: 1-10 energy rating
- **Stress Level**: 1-10 stress rating
- **Anxiety Level**: 1-10 anxiety rating
- **Sleep Quality**: 1-10 sleep quality rating
- **Notes**: Optional text notes
- **Contributing Factors**: Tags like 'work', 'relationships', 'health'

### 🎯 **Intelligent Suggestions System**
- Analyzes mood, stress, and energy levels
- Provides personalized recommendations for mental wellness
- Different suggestions for different mental states:
  - **Low Mood**: Walking, breathing exercises, social connection
  - **High Stress**: Relaxation techniques, journaling, music
  - **Low Energy**: Hydration, stretching, power naps
  - **Good Mood**: Gratitude exercises, sharing positivity

### 📈 **Analytics & Insights**
- Weekly mood trends and charts
- Average mood, stress, and energy calculations
- Mood trend analysis (improving/declining/stable)
- Historical mood tracking (up to 365 days)

### 🚨 **Dashboard Integration**
- Real-time mood status on dashboard
- Popup suggestions for users with low mood or high stress
- Visual mood indicators and trends
- Integration with existing analytics

## 🛠️ Technical Implementation

### Database Collections
- **`moods`**: Stores daily mood entries
- **`mood_suggestions`**: Logs user interactions with suggestions

### API Endpoints

#### Core Mood Tracking
- `GET /api/mood/check-prompt` - Check if user needs daily mood prompt
- `POST /api/mood/submit` - Submit daily mood data
- `GET /api/mood/today` - Get today's mood entry
- `GET /api/mood/history?days=30` - Get mood history
- `GET /api/mood/analytics?days=7` - Get mood analytics

#### Charts & Visualizations
- `GET /api/mood/weekly-chart` - Get weekly mood chart data

#### Suggestions System
- `POST /api/mood/suggestions` - Get personalized suggestions
- `POST /api/mood/suggestion-action` - Log suggestion interactions

#### Dashboard Integration
- `GET /api/mood/dashboard-status` - Get mood status for dashboard

#### Updated Analytics
- `GET /api/analytics/dashboard-stats` - Now includes real mood data
- `GET /api/analytics/mood-data` - Real weekly mood charts

## 📝 Usage Examples

### 1. Check if User Needs Mood Prompt
```javascript
const response = await fetch('/api/mood/check-prompt', {
    headers: { 'Authorization': `Bearer ${token}` }
});
const data = await response.json();
if (data.show_prompt) {
    // Show mood input form
}
```

### 2. Submit Daily Mood
```javascript
const moodData = {
    mood_score: 7,
    mood_label: 'happy',
    energy_level: 8,
    stress_level: 3,
    anxiety_level: 2,
    sleep_quality: 8,
    notes: 'Had a great day at work!',
    factors: ['work', 'achievement']
};

const response = await fetch('/api/mood/submit', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(moodData)
});
```

### 3. Get Dashboard Status with Suggestions
```javascript
const response = await fetch('/api/mood/dashboard-status', {
    headers: { 'Authorization': `Bearer ${token}` }
});
const data = await response.json();

if (data.show_suggestions) {
    // Display popup with suggestions
    showSuggestionPopup(data.suggestions);
}
```

### 4. Get Weekly Mood Chart
```javascript
const response = await fetch('/api/mood/weekly-chart', {
    headers: { 'Authorization': `Bearer ${token}` }
});
const data = await response.json();
// Use data.chart_data for mood visualization
```

## 🎨 Frontend Integration Guide

### Dashboard Changes Needed

1. **Daily Mood Prompt**
   ```javascript
   // On dashboard load
   const checkMoodPrompt = async () => {
       const response = await fetch('/api/mood/check-prompt');
       const data = await response.json();
       if (data.show_prompt) {
           showMoodPromptModal();
       }
   };
   ```

2. **Suggestion Popup**
   ```javascript
   // Check for suggestions to show
   const checkSuggestions = async () => {
       const response = await fetch('/api/mood/dashboard-status');
       const data = await response.json();
       if (data.show_suggestions) {
           showSuggestionPopup(data.suggestions);
       }
   };
   ```

3. **Mood Widget/Card**
   ```javascript
   // Display current mood status
   const displayMoodWidget = (moodData) => {
       return (
           <div className="mood-widget">
               <h3>Today's Mood</h3>
               <div className="mood-score">{moodData.mood?.score}/10</div>
               <div className="mood-label">{moodData.mood?.label}</div>
               <div className="mood-trend">{moodData.mood_trend}</div>
           </div>
       );
   };
   ```

### Required UI Components

1. **Mood Input Modal** - For daily mood submission
2. **Suggestion Popup** - For displaying wellness suggestions
3. **Mood Chart Widget** - For displaying weekly trends
4. **Mood Status Indicator** - For dashboard display

## 🔄 Workflow

1. **User opens dashboard** → Check if mood prompt needed
2. **First visit of day** → Show mood input modal
3. **User submits mood** → Store in database + generate suggestions
4. **Low mood/high stress detected** → Show suggestion popup
5. **User interacts with suggestions** → Log interactions
6. **Analytics update** → Real-time mood data in dashboard
7. **Weekly/monthly views** → Historical mood trends

## 🧪 Testing

Run the test script to verify implementation:
```bash
python test_mood_feature.py
```

## 🚀 Deployment Notes

1. **Database**: MongoDB collections will be created automatically
2. **Dependencies**: No additional Python packages required
3. **Environment**: Works with existing MongoDB setup
4. **Backward Compatibility**: Maintains existing analytics endpoints

## 🎯 Benefits

- **Mental Health Awareness**: Daily mood tracking increases self-awareness
- **Early Intervention**: Identifies concerning mood patterns early
- **Personalized Support**: Tailored suggestions based on individual needs
- **Data-Driven Insights**: Analytics help users understand mood patterns
- **Non-Intrusive**: Only prompts once per day, respects user privacy
- **Actionable Recommendations**: Practical suggestions users can implement immediately

## 🔮 Future Enhancements

- Integration with calendar for correlating events with mood
- Machine learning for better suggestion personalization
- Mood pattern alerts for concerning trends
- Integration with wearable devices for additional health metrics
- Gamification with mood streaks and achievements
- Mood sharing with trusted contacts (opt-in)