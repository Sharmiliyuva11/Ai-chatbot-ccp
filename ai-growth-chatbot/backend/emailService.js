const nodemailer = require('nodemailer');

// Email configuration (using Gmail as example - in production, use environment variables)
const createTransporter = () => {
  return nodemailer.createTransporter({
    service: 'gmail',
    auth: {
      user: process.env.EMAIL_USER || 'your-email@gmail.com', // Replace with your email
      pass: process.env.EMAIL_PASS || 'your-app-password'     // Replace with your app password
    }
  });
};

// Send coding reminder email
const sendCodingReminder = async (userEmail, userName, reminderType, projectName = '') => {
  try {
    const transporter = createTransporter();
    
    let subject, htmlContent;
    
    switch (reminderType) {
      case 'daily':
        subject = '🚀 Daily Coding Reminder from Coby';
        htmlContent = `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2563eb;">Hello ${userName}! 👋</h2>
            <p>It's time for your daily coding session with Coby!</p>
            <p>Remember: Consistency is key to becoming a better developer. Even 30 minutes of coding can make a huge difference.</p>
            <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #1e40af;">💡 Today's Coding Tip:</h3>
              <p>Try writing clean, readable code. Your future self will thank you!</p>
            </div>
            <a href="http://localhost:5173/coding-space" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Start Coding Now</a>
            <p style="margin-top: 20px; color: #6b7280; font-size: 14px;">
              Happy coding!<br>
              - Coby, Your AI Companion
            </p>
          </div>
        `;
        break;
        
      case 'project':
        subject = `📋 Project Reminder: ${projectName}`;
        htmlContent = `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2563eb;">Project Update Reminder 📋</h2>
            <p>Hi ${userName},</p>
            <p>Don't forget to work on your project: <strong>${projectName}</strong></p>
            <p>Keep the momentum going! Every line of code brings you closer to completion.</p>
            <div style="background-color: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2563eb;">
              <h3 style="color: #1e40af; margin-top: 0;">🎯 Next Steps:</h3>
              <ul>
                <li>Review your current progress</li>
                <li>Identify the next feature to implement</li>
                <li>Set a small, achievable goal for today</li>
              </ul>
            </div>
            <a href="http://localhost:5173/coding-space" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Continue Project</a>
            <p style="margin-top: 20px; color: #6b7280; font-size: 14px;">
              You've got this!<br>
              - Coby
            </p>
          </div>
        `;
        break;
        
      case 'weekly':
        subject = '📊 Weekly Coding Progress Summary';
        htmlContent = `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2563eb;">Weekly Coding Summary 📊</h2>
            <p>Hello ${userName},</p>
            <p>Here's your weekly coding progress summary from Coby!</p>
            <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #1e40af;">This Week's Achievements:</h3>
              <ul>
                <li>Maintained consistent coding practice</li>
                <li>Explored new concepts and technologies</li>
                <li>Made progress on your projects</li>
              </ul>
            </div>
            <div style="background-color: #fef3c7; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #92400e;">💪 Next Week's Goals:</h3>
              <p>Set achievable goals and continue your coding journey!</p>
            </div>
            <a href="http://localhost:5173/coding-space" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Plan Next Week</a>
            <p style="margin-top: 20px; color: #6b7280; font-size: 14px;">
              Keep up the great work!<br>
              - Coby
            </p>
          </div>
        `;
        break;
        
      default:
        subject = '🤖 Coding Reminder from Coby';
        htmlContent = `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2563eb;">Coding Reminder 🤖</h2>
            <p>Hi ${userName},</p>
            <p>This is your friendly reminder to continue your coding journey!</p>
            <a href="http://localhost:5173/coding-space" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Start Coding</a>
            <p style="margin-top: 20px; color: #6b7280; font-size: 14px;">
              Happy coding!<br>
              - Coby
            </p>
          </div>
        `;
    }

    const mailOptions = {
      from: process.env.EMAIL_USER || 'your-email@gmail.com',
      to: userEmail,
      subject: subject,
      html: htmlContent
    };

    const result = await transporter.sendMail(mailOptions);
    console.log('Email sent successfully:', result.messageId);
    return { success: true, messageId: result.messageId };
    
  } catch (error) {
    console.error('Error sending email:', error);
    return { success: false, error: error.message };
  }
};

// Send welcome email for new users
const sendWelcomeEmail = async (userEmail, userName) => {
  try {
    const transporter = createTransporter();
    
    const mailOptions = {
      from: process.env.EMAIL_USER || 'your-email@gmail.com',
      to: userEmail,
      subject: '🎉 Welcome to Coby - Your AI Coding Companion!',
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <h1 style="color: #2563eb; text-align: center;">Welcome to Coby! 🎉</h1>
          <p>Hi ${userName},</p>
          <p>Welcome to Coby, your AI-powered companion for growth and coding excellence!</p>
          
          <div style="background-color: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #1e40af; margin-top: 0;">🚀 What you can do with Coby:</h3>
            <ul>
              <li><strong>Coding Space:</strong> Build and manage your projects</li>
              <li><strong>Smart Reminders:</strong> Stay consistent with your coding practice</li>
              <li><strong>AI Support:</strong> Get help and guidance whenever you need it</li>
              <li><strong>Community:</strong> Connect with other developers</li>
            </ul>
          </div>
          
          <div style="text-align: center; margin: 30px 0;">
            <a href="http://localhost:5173/coding-space" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Explore Coding Space</a>
          </div>
          
          <p style="color: #6b7280; font-size: 14px;">
            Ready to start your coding journey? I'm here to help you every step of the way!<br><br>
            Best regards,<br>
            Coby - Your AI Companion
          </p>
        </div>
      `
    };

    const result = await transporter.sendMail(mailOptions);
    console.log('Welcome email sent successfully:', result.messageId);
    return { success: true, messageId: result.messageId };
    
  } catch (error) {
    console.error('Error sending welcome email:', error);
    return { success: false, error: error.message };
  }
};

module.exports = {
  sendCodingReminder,
  sendWelcomeEmail
};