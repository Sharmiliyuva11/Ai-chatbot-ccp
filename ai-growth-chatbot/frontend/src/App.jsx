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
import SimplePage from './pages/Static/SimplePage';
import './App.css';

const App = () => {
  return (
    <ThemeProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Landing />} />
          {/* Footer-linked public pages */}
          <Route path="/features" element={<SimplePage title="Features" subtitle="Explore what Coby offers."/>} />
          <Route path="/about" element={<SimplePage title="About" subtitle="Learn more about Coby.">Coby blends AI-assisted growth tools with wellness support and a helpful community.</SimplePage>} />
          <Route path="/testimonials" element={<SimplePage title="Testimonials" subtitle="What our users say."/>} />
          <Route path="/contact" element={<SimplePage title="Contact" subtitle="We’d love to hear from you.">Reach us at support@coby.app</SimplePage>} />
          <Route path="/community" element={<SimplePage title="Community" subtitle="Join discussions and events."/>} />
          <Route path="/help" element={<SimplePage title="Help Center" subtitle="Guides and FAQs to get you started."/>} />
          <Route path="/privacy" element={<SimplePage title="Privacy Policy" subtitle="Your privacy matters.">We respect your data and follow best practices to keep it safe.</SimplePage>} />
          <Route path="/terms" element={<SimplePage title="Terms of Service" subtitle="Please read carefully."/>} />
          <Route path="/security" element={<SimplePage title="Security" subtitle="How we keep things secure."/>} />
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
