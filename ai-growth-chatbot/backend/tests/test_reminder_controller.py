import unittest
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime, timedelta
import json
from bson import ObjectId
import sys
import os

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.reminder_controller import reminder_bp
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token


class TestReminderController(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        self.app.config['JWT_SECRET_KEY'] = 'jwt-test-secret'
        self.app.config['TESTING'] = True
        
        # Initialize JWT
        self.jwt = JWTManager(self.app)
        
        # Register blueprint
        self.app.register_blueprint(reminder_bp, url_prefix='/api/reminders')
        
        # Create test client
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create test access token
        with self.app.test_request_context():
            self.access_token = create_access_token(identity='test_user_123')
        
        self.valid_reminder_data = {
            'title': 'Test Meeting',
            'description': 'Important team meeting',
            'remind_at': '2024-12-31 14:30:00',
            'email': 'test@example.com'
        }
        
    def tearDown(self):
        """Clean up after each test method."""
        self.app_context.pop()
        
    def test_user_creates_reminder_successfully(self):
        """Test happy path: User creates reminder successfully"""
        with patch('controllers.reminder_controller.reminders_collection') as mock_collection:
            # Mock successful MongoDB insertion
            mock_collection.insert_one.return_value = Mock()
            
            with patch('controllers.reminder_controller.email_service.send_email') as mock_email:
                mock_email.return_value = True
                
                response = self.client.post(
                    '/api/reminders/',
                    data=json.dumps(self.valid_reminder_data),
                    content_type='application/json',
                    headers={'Authorization': f'Bearer {self.access_token}'}
                )
                
                self.assertEqual(response.status_code, 201)
                response_data = json.loads(response.data)
                self.assertTrue(response_data['success'])
                self.assertEqual(response_data['message'], 'Reminder added successfully.')
                
                # Verify MongoDB was called with correct data
                mock_collection.insert_one.assert_called_once()
                inserted_data = mock_collection.insert_one.call_args[0][0]
                self.assertEqual(inserted_data['user_id'], 'test_user_123')
                self.assertEqual(inserted_data['title'], 'Test Meeting')
                self.assertEqual(inserted_data['description'], 'Important team meeting')
                
                # Verify email was sent
                mock_email.assert_called_once()
                
    def test_missing_required_reminder_fields(self):
        """Test input verification: Missing required reminder fields"""
        test_cases = [
            {},  # Empty data
            {'title': 'Test'},  # Missing description and remind_at
            {'description': 'Test'},  # Missing title and remind_at
            {'remind_at': '2024-12-31 14:30:00'},  # Missing title and description
            {'title': 'Test', 'description': 'Test'},  # Missing remind_at
        ]
        
        for invalid_data in test_cases:
            with self.subTest(invalid_data=invalid_data):
                response = self.client.post(
                    '/api/reminders/',
                    data=json.dumps(invalid_data),
                    content_type='application/json',
                    headers={'Authorization': f'Bearer {self.access_token}'}
                )
                
                self.assertEqual(response.status_code, 400)
                response_data = json.loads(response.data)
                self.assertFalse(response_data['success'])
                self.assertEqual(response_data['message'], 'All fields are required.')
                
    def test_invalid_reminder_time_format(self):
        """Test input verification: Invalid reminder time format"""
        invalid_formats = [
            '2024-12-31',  # Missing time
            '14:30:00',  # Missing date
            '31-12-2024 14:30:00',  # Wrong date format
            '2024/12/31 14:30:00',  # Wrong date separator
            '2024-12-31 2:30:00',  # Wrong time format
            'invalid-datetime',  # Completely invalid
        ]
        
        for invalid_time in invalid_formats:
            with self.subTest(invalid_time=invalid_time):
                invalid_data = self.valid_reminder_data.copy()
                invalid_data['remind_at'] = invalid_time
                
                response = self.client.post(
                    '/api/reminders/',
                    data=json.dumps(invalid_data),
                    content_type='application/json',
                    headers={'Authorization': f'Bearer {self.access_token}'}
                )
                
                self.assertEqual(response.status_code, 400)
                response_data = json.loads(response.data)
                self.assertFalse(response_data['success'])
                self.assertEqual(response_data['message'], 'Invalid datetime format. Use YYYY-MM-DD HH:MM:SS')
                
    def test_mongodb_connection_failure_handling(self):
        """Test exception handling: MongoDB connection failure handling"""
        with patch('controllers.reminder_controller.reminders_collection') as mock_collection:
            # Mock MongoDB exception
            mock_collection.insert_one.side_effect = Exception('MongoDB connection failed')
            
            response = self.client.post(
                '/api/reminders/',
                data=json.dumps(self.valid_reminder_data),
                content_type='application/json',
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            
            self.assertEqual(response.status_code, 500)
            response_data = json.loads(response.data)
            self.assertFalse(response_data['success'])
            self.assertIn('MongoDB connection failed', response_data['error'])
            
    def test_email_sending_failure_handling(self):
        """Test exception handling: Email sending failure handling"""
        with patch('controllers.reminder_controller.reminders_collection') as mock_collection:
            mock_collection.insert_one.return_value = Mock()
            
            with patch('controllers.reminder_controller.email_service.send_email') as mock_email:
                # Mock email service exception
                mock_email.side_effect = Exception('SMTP server unavailable')
                
                response = self.client.post(
                    '/api/reminders/',
                    data=json.dumps(self.valid_reminder_data),
                    content_type='application/json',
                    headers={'Authorization': f'Bearer {self.access_token}'}
                )
                
                # Should still return success as email is optional
                self.assertEqual(response.status_code, 201)
                response_data = json.loads(response.data)
                self.assertTrue(response_data['success'])
                
                # Verify reminder was still saved despite email failure
                mock_collection.insert_one.assert_called_once()
                
    @patch('controllers.reminder_controller.reminders_collection')
    def test_get_reminders_success(self, mock_collection):
        """Test fetching user reminders successfully"""
        # Mock reminder data
        mock_reminders = [
            {
                '_id': ObjectId('507f1f77bcf86cd799439011'),
                'user_id': 'test_user_123',
                'title': 'Meeting 1',
                'description': 'Team standup',
                'remind_at': datetime(2024, 12, 31, 14, 30, 0),
                'created_at': datetime(2024, 12, 1, 10, 0, 0)
            },
            {
                '_id': ObjectId('507f1f77bcf86cd799439012'),
                'user_id': 'test_user_123',
                'title': 'Meeting 2',
                'description': 'Project review',
                'remind_at': datetime(2025, 1, 15, 16, 0, 0),
                'created_at': datetime(2024, 12, 2, 11, 0, 0)
            }
        ]
        
        mock_collection.find.return_value = mock_reminders
        
        response = self.client.get(
            '/api/reminders/',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertEqual(len(response_data['reminders']), 2)
        
        # Verify filter was applied
        mock_collection.find.assert_called_once_with({'user_id': 'test_user_123'})
        
        # Check data transformation
        reminder = response_data['reminders'][0]
        self.assertEqual(reminder['title'], 'Meeting 1')
        self.assertEqual(reminder['remind_at'], '2024-12-31 14:30:00')
        
    @patch('controllers.reminder_controller.reminders_collection')
    def test_delete_reminder_success(self, mock_collection):
        """Test deleting reminder successfully"""
        # Mock successful deletion
        mock_result = Mock()
        mock_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_result
        
        reminder_id = '507f1f77bcf86cd799439011'
        response = self.client.delete(
            f'/api/reminders/{reminder_id}',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Reminder deleted.')
        
        # Verify delete was called with correct filter
        mock_collection.delete_one.assert_called_once()
        delete_filter = mock_collection.delete_one.call_args[0][0]
        self.assertEqual(str(delete_filter['_id']), reminder_id)
        self.assertEqual(delete_filter['user_id'], 'test_user_123')
        
    @patch('controllers.reminder_controller.reminders_collection')
    def test_delete_reminder_not_found(self, mock_collection):
        """Test deleting non-existent reminder"""
        # Mock no deletion (reminder not found)
        mock_result = Mock()
        mock_result.deleted_count = 0
        mock_collection.delete_one.return_value = mock_result
        
        reminder_id = '507f1f77bcf86cd799439999'
        response = self.client.delete(
            f'/api/reminders/{reminder_id}',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Reminder not found.')


if __name__ == '__main__':
    unittest.main()