import unittest
from unittest.mock import patch, MagicMock, Mock, call
from datetime import datetime, timedelta
import pytz
from bson import ObjectId
import sys
import os

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.reminder_scheduler import (
    get_reminder_datetime, 
    send_reminder_job, 
    schedule_reminders, 
    start_scheduler
)


class TestReminderScheduler(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_reminder = {
            '_id': ObjectId('507f1f77bcf86cd799439011'),
            'user_email': 'test@example.com',
            'title': 'Test Meeting',
            'description': 'Important team meeting',
            'date': '2024-12-31',
            'time': '14:30',
            'timezone': 'UTC',
            'notified': False
        }
        
        self.utc_tz = pytz.UTC
        self.eastern_tz = pytz.timezone('US/Eastern')
        
    def test_get_reminder_datetime_success_utc(self):
        """Test happy path: Get reminder datetime with UTC timezone"""
        reminder = self.sample_reminder.copy()
        
        result = get_reminder_datetime(reminder)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.year, 2024)
        self.assertEqual(result.month, 12)
        self.assertEqual(result.day, 31)
        self.assertEqual(result.hour, 14)
        self.assertEqual(result.minute, 30)
        self.assertEqual(result.tzinfo, self.utc_tz)
        
    def test_get_reminder_datetime_with_different_timezone(self):
        """Test get reminder datetime with non-UTC timezone"""
        reminder = self.sample_reminder.copy()
        reminder['timezone'] = 'US/Eastern'
        
        result = get_reminder_datetime(reminder)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.tzinfo, self.eastern_tz)
        
    def test_get_reminder_datetime_missing_date(self):
        """Test input verification: Missing date field"""
        reminder = self.sample_reminder.copy()
        del reminder['date']
        
        result = get_reminder_datetime(reminder)
        
        self.assertIsNone(result)
        
    def test_get_reminder_datetime_missing_time(self):
        """Test input verification: Missing time field"""
        reminder = self.sample_reminder.copy()
        del reminder['time']
        
        result = get_reminder_datetime(reminder)
        
        self.assertIsNone(result)
        
    def test_get_reminder_datetime_invalid_format(self):
        """Test exception handling: Invalid datetime format"""
        invalid_formats = [
            {'date': 'invalid-date', 'time': '14:30'},
            {'date': '2024-12-31', 'time': 'invalid-time'},
            {'date': '31-12-2024', 'time': '14:30'},  # Wrong date format
            {'date': '2024-12-31', 'time': '2:30'},   # Wrong time format
        ]
        
        for invalid_format in invalid_formats:
            with self.subTest(invalid_format=invalid_format):
                reminder = self.sample_reminder.copy()
                reminder.update(invalid_format)
                
                result = get_reminder_datetime(reminder)
                
                self.assertIsNone(result)
                
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.email_service')
    def test_send_reminder_email_with_content(self, mock_email_service, mock_collection):
        """Test happy path: Send reminder email with content"""
        # Mock finding reminder in database
        mock_collection.find_one.return_value = self.sample_reminder
        mock_email_service.send_reminder_email.return_value = True
        
        reminder_id = ObjectId('507f1f77bcf86cd799439011')
        
        send_reminder_job(reminder_id)
        
        # Verify database query
        mock_collection.find_one.assert_called_once_with({'_id': reminder_id})
        
        # Verify email was sent with correct parameters
        mock_email_service.send_reminder_email.assert_called_once_with(
            'test@example.com', 
            self.sample_reminder
        )
        
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.email_service')
    def test_send_reminder_job_reminder_not_found(self, mock_email_service, mock_collection):
        """Test exception handling: Reminder not found in database"""
        # Mock reminder not found
        mock_collection.find_one.return_value = None
        
        reminder_id = ObjectId('507f1f77bcf86cd799439999')
        
        # Should not raise exception
        send_reminder_job(reminder_id)
        
        # Verify database was queried
        mock_collection.find_one.assert_called_once_with({'_id': reminder_id})
        
        # Verify email was not attempted
        mock_email_service.send_reminder_email.assert_not_called()
        
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.email_service')
    def test_send_reminder_job_missing_email(self, mock_email_service, mock_collection):
        """Test branching: Send reminder with missing email"""
        reminder_without_email = self.sample_reminder.copy()
        del reminder_without_email['user_email']
        
        mock_collection.find_one.return_value = reminder_without_email
        
        reminder_id = ObjectId('507f1f77bcf86cd799439011')
        
        send_reminder_job(reminder_id)
        
        # Verify database was queried
        mock_collection.find_one.assert_called_once_with({'_id': reminder_id})
        
        # Verify email was not sent due to missing email
        mock_email_service.send_reminder_email.assert_not_called()
        
    @patch('services.reminder_scheduler.scheduler')
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.datetime')
    def test_schedule_reminders_finds_pending_tasks(self, mock_datetime, mock_collection, mock_scheduler):
        """Test happy path: Schedule reminders finds pending tasks"""
        # Mock current time
        now = datetime(2024, 12, 30, 10, 0, 0, tzinfo=pytz.UTC)
        mock_datetime.utcnow.return_value = now.replace(tzinfo=None)
        
        # Mock pending reminders
        future_reminder = self.sample_reminder.copy()
        future_reminder['date'] = '2024-12-31'  # Tomorrow
        future_reminder['time'] = '14:30'
        
        mock_collection.find.return_value = [future_reminder]
        
        # Mock scheduler methods
        mock_scheduler.get_job.return_value = None  # Job doesn't exist yet
        mock_scheduler.add_job.return_value = Mock()
        
        schedule_reminders()
        
        # Verify database query for pending reminders
        expected_query = {
            'notified': {'$ne': True},
            'date': {'$exists': True},
            'time': {'$exists': True}
        }
        mock_collection.find.assert_called_once_with(expected_query)
        
        # Verify scheduler job was added
        mock_scheduler.add_job.assert_called_once()
        job_call = mock_scheduler.add_job.call_args
        
        # Check job parameters
        self.assertEqual(job_call[0][0], send_reminder_job)  # Function
        self.assertEqual(job_call[1]['trigger'], 'date')  # Trigger type
        self.assertEqual(job_call[1]['args'], [future_reminder['_id']])  # Arguments
        self.assertEqual(job_call[1]['id'], f"reminder_{str(future_reminder['_id'])}")  # Job ID
        
    @patch('services.reminder_scheduler.scheduler')
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.datetime')
    def test_schedule_reminders_skips_past_reminders(self, mock_datetime, mock_collection, mock_scheduler):
        """Test branching: Schedule reminders skips past reminders"""
        # Mock current time
        now = datetime(2024, 12, 31, 16, 0, 0, tzinfo=pytz.UTC)
        mock_datetime.utcnow.return_value = now.replace(tzinfo=None)
        
        # Mock past reminder
        past_reminder = self.sample_reminder.copy()
        past_reminder['date'] = '2024-12-31'  # Same day
        past_reminder['time'] = '14:30'  # But earlier time
        
        mock_collection.find.return_value = [past_reminder]
        mock_scheduler.get_job.return_value = None
        
        schedule_reminders()
        
        # Verify no job was scheduled for past reminder
        mock_scheduler.add_job.assert_not_called()
        
    @patch('services.reminder_scheduler.scheduler')
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.datetime')
    def test_schedule_reminders_skips_existing_jobs(self, mock_datetime, mock_collection, mock_scheduler):
        """Test branching: Schedule reminders skips existing jobs"""
        # Mock current time
        now = datetime(2024, 12, 30, 10, 0, 0, tzinfo=pytz.UTC)
        mock_datetime.utcnow.return_value = now.replace(tzinfo=None)
        
        future_reminder = self.sample_reminder.copy()
        future_reminder['date'] = '2024-12-31'
        future_reminder['time'] = '14:30'
        
        mock_collection.find.return_value = [future_reminder]
        
        # Mock existing job
        mock_existing_job = Mock()
        mock_scheduler.get_job.return_value = mock_existing_job
        
        schedule_reminders()
        
        # Verify job was not added since it already exists
        mock_scheduler.add_job.assert_not_called()
        
    @patch('services.reminder_scheduler.scheduler')
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.datetime')
    def test_apscheduler_job_creation_failure(self, mock_datetime, mock_collection, mock_scheduler):
        """Test exception handling: APScheduler job creation failure"""
        # Mock current time
        now = datetime(2024, 12, 30, 10, 0, 0, tzinfo=pytz.UTC)
        mock_datetime.utcnow.return_value = now.replace(tzinfo=None)
        
        future_reminder = self.sample_reminder.copy()
        future_reminder['date'] = '2024-12-31'
        future_reminder['time'] = '14:30'
        
        mock_collection.find.return_value = [future_reminder]
        mock_scheduler.get_job.return_value = None
        
        # Mock scheduler exception
        mock_scheduler.add_job.side_effect = Exception('Scheduler unavailable')
        
        # Should not raise exception - error handling should be graceful
        try:
            schedule_reminders()
        except Exception as e:
            self.fail(f"schedule_reminders raised an exception: {e}")
            
    @patch('services.reminder_scheduler.scheduler')
    @patch('services.reminder_scheduler.schedule_reminders')
    def test_start_scheduler(self, mock_schedule_reminders, mock_scheduler):
        """Test scheduler startup process"""
        mock_scheduler.start.return_value = Mock()
        
        start_scheduler()
        
        # Verify scheduler was started
        mock_scheduler.start.assert_called_once()
        
        # Verify initial reminder scheduling was called
        mock_schedule_reminders.assert_called_once()
        
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.datetime')
    def test_schedule_reminders_handles_invalid_datetime_gracefully(self, mock_datetime, mock_collection):
        """Test exception handling: Invalid reminder datetime handled gracefully"""
        # Mock current time
        now = datetime(2024, 12, 30, 10, 0, 0, tzinfo=pytz.UTC)
        mock_datetime.utcnow.return_value = now.replace(tzinfo=None)
        
        # Mock reminder with invalid date/time
        invalid_reminder = self.sample_reminder.copy()
        invalid_reminder['date'] = 'invalid-date'
        invalid_reminder['time'] = 'invalid-time'
        
        mock_collection.find.return_value = [invalid_reminder]
        
        # Should not raise exception
        try:
            schedule_reminders()
        except Exception as e:
            self.fail(f"schedule_reminders raised an exception for invalid datetime: {e}")
            
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.datetime')
    def test_schedule_reminders_handles_database_error(self, mock_datetime, mock_collection):
        """Test exception handling: Database connection error"""
        # Mock current time
        now = datetime(2024, 12, 30, 10, 0, 0, tzinfo=pytz.UTC)
        mock_datetime.utcnow.return_value = now.replace(tzinfo=None)
        
        # Mock database exception
        mock_collection.find.side_effect = Exception('Database connection failed')
        
        # Should not raise exception - error should be handled gracefully
        try:
            schedule_reminders()
        except Exception as e:
            self.fail(f"schedule_reminders raised an exception for database error: {e}")


if __name__ == '__main__':
    unittest.main()