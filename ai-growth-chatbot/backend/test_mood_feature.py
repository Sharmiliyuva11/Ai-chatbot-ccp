#!/usr/bin/env python3
"""
Test script for the mood tracking feature
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.mood_model import Mood, MoodSuggestion
import datetime

def test_mood_feature():
    """Test the mood tracking functionality"""
    print("🧪 Testing Mood Tracking Feature")
    print("=" * 50)
    
    # Test data
    test_user_id = "test_user_123"
    
    print("1. Testing mood prompt check...")
    should_prompt = Mood.should_show_mood_prompt(test_user_id)
    print(f"   Should show mood prompt: {should_prompt}")
    
    print("\n2. Creating test mood entry...")
    test_mood_data = {
        'mood_score': 3,  # Low mood
        'mood_label': 'sad',
        'energy_level': 4,
        'stress_level': 8,  # High stress
        'anxiety_level': 6,
        'sleep_quality': 5,
        'notes': 'Feeling stressed about work deadlines',
        'factors': ['work', 'deadlines', 'sleep']
    }
    
    mood_entry = Mood.create_mood_entry(test_user_id, test_mood_data)
    print(f"   Created mood entry: {mood_entry['_id']}")
    print(f"   Mood score: {mood_entry['mood_score']}")
    print(f"   Created at: {mood_entry['created_at']}")
    
    print("\n3. Testing mood prompt check after entry...")
    should_prompt_after = Mood.should_show_mood_prompt(test_user_id)
    print(f"   Should show mood prompt: {should_prompt_after}")
    
    print("\n4. Getting today's mood...")
    today_mood = Mood.get_today_mood(test_user_id)
    if today_mood:
        print(f"   Today's mood score: {today_mood['mood_score']}")
        print(f"   Today's mood label: {today_mood['mood_label']}")
    
    print("\n5. Testing mood analytics...")
    analytics = Mood.get_mood_analytics(test_user_id, days=7)
    print(f"   Average mood: {analytics['average_mood']}")
    print(f"   Average stress: {analytics['average_stress']}")
    print(f"   Mood trend: {analytics['mood_trend']}")
    print(f"   Total entries: {analytics['total_entries']}")
    
    print("\n6. Testing mood suggestions...")
    suggestions = MoodSuggestion.get_suggestions_for_mood(
        mood_score=3,  # Low mood
        stress_level=8,  # High stress
        energy_level=4   # Low energy
    )
    print(f"   Generated {len(suggestions)} suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"      {i}. {suggestion['icon']} {suggestion['title']}")
        print(f"         {suggestion['description']}")
    
    print("\n7. Testing weekly mood chart data...")
    weekly_data = Mood.get_weekly_mood_data(test_user_id)
    print(f"   Weekly chart data points: {len(weekly_data)}")
    for day_data in weekly_data:
        mood_str = str(day_data['mood']) if day_data['mood'] is not None else 'No data'
        print(f"      {day_data['day']}: Mood={mood_str}")
    
    print("\n8. Testing suggestion logging...")
    test_suggestion = {
        'type': 'activity',
        'title': 'Take a 10-minute walk outside',
        'action': 'clicked'
    }
    log_id = MoodSuggestion.create_suggestion_log(test_user_id, test_suggestion)
    print(f"   Logged suggestion interaction: {log_id}")
    
    print("\n✅ Mood tracking feature test completed!")
    print("\n📋 API Endpoints Available:")
    print("   GET  /api/mood/check-prompt       - Check if user needs mood prompt")
    print("   POST /api/mood/submit             - Submit daily mood data")
    print("   GET  /api/mood/today              - Get today's mood entry")
    print("   GET  /api/mood/history?days=30    - Get mood history")
    print("   GET  /api/mood/analytics?days=7   - Get mood analytics")
    print("   GET  /api/mood/weekly-chart       - Get weekly mood chart data")
    print("   POST /api/mood/suggestions        - Get personalized suggestions")
    print("   POST /api/mood/suggestion-action  - Log suggestion interactions")
    print("   GET  /api/mood/dashboard-status   - Get dashboard mood status & suggestions")
    
    print("\n📊 Updated Analytics Endpoints:")
    print("   GET  /api/analytics/dashboard-stats - Now includes real mood data")
    print("   GET  /api/analytics/mood-data       - Now includes real weekly mood charts")
    
    return True

if __name__ == "__main__":
    try:
        test_mood_feature()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()