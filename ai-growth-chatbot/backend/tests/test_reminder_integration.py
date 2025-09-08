import unittest
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime, timedelta
import pytz
from bson import ObjectId
import sys
import os

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.reminder_scheduler import schedule_reminders, send_reminder_job
from services.email_service import EmailService


class TestReminderIntegration(unittest.TestCase):
    """Integration tests for the complete reminder flow"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_reminder = {
            '_id': ObjectId('507f1f77bcf86cd799439011'),
            'user_email': 'test@example.com',
            'title': 'Integration Test Meeting',
            'description': 'End-to-end reminder test',
            'date': '2024-12-31',
            'time': '14:30',
            'timezone': 'UTC',
            'notified': False
        }
        
    @patch('services.reminder_scheduler.scheduler')
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.datetime')
    def test_complete_reminder_scheduling_flow(self, mock_datetime, mock_collection, mock_scheduler):
        """Test complete flow: Create reminder -> Schedule job -> Execute at right time"""
        # Step 1: Mock current time (before reminder time)
        now = datetime(2024, 12, 30, 10, 0, 0, tzinfo=pytz.UTC)
        mock_datetime.utcnow.return_value = now.replace(tzinfo=None)
        
        # Step 2: Mock pending reminder in database
        mock_collection.find.return_value = [self.sample_reminder]
        
        # Step 3: Mock scheduler - no existing job
        mock_scheduler.get_job.return_value = None
        mock_scheduler.add_job.return_value = Mock()
        
        # Execute scheduling
        schedule_reminders()
        
        # Verify database query
        expected_query = {
            'notified': {'$ne': True},
            'date': {'$exists': True},
            'time': {'$exists': True}
        }
        mock_collection.find.assert_called_once_with(expected_query)
        
        # Verify scheduler job creation
        mock_scheduler.add_job.assert_called_once()
        job_call = mock_scheduler.add_job.call_args
        
        # Verify job parameters
        self.assertEqual(job_call[0][0], send_reminder_job)  # Function to call
        self.assertEqual(job_call[1]['trigger'], 'date')  # Date trigger
        self.assertEqual(job_call[1]['args'], [self.sample_reminder['_id']])  # Reminder ID
        
        # Verify job ID format
        expected_job_id = f"reminder_{str(self.sample_reminder['_id'])}"
        self.assertEqual(job_call[1]['id'], expected_job_id)
        
        # Verify run_date is properly calculated
        run_date = job_call[1]['run_date']
        self.assertEqual(run_date.year, 2024)
        self.assertEqual(run_date.month, 12)
        self.assertEqual(run_date.day, 31)
        self.assertEqual(run_date.hour, 14)
        self.assertEqual(run_date.minute, 30)
        
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.email_service.smtplib.SMTP')
    @patch.dict(os.environ, {
        'EMAIL_HOST': 'smtp.test.com',
        'EMAIL_PORT': '587',
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASS': 'test_password'
    })
    def test_complete_email_sending_flow(self, mock_smtp, mock_collection):
        """Test complete flow: Job executes -> Finds reminder -> Sends email"""
        # Step 1: Mock reminder found in database
        mock_collection.find_one.return_value = self.sample_reminder
        
        # Step 2: Mock successful SMTP server
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        mock_server.sendmail.return_value = {}
        
        # Step 3: Execute reminder job (simulating APScheduler execution)
        reminder_id = self.sample_reminder['_id']
        send_reminder_job(reminder_id)
        
        # Verify database lookup
        mock_collection.find_one.assert_called_once_with({'_id': reminder_id})
        
        # Verify email server interaction
        mock_smtp.assert_called_once_with('smtp.test.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('test@example.com', 'test_password')
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()
        
        # Verify email content
        sendmail_call = mock_server.sendmail.call_args[0]
        email_from = sendmail_call[0]
        email_to = sendmail_call[1]
        email_content = sendmail_call[2]
        
        self.assertEqual(email_from, 'test@example.com')
        self.assertEqual(email_to, 'test@example.com')
        self.assertIn('Integration Test Meeting', email_content)
        self.assertIn('End-to-end reminder test', email_content)
        self.assertIn('2024-12-31', email_content)
        self.assertIn('14:30', email_content)
        
    @patch('services.reminder_scheduler.scheduler')
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.datetime')
    def test_multiple_reminders_scheduling(self, mock_datetime, mock_collection, mock_scheduler):
        """Test scheduling multiple reminders with different times"""
        # Mock current time
        now = datetime(2024, 12, 30, 10, 0, 0, tzinfo=pytz.UTC)
        mock_datetime.utcnow.return_value = now.replace(tzinfo=None)
        
        # Create multiple reminders
        reminder1 = self.sample_reminder.copy()
        reminder1['_id'] = ObjectId('507f1f77bcf86cd799439011')
        reminder1['title'] = 'Morning Meeting'
        reminder1['time'] = '09:00'
        
        reminder2 = self.sample_reminder.copy()
        reminder2['_id'] = ObjectId('507f1f77bcf86cd799439012')
        reminder2['title'] = 'Afternoon Meeting'
        reminder2['time'] = '15:30'
        
        reminder3 = self.sample_reminder.copy()
        reminder3['_id'] = ObjectId('507f1f77bcf86cd799439013')
        reminder3['title'] = 'Past Meeting'
        reminder3['date'] = '2024-12-29'  # Past date - should be skipped
        reminder3['time'] = '14:00'
        
        mock_collection.find.return_value = [reminder1, reminder2, reminder3]
        mock_scheduler.get_job.return_value = None
        mock_scheduler.add_job.return_value = Mock()
        
        schedule_reminders()
        
        # Verify only 2 jobs were scheduled (past reminder skipped)
        self.assertEqual(mock_scheduler.add_job.call_count, 2)
        
        # Verify both future reminders got scheduled
        job_calls = mock_scheduler.add_job.call_args_list
        scheduled_ids = [call[1]['args'][0] for call in job_calls]
        
        self.assertIn(reminder1['_id'], scheduled_ids)
        self.assertIn(reminder2['_id'], scheduled_ids)
        self.assertNotIn(reminder3['_id'], scheduled_ids)  # Past reminder not scheduled
        
    @patch('services.reminder_scheduler.scheduler')
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.datetime')
    def test_error_resilience_in_scheduling(self, mock_datetime, mock_collection, mock_scheduler):
        """Test that scheduling continues even if individual reminders fail"""
        # Mock current time
        now = datetime(2024, 12, 30, 10, 0, 0, tzinfo=pytz.UTC)
        mock_datetime.utcnow.return_value = now.replace(tzinfo=None)
        
        # Create reminders - one valid, one with invalid datetime
        valid_reminder = self.sample_reminder.copy()
        valid_reminder['_id'] = ObjectId('507f1f77bcf86cd799439011')
        
        invalid_reminder = self.sample_reminder.copy()
        invalid_reminder['_id'] = ObjectId('507f1f77bcf86cd799439012')
        invalid_reminder['date'] = 'invalid-date'  # This will cause parsing error
        invalid_reminder['time'] = 'invalid-time'
        
        mock_collection.find.return_value = [valid_reminder, invalid_reminder]
        mock_scheduler.get_job.return_value = None
        mock_scheduler.add_job.return_value = Mock()
        
        # Should not raise exception despite invalid reminder
        schedule_reminders()
        
        # Verify only valid reminder was scheduled
        mock_scheduler.add_job.assert_called_once()
        job_call = mock_scheduler.add_job.call_args
        self.assertEqual(job_call[1]['args'][0], valid_reminder['_id'])
        
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.email_service.smtplib.SMTP')
    def test_email_failure_handling_in_job_execution(self, mock_smtp, mock_collection):
        """Test that job execution handles email failures gracefully"""
        # Mock reminder found in database
        mock_collection.find_one.return_value = self.sample_reminder
        
        # Mock SMTP failure
        mock_smtp.side_effect = Exception('SMTP server unavailable')
        
        # Should not raise exception
        try:
            send_reminder_job(self.sample_reminder['_id'])
        except Exception as e:
            self.fail(f"send_reminder_job raised an exception: {e}")
            
        # Verify database was still queried
        mock_collection.find_one.assert_called_once()
        
    @patch('services.reminder_scheduler.scheduler')
    @patch('services.reminder_scheduler.reminders_col')
    @patch('services.reminder_scheduler.datetime')
    def test_timezone_handling_in_scheduling(self, mock_datetime, mock_collection, mock_scheduler):
        """Test that different timezones are handled correctly in scheduling"""
        # Mock current time in UTC
        now = datetime(2024, 12, 30, 10, 0, 0, tzinfo=pytz.UTC)
        mock_datetime.utcnow.return_value = now.replace(tzinfo=None)
        
        # Create reminder in different timezone
        eastern_reminder = self.sample_reminder.copy()
        eastern_reminder['timezone'] = 'US/Eastern'
        eastern_reminder['time'] = '09:30'  # 9:30 AM Eastern = 14:30 UTC
        
        mock_collection.find.return_value = [eastern_reminder]
        mock_scheduler.get_job.return_value = None
        mock_scheduler.add_job.return_value = Mock()
        
        schedule_reminders()
        
        # Verify job was scheduled
        mock_scheduler.add_job.assert_called_once()
        
        # Verify run_date accounts for timezone
        job_call = mock_scheduler.add_job.call_args
        run_date = job_call[1]['run_date']
        
        # The run_date should be timezone-aware
        self.assertIsNotNone(run_date.tzinfo)
        
    def test_reminder_data_validation_edge_cases(self):
        """Test various edge cases in reminder data validation"""
        from services.reminder_scheduler import get_reminder_datetime
        
        edge_cases = [
            # Missing fields
            {},
            {'date': '2024-12-31'},  # Missing time
            {'time': '14:30'},  # Missing date
            
            # Invalid date formats
            {'date': '2024/12/31', 'time': '14:30'},
            {'date': '31-12-2024', 'time': '14:30'},
            {'date': 'Dec 31, 2024', 'time': '14:30'},
            
            # Invalid time formats
            {'date': '2024-12-31', 'time': '2:30'},
            {'date': '2024-12-31', 'time': '14:30:00'},
            {'date': '2024-12-31', 'time': '2:30 PM'},
            
            # Edge dates
            {'date': '2024-02-29', 'time': '14:30'},  # Leap year - valid
            {'date': '2023-02-29', 'time': '14:30'},  # Non-leap year - invalid
            {'date': '2024-13-01', 'time': '14:30'},  # Invalid month
            {'date': '2024-12-32', 'time': '14:30'},  # Invalid day
        ]
        
        for case in edge_cases:
            with self.subTest(case=case):
                result = get_reminder_datetime(case)
                if case == {'date': '2024-02-29', 'time': '14:30'}:
                    # This should be valid (2024 is a leap year)
                    self.assertIsNotNone(result)
                else:
                    # All other cases should return None
                    self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()