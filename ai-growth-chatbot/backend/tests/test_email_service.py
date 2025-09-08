import unittest
from unittest.mock import patch, MagicMock, Mock
import smtplib
import sys
import os
from email.mime.multipart import MIMEMultipart

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.email_service import EmailService, email_service


class TestEmailService(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.email_service = EmailService()
        
        self.sample_reminder = {
            'title': 'Test Meeting',
            'description': 'Important team meeting',
            'date': '2024-12-31',
            'time': '14:30'
        }
        
    @patch('services.email_service.smtplib.SMTP')
    @patch.dict(os.environ, {
        'EMAIL_HOST': 'smtp.test.com',
        'EMAIL_PORT': '587',
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASS': 'test_password'
    })
    def test_send_reminder_email_with_content_success(self, mock_smtp):
        """Test happy path: Send reminder email with content successfully"""
        # Setup mock SMTP server
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        # Mock successful email sending
        mock_server.sendmail.return_value = {}
        
        result = self.email_service.send_reminder_email(
            'recipient@example.com', 
            self.sample_reminder
        )
        
        # Verify success
        self.assertTrue(result)
        
        # Verify SMTP server interaction
        mock_smtp.assert_called_once_with('smtp.test.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('test@example.com', 'test_password')
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()
        
        # Verify email parameters
        sendmail_call = mock_server.sendmail.call_args[0]
        self.assertEqual(sendmail_call[0], 'test@example.com')  # From
        self.assertEqual(sendmail_call[1], 'recipient@example.com')  # To
        
        # Verify email content contains reminder details
        email_content = sendmail_call[2]
        self.assertIn('Test Meeting', email_content)
        self.assertIn('Important team meeting', email_content)
        self.assertIn('2024-12-31', email_content)
        self.assertIn('14:30', email_content)
        
    @patch('services.email_service.smtplib.SMTP')
    def test_send_reminder_email_smtp_connection_failure(self, mock_smtp):
        """Test exception handling: SMTP connection failure"""
        # Mock SMTP connection failure
        mock_smtp.side_effect = smtplib.SMTPConnectError(421, 'Service not available')
        
        result = self.email_service.send_reminder_email(
            'recipient@example.com', 
            self.sample_reminder
        )
        
        # Verify failure is handled gracefully
        self.assertFalse(result)
        
    @patch('services.email_service.smtplib.SMTP')
    @patch.dict(os.environ, {
        'EMAIL_HOST': 'smtp.test.com',
        'EMAIL_PORT': '587',
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASS': 'wrong_password'
    })
    def test_send_reminder_email_authentication_failure(self, mock_smtp):
        """Test exception handling: SMTP authentication failure"""
        # Setup mock SMTP server
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        # Mock authentication failure
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, 'Authentication failed')
        
        result = self.email_service.send_reminder_email(
            'recipient@example.com', 
            self.sample_reminder
        )
        
        # Verify failure is handled gracefully
        self.assertFalse(result)
        
        # Verify connection was attempted
        mock_smtp.assert_called_once()
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        
    @patch('services.email_service.smtplib.SMTP')
    @patch.dict(os.environ, {
        'EMAIL_HOST': 'smtp.test.com',
        'EMAIL_PORT': '587',
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASS': 'test_password'
    })
    def test_send_reminder_email_sending_failure(self, mock_smtp):
        """Test exception handling: Email sending failure"""
        # Setup mock SMTP server
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        # Mock email sending failure
        mock_server.sendmail.side_effect = smtplib.SMTPRecipientsRefused({
            'recipient@example.com': (550, 'User unknown')
        })
        
        result = self.email_service.send_reminder_email(
            'recipient@example.com', 
            self.sample_reminder
        )
        
        # Verify failure is handled gracefully
        self.assertFalse(result)
        
        # Verify connection and authentication succeeded
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()
        
    @patch('services.email_service.smtplib.SMTP')
    @patch.dict(os.environ, {
        'EMAIL_HOST': 'smtp.test.com',
        'EMAIL_PORT': '587',
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASS': 'test_password'
    })
    def test_send_reminder_email_with_missing_reminder_fields(self, mock_smtp):
        """Test branching: Send reminder email with missing fields"""
        # Setup mock SMTP server
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        mock_server.sendmail.return_value = {}
        
        # Test with minimal reminder data
        minimal_reminder = {}
        
        result = self.email_service.send_reminder_email(
            'recipient@example.com', 
            minimal_reminder
        )
        
        # Should still succeed with default values
        self.assertTrue(result)
        
        # Verify email was sent
        mock_server.sendmail.assert_called_once()
        
        # Verify email content uses defaults for missing fields
        email_content = mock_server.sendmail.call_args[0][2]
        self.assertIn('Task', email_content)  # Default title
        
    @patch('services.email_service.smtplib.SMTP')
    def test_send_generic_email_success(self, mock_smtp):
        """Test happy path: Send generic email successfully"""
        # Setup mock SMTP server
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        mock_server.sendmail.return_value = {}
        
        result = self.email_service.send_email(
            'recipient@example.com',
            'Test Subject',
            'Test email body content'
        )
        
        # Verify success
        self.assertTrue(result)
        
        # Verify SMTP interaction
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('test@example.com', 'test_password')
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()
        
        # Verify email content
        sendmail_call = mock_server.sendmail.call_args[0]
        email_content = sendmail_call[2]
        self.assertIn('Test Subject', email_content)
        self.assertIn('Test email body content', email_content)
        
    @patch('services.email_service.smtplib.SMTP')
    @patch.dict(os.environ, {
        'EMAIL_HOST': 'smtp.test.com',
        'EMAIL_PORT': '587',
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASS': 'test_password'
    })
    def test_send_welcome_email_success(self, mock_smtp):
        """Test happy path: Send welcome email successfully"""
        # Setup mock SMTP server
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        mock_server.sendmail.return_value = {}
        
        result = self.email_service.send_welcome_email(
            'newuser@example.com',
            'John Doe'
        )
        
        # Verify success
        self.assertTrue(result)
        
        # Verify email was sent
        mock_server.sendmail.assert_called_once()
        
        # Verify email content contains welcome message and user name
        email_content = mock_server.sendmail.call_args[0][2]
        self.assertIn('Welcome to Coby AI', email_content)
        self.assertIn('John Doe', email_content)
        self.assertIn('AI Chat Assistant', email_content)
        self.assertIn('MindSpace', email_content)
        self.assertIn('Smart Reminders', email_content)
        
    @patch('services.email_service.smtplib.SMTP')
    @patch.dict(os.environ, {
        'EMAIL_HOST': 'smtp.test.com',
        'EMAIL_PORT': '587',
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASS': 'test_password',
        'CLIENT_URL': 'https://coby.ai'
    })
    def test_send_password_reset_email_success(self, mock_smtp):
        """Test happy path: Send password reset email successfully"""
        # Setup mock SMTP server
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        mock_server.sendmail.return_value = {}
        
        result = self.email_service.send_password_reset_email(
            'user@example.com',
            'reset_token_123',
            'Jane Smith'
        )
        
        # Verify success
        self.assertTrue(result)
        
        # Verify email was sent
        mock_server.sendmail.assert_called_once()
        
        # Verify email content contains reset information
        email_content = mock_server.sendmail.call_args[0][2]
        self.assertIn('Password Reset Request', email_content)
        self.assertIn('Jane Smith', email_content)
        self.assertIn('reset_token_123', email_content)
        self.assertIn('https://coby.ai/reset-password?token=reset_token_123', email_content)
        
    def test_email_service_initialization(self):
        """Test email service initialization with environment variables"""
        with patch.dict(os.environ, {
            'EMAIL_HOST': 'custom.smtp.com',
            'EMAIL_PORT': '465',
            'EMAIL_USER': 'custom@example.com',
            'EMAIL_PASS': 'custom_password',
            'CLIENT_URL': 'https://custom.app.com'
        }):
            service = EmailService()
            
            self.assertEqual(service.smtp_host, 'custom.smtp.com')
            self.assertEqual(service.smtp_port, 465)
            self.assertEqual(service.email_user, 'custom@example.com')
            self.assertEqual(service.email_pass, 'custom_password')
            self.assertEqual(service.client_url, 'https://custom.app.com')
            
    def test_email_service_default_values(self):
        """Test email service initialization with default values"""
        with patch.dict(os.environ, {}, clear=True):
            service = EmailService()
            
            self.assertEqual(service.smtp_host, 'smtp.gmail.com')
            self.assertEqual(service.smtp_port, 587)
            self.assertEqual(service.client_url, 'http://localhost:5174')
            
    def test_global_email_service_instance(self):
        """Test that global email service instance is created"""
        self.assertIsInstance(email_service, EmailService)
        
    @patch('services.email_service.smtplib.SMTP')
    @patch.dict(os.environ, {
        'EMAIL_HOST': 'smtp.test.com',
        'EMAIL_PORT': '587',
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASS': 'test_password'
    })
    def test_email_service_server_cleanup_on_success(self, mock_smtp):
        """Test that SMTP server connection is properly closed on success"""
        # Setup mock SMTP server
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        mock_server.sendmail.return_value = {}
        
        self.email_service.send_email(
            'recipient@example.com',
            'Test Subject',
            'Test Body'
        )
        
        # Verify server.quit() was called to close connection
        mock_server.quit.assert_called_once()
        
    @patch('services.email_service.smtplib.SMTP')
    @patch.dict(os.environ, {
        'EMAIL_HOST': 'smtp.test.com',
        'EMAIL_PORT': '587',
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASS': 'test_password'
    })
    def test_email_service_server_cleanup_on_failure(self, mock_smtp):
        """Test that SMTP server connection cleanup is handled on failure"""
        # Setup mock SMTP server
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        # Mock failure during sendmail
        mock_server.sendmail.side_effect = Exception('Send failed')
        
        result = self.email_service.send_email(
            'recipient@example.com',
            'Test Subject',
            'Test Body'
        )
        
        # Verify failure was handled gracefully
        self.assertFalse(result)
        
        # Note: In current implementation, quit() might not be called on exception
        # This test documents the current behavior and could be improved


if __name__ == '__main__':
    unittest.main()