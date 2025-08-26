import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import ApiService from '../services/api';

const ProtectedRoute = ({ children }) => {
  const [isChecking, setIsChecking] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      const authStatus = localStorage.getItem('isAuthenticated') === 'true';

      if (!token || !authStatus) {
        setIsAuthenticated(false);
        setIsChecking(false);
        return;
      }

      try {
        const response = await ApiService.getProfile();
        if (response.success) {
          setIsAuthenticated(true);
          localStorage.setItem('user', JSON.stringify(response.user));
        } else {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          localStorage.removeItem('isAuthenticated');
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('isAuthenticated');
        setIsAuthenticated(false);
      }
      setIsChecking(false);
    };

    checkAuth();
  }, []);

  if (isChecking) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      }}>
        <div style={{ 
          color: 'white', 
          fontSize: '18px',
          display: 'flex',
          alignItems: 'center',
          gap: '12px'
        }}>
          <div style={{
            width: '20px',
            height: '20px',
            border: '2px solid rgba(255,255,255,0.3)',
            borderTop: '2px solid white',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite'
          }}></div>
          Loading...
        </div>
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

export default ProtectedRoute;