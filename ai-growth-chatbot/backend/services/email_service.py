import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('EMAIL_PORT', 587))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_pass = os.getenv('EMAIL_PASS')
        self.client_url = os.getenv('CLIENT_URL', 'http://localhost:5174')

    def send_password_reset_email(self, to_email, reset_token, user_name):
        """Send password reset email"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Password Reset Request - Coby AI"
            msg['From'] = self.email_user
            msg['To'] = to_email

            # Create reset URL
            reset_url = f"{self.client_url}/reset-password?token={reset_token}"

            # Create HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🤖 Coby AI</h1>
                        <h2>Password Reset Request</h2>
                    </div>
                    <div class="content">
                        <p>Hello {user_name},</p>
                        
                        <p>We received a request to reset your password for your Coby AI account. If you didn't make this request, you can safely ignore this email.</p>
                        
                        <p>To reset your password, click the button below:</p>
                        
                        <p style="text-align: center;">
                            <a href="{reset_url}" class="button">Reset Password</a>
                        </p>
                        
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; background: #eee; padding: 10px; border-radius: 5px;">
                            {reset_url}
                        </p>
                        
                        <p><strong>This link will expire in 1 hour for security reasons.</strong></p>
                        
                        <p>If you have any questions or need help, please contact our support team.</p>
                        
                        <p>Best regards,<br>The Coby AI Team</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated email. Please do not reply to this message.</p>
                        <p>© 2024 Coby AI. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Create text content (fallback)
            text_content = f"""
            Password Reset Request - Coby AI

            Hello {user_name},

            We received a request to reset your password for your Coby AI account. If you didn't make this request, you can safely ignore this email.

            To reset your password, visit the following link:
            {reset_url}

            This link will expire in 1 hour for security reasons.

            If you have any questions or need help, please contact our support team.

            Best regards,
            The Coby AI Team

            ---
            This is an automated email. Please do not reply to this message.
            © 2024 Coby AI. All rights reserved.
            """

            # Attach parts
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)

            # Send email
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            text = msg.as_string()
            server.sendmail(self.email_user, to_email, text)
            server.quit()

            return True

        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    def send_welcome_email(self, to_email, user_name):
        """Send welcome email to new users"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Welcome to Coby AI! 🎉"
            msg['From'] = self.email_user
            msg['To'] = to_email

            # Create HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .feature {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #667eea; }}
                    .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🤖 Welcome to Coby AI!</h1>
                        <p>Your AI-powered growth companion</p>
                    </div>
                    <div class="content">
                        <p>Hello {user_name},</p>
                        
                        <p>Welcome to Coby AI! We're excited to have you join our community of learners and achievers.</p>
                        
                        <h3>🚀 What you can do with Coby:</h3>
                        
                        <div class="feature">
                            <strong>💬 AI Chat Assistant</strong><br>
                            Get intelligent responses and personalized guidance
                        </div>
                        
                        <div class="feature">
                            <strong>🧠 MindSpace</strong><br>
                            Organize your thoughts and ideas effectively
                        </div>
                        
                        <div class="feature">
                            <strong>⏰ Smart Reminders</strong><br>
                            Never miss important tasks or deadlines
                        </div>
                        
                        <div class="feature">
                            <strong>💻 Coding Space</strong><br>
                            Practice and improve your programming skills
                        </div>
                        
                        <p style="text-align: center;">
                            <a href="{self.client_url}/login" class="button">Get Started Now</a>
                        </p>
                        
                        <p>If you have any questions or need help getting started, feel free to reach out to our support team.</p>
                        
                        <p>Happy learning!<br>The Coby AI Team</p>
                    </div>
                    <div class="footer">
                        <p>© 2024 Coby AI. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Create text content (fallback)
            text_content = f"""
            Welcome to Coby AI! 🎉

            Hello {user_name},

            Welcome to Coby AI! We're excited to have you join our community of learners and achievers.

            What you can do with Coby:
            - AI Chat Assistant: Get intelligent responses and personalized guidance
            - MindSpace: Organize your thoughts and ideas effectively  
            - Smart Reminders: Never miss important tasks or deadlines
            - Coding Space: Practice and improve your programming skills

            Get started: {self.client_url}/login

            If you have any questions or need help getting started, feel free to reach out to our support team.

            Happy learning!
            The Coby AI Team

            ---
            © 2024 Coby AI. All rights reserved.
            """

            # Attach parts
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)

            # Send email
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            text = msg.as_string()
            server.sendmail(self.email_user, to_email, text)
            server.quit()

            return True

        except Exception as e:
            print(f"Failed to send welcome email: {str(e)}")
            return False

    def send_email(self, to_email, subject, body):
        """Send a generic email"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.email_user
            msg['To'] = to_email

            # Create content
            msg.attach(MIMEText(body, 'plain'))

            # Send email
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            text = msg.as_string()
            server.sendmail(self.email_user, to_email, text)
            server.quit()

            return True

        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

# Create global instance
email_service = EmailService()