import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, Bot, ArrowLeft, CheckCircle, AlertCircle } from 'lucide-react';
import './ForgotPassword.css';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email.trim()) {
      setError('Please enter your email address');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const { default: ApiService } = await import('../../services/api');
      
      const response = await ApiService.forgotPassword({ email: email.trim() });

      if (response.success) {
        setIsSuccess(true);
      } else {
        setError(response.message || 'Failed to send reset email');
      }
    } catch (err) {
      console.error('Forgot password error:', err);
      setError(err.message || 'Failed to send reset email. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <div className="forgot-password-container">
        <div className="forgot-password-card success-card">
          <div className="forgot-password-header">
            <div className="logo">
              <Bot className="logo-icon" />
              <span className="logo-text">Coby</span>
            </div>
            <div className="success-icon">
              <CheckCircle size={48} />
            </div>
            <h1>Check Your Email</h1>
            <p>
              We've sent a password reset link to <strong>{email}</strong>
            </p>
          </div>

          <div className="success-content">
            <div className="instructions">
              <h3>What to do next:</h3>
              <ol>
                <li>Check your email inbox</li>
                <li>Click the password reset link</li>
                <li>Create a new password</li>
                <li>Sign in with your new password</li>
              </ol>
            </div>

            <div className="help-text">
              <p>Didn't receive the email? Check your spam folder or try again with a different email address.</p>
            </div>

            <Link to="/login" className="back-to-login-btn">
              <ArrowLeft size={16} />
              Back to Sign In
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="forgot-password-container">
      <div className="forgot-password-card">
        <div className="forgot-password-header">
          <div className="logo">
            <Bot className="logo-icon" />
            <span className="logo-text">Coby</span>
          </div>
          <h1>Forgot Password?</h1>
          <p>No worries! Enter your email address and we'll send you a link to reset your password.</p>
        </div>

        <form onSubmit={handleSubmit} className="forgot-password-form">
          {error && (
            <div className="error-message">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <div className="input-container">
              <Mail className="input-icon" />
              <input
                type="email"
                id="email"
                name="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  setError('');
                }}
                placeholder="Enter your email address"
                required
                autoComplete="email"
              />
            </div>
          </div>

          <button
            type="submit"
            className={`reset-btn ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? 'Sending...' : 'Send Reset Link'}
          </button>
        </form>

        <div className="forgot-password-footer">
          <Link to="/login" className="back-link">
            <ArrowLeft size={16} />
            Back to Sign In
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;