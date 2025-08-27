import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Notifications from './pages/Notifications/Notifications';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import CodingSpace from './pages/CodingSpace/CodingSpace';
import Roundtable from './pages/Roundtable/Roundtable';
import MindSpace from './pages/MindSpace/MindSpace';
import SpeakUp from './pages/SpeakUp/SpeakUp';
import SafeLink from './pages/SafeLink/SafeLink';
import Reminders from './pages/Reminders/Reminders';
import Profile from './pages/Profile/Profile';
import Settings from './pages/Settings/Settings';
import Landing from './pages/Landing/Landing';
import Login from './pages/Login/Login';
import Signup from './pages/Signup/Signup';
import ForgotPassword from './pages/ForgotPassword/ForgotPassword';
import ResetPassword from './pages/ResetPassword/ResetPassword';
import AuthCallback from './pages/AuthCallback/AuthCallback';
import ProtectedRoute from './components/ProtectedRoute';
import PublicRoute from './components/PublicRoute';
import { ThemeProvider } from './contexts/ThemeContext';
import './App.css';

const App = () => {
  return (
    <ThemeProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            }
          />
          <Route path="/signup" element={
              <PublicRoute>
                <Signup />
              </PublicRoute>
            }
          />
          <Route path="/forgot-password" element={
              <PublicRoute>
                <ForgotPassword />
              </PublicRoute>
            }
          />
          <Route path="/reset-password" element={
              <PublicRoute>
                <ResetPassword />
              </PublicRoute>
            }
          />
          <Route path="/auth/callback" element={<AuthCallback />} />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="coding-space" element={<CodingSpace />} />
            <Route path="roundtable" element={<Roundtable />} />
            <Route path="mind-space" element={<MindSpace />} />
            <Route path="speak-up" element={<SpeakUp />} />
            <Route path="safe-link" element={<SafeLink />} />
            <Route path="reminders" element={<Reminders />} />
            <Route path="profile" element={<Profile />} />
            <Route path="settings" element={<Settings />} />
            <Route path="notifications" element={<Notifications />} />
          </Route>

          {/* Fallback route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;
