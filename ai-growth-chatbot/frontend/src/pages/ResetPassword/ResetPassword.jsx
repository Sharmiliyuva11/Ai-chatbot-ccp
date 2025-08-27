import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { Eye, EyeOff, Lock, Bot, CheckCircle, AlertCircle } from 'lucide-react';
import './ResetPassword.css';

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');

  const [formData, setFormData] = useState({
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isTokenValid, setIsTokenValid] = useState(null);
  const [error, setError] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);

  useEffect(() => {
    if (!token) {
      setError('Invalid reset link. Please request a new password reset.');
      setIsTokenValid(false);
      return;
    }

    // Verify token validity
    const verifyToken = async () => {
      try {
        const { default: ApiService } = await import('../../services/api');
        const response = await ApiService.verifyResetToken({ token });
        
        if (response.success) {
          setIsTokenValid(true);
        } else {
          setError('This reset link has expired or is invalid. Please request a new password reset.');
          setIsTokenValid(false);
        }
      } catch (err) {
        console.error('Token verification error:', err);
        setError('Failed to verify reset link. Please try again.');
        setIsTokenValid(false);
      }
    };

    verifyToken();
  }, [token]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const validateForm = () => {
    if (!formData.password.trim()) {
      setError('Password is required');
      return false;
    }
    if (formData.password.length < 3) {
      setError('Password must be at least 3 characters long');
      return false;
    }
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const { default: ApiService } = await import('../../services/api');
      
      const response = await ApiService.resetPassword({
        token,
        password: formData.password
      });

      if (response.success) {
        setIsSuccess(true);
        // Redirect to login after success
        setTimeout(() => {
          navigate('/login', { 
            state: { 
              message: 'Password reset successful! Please sign in with your new password.' 
            } 
          });
        }, 3000);
      } else {
        setError(response.message || 'Failed to reset password');
      }
    } catch (err) {
      console.error('Password reset error:', err);
      setError(err.message || 'Failed to reset password. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Show loading state while verifying token
  if (isTokenValid === null) {
    return (
      <div className="reset-password-container">
        <div className="reset-password-card">
          <div className="reset-password-header">
            <div className="logo">
              <Bot className="logo-icon" />
              <span className="logo-text">Coby</span>
            </div>
            <div className="loading-spinner">
              <div className="spinner"></div>
            </div>
            <p>Verifying reset link...</p>
          </div>
        </div>
      </div>
    );
  }

  // Show error if token is invalid
  if (isTokenValid === false) {
    return (
      <div className="reset-password-container">
        <div className="reset-password-card error-card">
          <div className="reset-password-header">
            <div className="logo">
              <Bot className="logo-icon" />
              <span className="logo-text">Coby</span>
            </div>
            <div className="error-icon">
              <AlertCircle size={48} />
            </div>
            <h1>Invalid Reset Link</h1>
            <p>{error}</p>
          </div>
          <div className="error-actions">
            <Link to="/forgot-password" className="retry-btn">
              Request New Reset Link
            </Link>
            <Link to="/login" className="back-link">
              Back to Sign In
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Show success message
  if (isSuccess) {
    return (
      <div className="reset-password-container">
        <div className="reset-password-card success-card">
          <div className="reset-password-header">
            <div className="logo">
              <Bot className="logo-icon" />
              <span className="logo-text">Coby</span>
            </div>
            <div className="success-icon">
              <CheckCircle size={48} />
            </div>
            <h1>Password Reset Successful!</h1>
            <p>Your password has been successfully reset. You can now sign in with your new password.</p>
          </div>
          <div className="success-content">
            <p>Redirecting you to the sign-in page...</p>
            <Link to="/login" className="login-now-btn">
              Sign In Now
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Show password reset form
  return (
    <div className="reset-password-container">
      <div className="reset-password-card">
        <div className="reset-password-header">
          <div className="logo">
            <Bot className="logo-icon" />
              <span className="logo-text">Coby</span>
          </div>
          <h1>Reset Your Password</h1>
          <p>Enter your new password below</p>
        </div>

        <form onSubmit={handleSubmit} className="reset-password-form">
          {error && (
            <div className="error-message">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="password">New Password</label>
            <div className="input-container">
              <Lock className="input-icon" />
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your new password"
                required
                autoComplete="new-password"
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff /> : <Eye />}
              </button>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm New Password</label>
            <div className="input-container">
              <Lock className="input-icon" />
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="Confirm your new password"
                required
                autoComplete="new-password"
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              >
                {showConfirmPassword ? <EyeOff /> : <Eye />}
              </button>
            </div>
          </div>

          <div className="password-requirements">
            <p>Password requirements:</p>
            <ul>
              <li className={formData.password.length >= 3 ? 'valid' : 'invalid'}>
                At least 3 characters long
              </li>
              <li className={formData.password === formData.confirmPassword && formData.password ? 'valid' : 'invalid'}>
                Passwords match
              </li>
            </ul>
          </div>

          <button
            type="submit"
            className={`reset-btn ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? 'Resetting Password...' : 'Reset Password'}
          </button>
        </form>

        <div className="reset-password-footer">
          <Link to="/login" className="back-link">
            Remember your password? Sign In
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;