import React from 'react';
import { Navigate } from 'react-router-dom';

const PublicRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

  return !isAuthenticated ? children : <Navigate to="/dashboard" replace />;
};

export default PublicRoute;