import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Bot, CheckCircle, AlertCircle } from 'lucide-react';
import './AuthCallback.css';

const AuthCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('loading'); // 'loading', 'success', 'error'
  const [message, setMessage] = useState('');

  useEffect(() => {
    const handleCallback = () => {
      const token = searchParams.get('token');
      const user = searchParams.get('user');
      const error = searchParams.get('error');

      if (error) {
        // Handle error cases
        let errorMessage = '';
        switch (error) {
          case 'oauth_failed':
            errorMessage = 'Google authentication failed. Please try again.';
            break;
          case 'registration_failed':
            errorMessage = 'Failed to create account. Please try again or contact support.';
            break;
          default:
            errorMessage = 'Authentication failed. Please try again.';
        }
        
        setStatus('error');
        setMessage(errorMessage);
        
        // Redirect to login after showing error
        setTimeout(() => {
          navigate('/login', { 
            state: { 
              error: errorMessage 
            } 
          });
        }, 3000);
        
      } else if (token && user) {
        // Success case
        setStatus('success');
        setMessage(`Welcome, ${decodeURIComponent(user)}!`);
        
        // Store token and user data
        localStorage.setItem('token', token);
        localStorage.setItem('isAuthenticated', 'true');
        
        // Get user profile to store complete user data
        const getUserProfile = async () => {
          try {
            const { default: ApiService } = await import('../../services/api');
            const response = await ApiService.getProfile();
            
            if (response.success) {
              localStorage.setItem('user', JSON.stringify(response.user));
            }
          } catch (err) {
            console.error('Failed to get user profile:', err);
          }
        };
        
        getUserProfile();
        
        // Redirect to dashboard
        setTimeout(() => {
          navigate('/dashboard');
        }, 2000);
        
      } else {
        // No token or unexpected state
        setStatus('error');
        setMessage('Invalid authentication response. Please try again.');
        
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  const getContent = () => {
    switch (status) {
      case 'loading':
        return {
          icon: <div className="loading-spinner"><div className="spinner"></div></div>,
          title: 'Completing Sign In...',
          message: 'Please wait while we complete your authentication.',
          className: 'loading'
        };
      case 'success':
        return {
          icon: <CheckCircle size={48} />,
          title: 'Sign In Successful!',
          message,
          className: 'success'
        };
      case 'error':
        return {
          icon: <AlertCircle size={48} />,
          title: 'Sign In Failed',
          message,
          className: 'error'
        };
      default:
        return {
          icon: <div className="loading-spinner"><div className="spinner"></div></div>,
          title: 'Processing...',
          message: 'Please wait...',
          className: 'loading'
        };
    }
  };

  const content = getContent();

  return (
    <div className="auth-callback-container">
      <div className={`auth-callback-card ${content.className}`}>
        <div className="auth-callback-header">
          <div className="logo">
            <Bot className="logo-icon" />
            <span className="logo-text">Cally</span>
          </div>
          
          <div className={`status-icon ${content.className}`}>
            {content.icon}
          </div>
          
          <h1>{content.title}</h1>
          <p>{content.message}</p>
          
          {status === 'success' && (
            <p className="redirect-message">
              Redirecting you to your dashboard...
            </p>
          )}
          
          {status === 'error' && (
            <p className="redirect-message">
              Redirecting you back to sign in...
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthCallback;