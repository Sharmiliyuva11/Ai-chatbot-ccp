import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.mindspace_controller import mindspace_bp
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token


class TestMindspaceController(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        self.app.config['JWT_SECRET_KEY'] = 'jwt-test-secret'
        self.app.config['TESTING'] = True
        
        # Initialize JWT
        self.jwt = JWTManager(self.app)
        
        # Register blueprint
        self.app.register_blueprint(mindspace_bp)
        
        # Create test client
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create test access token
        with self.app.test_request_context():
            self.access_token = create_access_token(identity='test_user_123')
        
        # Test data
        self.valid_low_stars_data = {
            'stars': 2,
            'text': 'I am feeling really down and anxious today.'
        }
        
        self.valid_text_only_data = {
            'stars': 3,
            'text': 'Having a tough time with work stress.'
        }
        
        self.valid_high_stars_data = {
            'stars': 5,
            'text': ''
        }
        
        self.missing_stars_data = {
            'text': 'Some text without stars'
        }
        
        self.empty_text_data = {
            'stars': 1,
            'text': ''
        }
        
    def tearDown(self):
        """Clean up after each test method."""
        self.app_context.pop()
    
    def _get_auth_headers(self):
        """Helper method to get authorization headers."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    @patch('controllers.mindspace_controller.analyze_sentiment')
    def test_successful_mood_analysis_with_low_stars(self, mock_analyze_sentiment):
        """Test successful mood analysis when stars <= 2."""
        # Mock sentiment analysis response
        mock_analyze_sentiment.return_value = {
            'success': True,
            'sentiment': 'negative',
            'polarity_score': -0.5,
            'suggestion': 'It seems you are feeling down. Remember, tough times pass.'
        }
        
        # Make request
        response = self.client.post(
            '/api/mindspace/mood',
            data=json.dumps(self.valid_low_stars_data),
            headers=self._get_auth_headers()
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['sentiment'], 'negative')
        self.assertIn('suggestion', data)
        
        # Verify sentiment analysis was called
        mock_analyze_sentiment.assert_called_once_with('I am feeling really down and anxious today.')
    
    @patch('controllers.mindspace_controller.analyze_sentiment')
    def test_successful_mood_analysis_with_text_only(self, mock_analyze_sentiment):
        """Test successful mood analysis when user provides text (any stars rating)."""
        # Mock sentiment analysis response
        mock_analyze_sentiment.return_value = {
            'success': True,
            'sentiment': 'neutral',
            'polarity_score': 0.1,
            'suggestion': 'It\'s okay to feel neutral. Try doing something you enjoy.'
        }
        
        # Make request
        response = self.client.post(
            '/api/mindspace/mood',
            data=json.dumps(self.valid_text_only_data),
            headers=self._get_auth_headers()
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['sentiment'], 'neutral')
        self.assertIn('suggestion', data)
        
        # Verify sentiment analysis was called
        mock_analyze_sentiment.assert_called_once_with('Having a tough time with work stress.')
    
    def test_high_stars_without_text_handling(self):
        """Test handling when stars > 2 and no text provided."""
        # Make request
        response = self.client.post(
            '/api/mindspace/mood',
            data=json.dumps(self.valid_high_stars_data),
            headers=self._get_auth_headers()
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Glad you're feeling okay! 😊")
        self.assertNotIn('sentiment', data)
        self.assertNotIn('suggestion', data)
    
    def test_missing_stars_parameter_validation(self):
        """Test validation when stars parameter is missing."""
        # Make request
        response = self.client.post(
            '/api/mindspace/mood',
            data=json.dumps(self.missing_stars_data),
            headers=self._get_auth_headers()
        )
        
        # Assertions
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Mood rating (stars) is required')
    
    @patch('controllers.mindspace_controller.analyze_sentiment')
    def test_empty_text_sentiment_analysis(self, mock_analyze_sentiment):
        """Test sentiment analysis when text is empty for low stars."""
        # Mock sentiment analysis response for default text
        mock_analyze_sentiment.return_value = {
            'success': True,
            'sentiment': 'negative',
            'polarity_score': -0.3,
            'suggestion': 'It seems you are feeling down. Remember, tough times pass.'
        }
        
        # Make request
        response = self.client.post(
            '/api/mindspace/mood',
            data=json.dumps(self.empty_text_data),
            headers=self._get_auth_headers()
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['sentiment'], 'negative')
        self.assertIn('suggestion', data)
        
        # Verify sentiment analysis was called with default text
        mock_analyze_sentiment.assert_called_once_with("I'm not feeling great.")
    
    def test_unauthorized_request_handling(self):
        """Test handling of requests without proper JWT token."""
        # Make request without authorization header
        response = self.client.post(
            '/api/mindspace/mood',
            data=json.dumps(self.valid_low_stars_data),
            headers={'Content-Type': 'application/json'}
        )
        
        # Assertions
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('msg', data)
    
    @patch('controllers.mindspace_controller.analyze_sentiment')
    def test_sentiment_service_error_handling(self, mock_analyze_sentiment):
        """Test handling when sentiment service returns an error."""
        # Mock sentiment analysis to return error
        mock_analyze_sentiment.return_value = {
            'success': False,
            'message': 'No input text provided.'
        }
        
        # Make request
        response = self.client.post(
            '/api/mindspace/mood',
            data=json.dumps(self.valid_low_stars_data),
            headers=self._get_auth_headers()
        )
        
        # Since the controller doesn't handle sentiment service errors explicitly,
        # it will still return success but might not have expected fields
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        # The controller will still try to access sentiment and suggestion keys
        # This test reveals a potential improvement area in error handling
    
    def test_invalid_json_request_handling(self):
        """Test handling of malformed JSON requests."""
        # Make request with invalid JSON
        response = self.client.post(
            '/api/mindspace/mood',
            data='{"stars": 2, "text": "incomplete json"',  # Missing closing brace
            headers=self._get_auth_headers()
        )
        
        # Assertions
        self.assertEqual(response.status_code, 400)
    
    @patch('controllers.mindspace_controller.analyze_sentiment')
    def test_stars_exactly_two_triggers_sentiment_analysis(self, mock_analyze_sentiment):
        """Test that stars exactly equal to 2 triggers sentiment analysis."""
        # Mock sentiment analysis response
        mock_analyze_sentiment.return_value = {
            'success': True,
            'sentiment': 'negative',
            'polarity_score': -0.4,
            'suggestion': 'It seems you are feeling down. Remember, tough times pass.'
        }
        
        test_data = {
            'stars': 2,
            'text': 'Not feeling my best today.'
        }
        
        # Make request
        response = self.client.post(
            '/api/mindspace/mood',
            data=json.dumps(test_data),
            headers=self._get_auth_headers()
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['sentiment'], 'negative')
        self.assertIn('suggestion', data)
        
        # Verify sentiment analysis was called
        mock_analyze_sentiment.assert_called_once_with('Not feeling my best today.')
    
    @patch('controllers.mindspace_controller.analyze_sentiment')
    def test_stars_one_triggers_sentiment_analysis(self, mock_analyze_sentiment):
        """Test that stars equal to 1 triggers sentiment analysis."""
        # Mock sentiment analysis response
        mock_analyze_sentiment.return_value = {
            'success': True,
            'sentiment': 'negative',
            'polarity_score': -0.8,
            'suggestion': 'It seems you are feeling down. Remember, tough times pass.'
        }
        
        test_data = {
            'stars': 1,
            'text': 'Having a really tough day.'
        }
        
        # Make request
        response = self.client.post(
            '/api/mindspace/mood',
            data=json.dumps(test_data),
            headers=self._get_auth_headers()
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['sentiment'], 'negative')
        self.assertIn('suggestion', data)
        
        # Verify sentiment analysis was called
        mock_analyze_sentiment.assert_called_once_with('Having a really tough day.')
    
    @patch('controllers.mindspace_controller.analyze_sentiment')
    def test_stars_three_with_text_triggers_sentiment_analysis(self, mock_analyze_sentiment):
        """Test that stars = 3 with text triggers sentiment analysis."""
        # Mock sentiment analysis response
        mock_analyze_sentiment.return_value = {
            'success': True,
            'sentiment': 'neutral',
            'polarity_score': 0.0,
            'suggestion': 'It\'s okay to feel neutral. Try doing something you enjoy.'
        }
        
        test_data = {
            'stars': 3,
            'text': 'Just an average day, nothing special.'
        }
        
        # Make request
        response = self.client.post(
            '/api/mindspace/mood',
            data=json.dumps(test_data),
            headers=self._get_auth_headers()
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['sentiment'], 'neutral')
        self.assertIn('suggestion', data)
        
        # Verify sentiment analysis was called
        mock_analyze_sentiment.assert_called_once_with('Just an average day, nothing special.')
    
    def test_stars_three_without_text_no_analysis(self):
        """Test that stars = 3 without text does not trigger sentiment analysis."""
        test_data = {
            'stars': 3,
            'text': ''
        }
        
        # Make request
        response = self.client.post(
            '/api/mindspace/mood',
            data=json.dumps(test_data),
            headers=self._get_auth_headers()
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Glad you're feeling okay! 😊")
        self.assertNotIn('sentiment', data)
        self.assertNotIn('suggestion', data)


if __name__ == '__main__':
    unittest.main()