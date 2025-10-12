#!/usr/bin/env python3
"""
Unit tests for mood tracking feature
"""

import unittest
import json
import datetime
from unittest.mock import patch, MagicMock
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app
from models.mood_model import Mood, MoodSuggestion


class MoodTrackingTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and test data"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Mock JWT token
        self.test_token = 'test_jwt_token'
        self.test_user_id = 'test_user_123'
        
        # Test mood data
        self.valid_mood_data = {
            'mood_score': 7,
            'mood_label': 'happy',
            'energy_level': 8,
            'stress_level': 3,
            'anxiety_level': 2,
            'sleep_quality': 8,
            'notes': 'Feeling great today!',
            'factors': ['work', 'exercise']
        }
        
        self.invalid_mood_data = {
            'mood_score': 15,  # Invalid range
            'energy_level': 8
            # Missing required mood_label
        }

    @patch('controllers.mood_controller.get_jwt_identity')
    @patch('models.mood_model.Mood.create_mood_entry')
    @patch('models.mood_model.Mood.get_today_mood')
    def test_create_mood_entry_successfully(self, mock_get_today_mood, mock_create_mood_entry, mock_get_jwt_identity):
        """Test creating a mood entry successfully"""
        # Setup mocks
        mock_get_jwt_identity.return_value = self.test_user_id
        mock_get_today_mood.return_value = None  # No existing mood today
        mock_create_mood_entry.return_value = {
            '_id': 'mood_entry_id',
            'mood_score': 7,
            'mood_label': 'happy',
            'created_at': datetime.datetime.utcnow()
        }
        
        # Make request
        response = self.client.post('/api/mood/submit',
                                  data=json.dumps(self.valid_mood_data),
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {self.test_token}'})
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Mood submitted successfully')
        self.assertIn('mood_entry', data)
        self.assertIn('suggestions', data)
        
        # Verify mock calls
        mock_create_mood_entry.assert_called_once()
        mock_get_today_mood.assert_called_once_with(self.test_user_id)

    @patch('controllers.mood_controller.get_jwt_identity')
    @patch('models.mood_model.Mood.should_show_mood_prompt')
    def test_check_mood_prompt_needed(self, mock_should_show_mood_prompt, mock_get_jwt_identity):
        """Test checking if mood prompt is needed"""
        # Setup mocks
        mock_get_jwt_identity.return_value = self.test_user_id
        mock_should_show_mood_prompt.return_value = True
        
        # Make request
        response = self.client.get('/api/mood/check-prompt',
                                 headers={'Authorization': f'Bearer {self.test_token}'})
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['show_prompt'])
        
        # Verify mock calls
        mock_should_show_mood_prompt.assert_called_once_with(self.test_user_id)

    @patch('controllers.mood_controller.get_jwt_identity')
    @patch('models.mood_model.Mood.get_today_mood')
    def test_get_today_mood_entry(self, mock_get_today_mood, mock_get_jwt_identity):
        """Test getting today's mood entry"""
        # Setup mocks
        mock_get_jwt_identity.return_value = self.test_user_id
        mock_mood = {
            '_id': 'mood_id',
            'mood_score': 8,
            'mood_label': 'very happy',
            'energy_level': 9,
            'stress_level': 2,
            'created_at': datetime.datetime.utcnow()
        }
        mock_get_today_mood.return_value = mock_mood
        
        # Make request
        response = self.client.get('/api/mood/today',
                                 headers={'Authorization': f'Bearer {self.test_token}'})
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['mood'])
        self.assertEqual(data['mood']['mood_score'], 8)
        self.assertEqual(data['mood']['mood_label'], 'very happy')

    @patch('models.mood_model.MoodSuggestion.get_suggestions_for_mood')
    def test_generate_mood_suggestions(self, mock_get_suggestions):
        """Test generating mood suggestions"""
        # Setup mock
        mock_suggestions = [
            {
                'type': 'activity',
                'title': 'Take a walk',
                'description': 'Fresh air helps',
                'icon': '🚶‍♀️'
            },
            {
                'type': 'mindfulness',
                'title': 'Deep breathing',
                'description': 'Helps reduce stress',
                'icon': '🧘‍♀️'
            }
        ]
        mock_get_suggestions.return_value = mock_suggestions
        
        # Test the suggestion generation function
        suggestions = MoodSuggestion.get_suggestions_for_mood(
            mood_score=3,  # Low mood
            stress_level=8,  # High stress
            energy_level=4   # Low energy
        )
        
        # Assertions
        self.assertIsInstance(suggestions, list)
        self.assertGreaterEqual(len(suggestions), 1)
        for suggestion in suggestions:
            self.assertIn('type', suggestion)
            self.assertIn('title', suggestion)
            self.assertIn('description', suggestion)
            self.assertIn('icon', suggestion)

    @patch('controllers.mood_controller.get_jwt_identity')
    @patch('models.mood_model.Mood.get_today_mood')
    def test_invalid_mood_score_range(self, mock_get_today_mood, mock_get_jwt_identity):
        """Test submitting mood with invalid score range"""
        # Setup mocks
        mock_get_jwt_identity.return_value = self.test_user_id
        mock_get_today_mood.return_value = None
        
        # Make request with invalid data
        response = self.client.post('/api/mood/submit',
                                  data=json.dumps(self.invalid_mood_data),
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {self.test_token}'})
        
        # Assertions
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('Mood score must be between 1 and 10', data['message'])

    @patch('controllers.mood_controller.get_jwt_identity')
    @patch('models.mood_model.Mood.get_today_mood')
    def test_missing_required_fields(self, mock_get_today_mood, mock_get_jwt_identity):
        """Test submitting mood with missing required fields"""
        # Setup mocks
        mock_get_jwt_identity.return_value = self.test_user_id
        mock_get_today_mood.return_value = None
        
        # Make request with missing required field
        incomplete_data = {'mood_score': 5}  # Missing mood_label
        response = self.client.post('/api/mood/submit',
                                  data=json.dumps(incomplete_data),
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {self.test_token}'})
        
        # Assertions
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('Missing required field', data['message'])

    @patch('controllers.mood_controller.get_jwt_identity')
    @patch('models.mood_model.Mood.get_today_mood')
    def test_duplicate_daily_mood_entry(self, mock_get_today_mood, mock_get_jwt_identity):
        """Test attempting to submit duplicate mood entry for same day"""
        # Setup mocks
        mock_get_jwt_identity.return_value = self.test_user_id
        mock_get_today_mood.return_value = {  # Existing mood entry
            '_id': 'existing_mood_id',
            'mood_score': 6,
            'mood_label': 'good',
            'created_at': datetime.datetime.utcnow()
        }
        
        # Make request
        response = self.client.post('/api/mood/submit',
                                  data=json.dumps(self.valid_mood_data),
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {self.test_token}'})
        
        # Assertions
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('already submitted your mood for today', data['message'])

    @patch('controllers.mood_controller.get_jwt_identity')
    @patch('models.mood_model.Mood.should_show_mood_prompt')
    def test_mood_prompt_after_submission(self, mock_should_show_mood_prompt, mock_get_jwt_identity):
        """Test that mood prompt is not shown after submission"""
        # Setup mocks
        mock_get_jwt_identity.return_value = self.test_user_id
        mock_should_show_mood_prompt.return_value = False  # Already submitted today
        
        # Make request
        response = self.client.get('/api/mood/check-prompt',
                                 headers={'Authorization': f'Bearer {self.test_token}'})
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertFalse(data['show_prompt'])
        
        # Verify mock calls
        mock_should_show_mood_prompt.assert_called_once_with(self.test_user_id)

    @patch('controllers.mood_controller.get_jwt_identity')
    @patch('models.mood_model.Mood.get_mood_history')
    def test_get_mood_history(self, mock_get_mood_history, mock_get_jwt_identity):
        """Test getting mood history"""
        # Setup mocks
        mock_get_jwt_identity.return_value = self.test_user_id
        mock_history = [
            {
                '_id': 'mood1',
                'mood_score': 8,
                'mood_label': 'happy',
                'created_at': datetime.datetime.utcnow()
            },
            {
                '_id': 'mood2',
                'mood_score': 6,
                'mood_label': 'okay',
                'created_at': datetime.datetime.utcnow() - datetime.timedelta(days=1)
            }
        ]
        mock_get_mood_history.return_value = mock_history
        
        # Make request
        response = self.client.get('/api/mood/history?days=30',
                                 headers={'Authorization': f'Bearer {self.test_token}'})
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['moods']), 2)
        self.assertEqual(data['total_count'], 2)

    @patch('controllers.mood_controller.get_jwt_identity')
    @patch('models.mood_model.Mood.get_mood_analytics')
    def test_get_mood_analytics(self, mock_get_mood_analytics, mock_get_jwt_identity):
        """Test getting mood analytics"""
        # Setup mocks
        mock_get_jwt_identity.return_value = self.test_user_id
        mock_analytics = {
            'average_mood': 7.5,
            'average_energy': 8.0,
            'average_stress': 3.5,
            'mood_trend': 'improving',
            'total_entries': 5
        }
        mock_get_mood_analytics.return_value = mock_analytics
        
        # Make request
        response = self.client.get('/api/mood/analytics',
                                 headers={'Authorization': f'Bearer {self.test_token}'})
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['analytics']['average_mood'], 7.5)
        self.assertEqual(data['analytics']['mood_trend'], 'improving')

    @patch('controllers.mood_controller.get_jwt_identity')
    @patch('models.mood_model.MoodSuggestion.create_suggestion_log')
    def test_log_suggestion_action(self, mock_create_suggestion_log, mock_get_jwt_identity):
        """Test logging suggestion actions"""
        # Setup mocks
        mock_get_jwt_identity.return_value = self.test_user_id
        mock_create_suggestion_log.return_value = 'log_id_123'
        
        # Test data
        action_data = {
            'type': 'activity',
            'title': 'Take a walk',
            'action': 'completed'
        }
        
        # Make request
        response = self.client.post('/api/mood/suggestion-action',
                                  data=json.dumps(action_data),
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {self.test_token}'})
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Action logged successfully')
        
        # Verify mock calls
        mock_create_suggestion_log.assert_called_once()

    @patch('controllers.mood_controller.get_jwt_identity')
    @patch('models.mood_model.Mood.get_weekly_mood_data')
    def test_get_weekly_mood_chart(self, mock_get_weekly_mood_data, mock_get_jwt_identity):
        """Test getting weekly mood chart data"""
        # Setup mocks
        mock_get_jwt_identity.return_value = self.test_user_id
        mock_chart_data = [
            {'day': 'Mon', 'mood': 7, 'energy': 8, 'stress': 3, 'date': '2023-10-01'},
            {'day': 'Tue', 'mood': 8, 'energy': 9, 'stress': 2, 'date': '2023-10-02'},
            {'day': 'Wed', 'mood': 6, 'energy': 7, 'stress': 4, 'date': '2023-10-03'},
            {'day': 'Thu', 'mood': None, 'energy': None, 'stress': None, 'date': '2023-10-04'},
            {'day': 'Fri', 'mood': 9, 'energy': 10, 'stress': 1, 'date': '2023-10-05'},
            {'day': 'Sat', 'mood': 8, 'energy': 8, 'stress': 2, 'date': '2023-10-06'},
            {'day': 'Sun', 'mood': 7, 'energy': 7, 'stress': 3, 'date': '2023-10-07'}
        ]
        mock_get_weekly_mood_data.return_value = mock_chart_data
        
        # Make request
        response = self.client.get('/api/mood/weekly-chart',
                                 headers={'Authorization': f'Bearer {self.test_token}'})
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['chart_data']), 7)
        
        # Verify some specific data points
        monday_data = data['chart_data'][0]
        self.assertEqual(monday_data['day'], 'Mon')
        self.assertEqual(monday_data['mood'], 7)
        
        # Check that Thursday has no data
        thursday_data = data['chart_data'][3]
        self.assertEqual(thursday_data['day'], 'Thu')
        self.assertIsNone(thursday_data['mood'])


class MoodModelTestCase(unittest.TestCase):
    """Test cases for mood model functions"""
    
    def test_suggestion_generation_low_mood(self):
        """Test that appropriate suggestions are generated for low mood"""
        suggestions = MoodSuggestion.get_suggestions_for_mood(
            mood_score=3,  # Low mood
            stress_level=5,
            energy_level=5
        )
        
        # Should include suggestions for low mood
        suggestion_titles = [s['title'] for s in suggestions]
        self.assertTrue(any('walk' in title.lower() for title in suggestion_titles))
        self.assertTrue(any('breathing' in title.lower() for title in suggestion_titles))

    def test_suggestion_generation_high_stress(self):
        """Test that appropriate suggestions are generated for high stress"""
        suggestions = MoodSuggestion.get_suggestions_for_mood(
            mood_score=5,
            stress_level=8,  # High stress
            energy_level=5
        )
        
        # Should include suggestions for high stress
        suggestion_titles = [s['title'] for s in suggestions]
        self.assertTrue(any('relax' in title.lower() for title in suggestion_titles))

    def test_suggestion_generation_low_energy(self):
        """Test that appropriate suggestions are generated for low energy"""
        suggestions = MoodSuggestion.get_suggestions_for_mood(
            mood_score=5,
            stress_level=5,
            energy_level=3  # Low energy
        )
        
        # Should include suggestions for low energy
        suggestion_titles = [s['title'] for s in suggestions]
        self.assertTrue(any('hydrat' in title.lower() for title in suggestion_titles))

    def test_suggestion_generation_good_mood(self):
        """Test that appropriate suggestions are generated for good mood"""
        suggestions = MoodSuggestion.get_suggestions_for_mood(
            mood_score=8,  # Good mood
            stress_level=2,
            energy_level=8
        )
        
        # Should include positive reinforcement suggestions
        suggestion_titles = [s['title'] for s in suggestions]
        self.assertTrue(any('grateful' in title.lower() for title in suggestion_titles))


if __name__ == '__main__':
    unittest.main(verbosity=2)