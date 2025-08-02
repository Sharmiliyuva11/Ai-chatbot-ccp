import React, { useState } from 'react';
import { 
  Settings as SettingsIcon, 
  Bell, 
  Shield, 
  Moon, 
  Sun, 
  Globe, 
  Smartphone,
  Mail,
  Lock,
  Eye,
  EyeOff,
  Save,
  Trash2,
  Download,
  Upload
} from 'lucide-react';
import './Settings.css';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [showPassword, setShowPassword] = useState(false);
  
  const [settings, setSettings] = useState({
    // General Settings
    theme: 'light',
    language: 'en',
    timezone: 'America/New_York',
    
    // Notification Settings
    emailNotifications: true,
    pushNotifications: true,
    smsNotifications: false,
    reminderNotifications: true,
    sessionReminders: true,
    moodReminders: true,
    
    // Privacy Settings
    profileVisibility: 'private',
    dataSharing: false,
    analyticsOptIn: true,
    locationTracking: false,
    
    // Security Settings
    twoFactorAuth: false,
    sessionTimeout: 30,
    loginAlerts: true
  });

  const tabs = [
    { id: 'general', name: 'General', icon: SettingsIcon },
    { id: 'notifications', name: 'Notifications', icon: Bell },
    { id: 'privacy', name: 'Privacy', icon: Shield },
    { id: 'security', name: 'Security', icon: Lock },
    { id: 'data', name: 'Data & Export', icon: Download }
  ];

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSaveSettings = () => {
    // Save settings logic here
    console.log('Saving settings:', settings);
    // Show success message
  };

  const handleExportData = () => {
    // Export data logic here
    console.log('Exporting user data...');
  };

  const handleDeleteAccount = () => {
    // Delete account logic here
    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      console.log('Deleting account...');
    }
  };

  return (
    <div className="settings">
      <div className="settings-header">
        <h1>Settings</h1>
        <p>Manage your account preferences and privacy settings</p>
      </div>

      <div className="settings-container">
        <div className="settings-sidebar">
          <nav className="settings-nav">
            {tabs.map(tab => (
              <button
                key={tab.id}
                className={`nav-item ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                <tab.icon className="nav-icon" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>

        <div className="settings-content">
          {activeTab === 'general' && (
            <div className="settings-section">
              <h2>General Settings</h2>
              
              <div className="setting-group">
                <h3>Appearance</h3>
                <div className="setting-item">
                  <div className="setting-info">
                    <label>Theme</label>
                    <p>Choose your preferred color scheme</p>
                  </div>
                  <div className="theme-selector">
                    <button 
                      className={`theme-btn ${settings.theme === 'light' ? 'active' : ''}`}
                      onClick={() => handleSettingChange('theme', 'light')}
                    >
                      <Sun className="theme-icon" />
                      Light
                    </button>
                    <button 
                      className={`theme-btn ${settings.theme === 'dark' ? 'active' : ''}`}
                      onClick={() => handleSettingChange('theme', 'dark')}
                    >
                      <Moon className="theme-icon" />
                      Dark
                    </button>
                  </div>
                </div>
              </div>

              <div className="setting-group">
                <h3>Localization</h3>
                <div className="setting-item">
                  <div className="setting-info">
                    <label>Language</label>
                    <p>Select your preferred language</p>
                  </div>
                  <select 
                    value={settings.language}
                    onChange={(e) => handleSettingChange('language', e.target.value)}
                  >
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                    <option value="de">German</option>
                  </select>
                </div>

                <div className="setting-item">
                  <div className="setting-info">
                    <label>Timezone</label>
                    <p>Your local timezone for scheduling</p>
                  </div>
                  <select 
                    value={settings.timezone}
                    onChange={(e) => handleSettingChange('timezone', e.target.value)}
                  >
                    <option value="America/New_York">Eastern Time</option>
                    <option value="America/Chicago">Central Time</option>
                    <option value="America/Denver">Mountain Time</option>
                    <option value="America/Los_Angeles">Pacific Time</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="settings-section">
              <h2>Notification Settings</h2>
              
              <div className="setting-group">
                <h3>Communication Preferences</h3>
                <div className="setting-item">
                  <div className="setting-info">
                    <Mail className="setting-icon" />
                    <div>
                      <label>Email Notifications</label>
                      <p>Receive updates and reminders via email</p>
                    </div>
                  </div>
                  <label className="toggle-switch">
                    <input 
                      type="checkbox" 
                      checked={settings.emailNotifications}
                      onChange={(e) => handleSettingChange('emailNotifications', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <div className="setting-info">
                    <Smartphone className="setting-icon" />
                    <div>
                      <label>Push Notifications</label>
                      <p>Get instant notifications on your device</p>
                    </div>
                  </div>
                  <label className="toggle-switch">
                    <input 
                      type="checkbox" 
                      checked={settings.pushNotifications}
                      onChange={(e) => handleSettingChange('pushNotifications', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <div className="setting-info">
                    <Bell className="setting-icon" />
                    <div>
                      <label>SMS Notifications</label>
                      <p>Receive text messages for important updates</p>
                    </div>
                  </div>
                  <label className="toggle-switch">
                    <input 
                      type="checkbox" 
                      checked={settings.smsNotifications}
                      onChange={(e) => handleSettingChange('smsNotifications', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>
              </div>

              <div className="setting-group">
                <h3>Reminder Settings</h3>
                <div className="setting-item">
                  <div className="setting-info">
                    <label>Session Reminders</label>
                    <p>Get notified about upcoming therapy sessions</p>
                  </div>
                  <label className="toggle-switch">
                    <input 
                      type="checkbox" 
                      checked={settings.sessionReminders}
                      onChange={(e) => handleSettingChange('sessionReminders', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <div className="setting-info">
                    <label>Mood Check-in Reminders</label>
                    <p>Daily reminders to log your mood</p>
                  </div>
                  <label className="toggle-switch">
                    <input 
                      type="checkbox" 
                      checked={settings.moodReminders}
                      onChange={(e) => handleSettingChange('moodReminders', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'privacy' && (
            <div className="settings-section">
              <h2>Privacy Settings</h2>
              
              <div className="setting-group">
                <h3>Profile & Data</h3>
                <div className="setting-item">
                  <div className="setting-info">
                    <label>Profile Visibility</label>
                    <p>Control who can see your profile information</p>
                  </div>
                  <select 
                    value={settings.profileVisibility}
                    onChange={(e) => handleSettingChange('profileVisibility', e.target.value)}
                  >
                    <option value="private">Private</option>
                    <option value="friends">Friends Only</option>
                    <option value="public">Public</option>
                  </select>
                </div>

                <div className="setting-item">
                  <div className="setting-info">
                    <label>Data Sharing</label>
                    <p>Allow sharing anonymized data for research</p>
                  </div>
                  <label className="toggle-switch">
                    <input 
                      type="checkbox" 
                      checked={settings.dataSharing}
                      onChange={(e) => handleSettingChange('dataSharing', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <div className="setting-info">
                    <label>Analytics</label>
                    <p>Help improve our service with usage analytics</p>
                  </div>
                  <label className="toggle-switch">
                    <input 
                      type="checkbox" 
                      checked={settings.analyticsOptIn}
                      onChange={(e) => handleSettingChange('analyticsOptIn', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <div className="setting-info">
                    <label>Location Tracking</label>
                    <p>Allow location-based features and recommendations</p>
                  </div>
                  <label className="toggle-switch">
                    <input 
                      type="checkbox" 
                      checked={settings.locationTracking}
                      onChange={(e) => handleSettingChange('locationTracking', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="settings-section">
              <h2>Security Settings</h2>
              
              <div className="setting-group">
                <h3>Account Security</h3>
                <div className="setting-item">
                  <div className="setting-info">
                    <label>Change Password</label>
                    <p>Update your account password</p>
                  </div>
                  <button className="secondary-btn">Change Password</button>
                </div>

                <div className="setting-item">
                  <div className="setting-info">
                    <label>Two-Factor Authentication</label>
                    <p>Add an extra layer of security to your account</p>
                  </div>
                  <label className="toggle-switch">
                    <input 
                      type="checkbox" 
                      checked={settings.twoFactorAuth}
                      onChange={(e) => handleSettingChange('twoFactorAuth', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <div className="setting-info">
                    <label>Session Timeout</label>
                    <p>Automatically log out after inactivity</p>
                  </div>
                  <select 
                    value={settings.sessionTimeout}
                    onChange={(e) => handleSettingChange('sessionTimeout', parseInt(e.target.value))}
                  >
                    <option value={15}>15 minutes</option>
                    <option value={30}>30 minutes</option>
                    <option value={60}>1 hour</option>
                    <option value={120}>2 hours</option>
                    <option value={0}>Never</option>
                  </select>
                </div>

                <div className="setting-item">
                  <div className="setting-info">
                    <label>Login Alerts</label>
                    <p>Get notified of new login attempts</p>
                  </div>
                  <label className="toggle-switch">
                    <input 
                      type="checkbox" 
                      checked={settings.loginAlerts}
                      onChange={(e) => handleSettingChange('loginAlerts', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'data' && (
            <div className="settings-section">
              <h2>Data & Export</h2>
              
              <div className="setting-group">
                <h3>Data Management</h3>
                <div className="setting-item">
                  <div className="setting-info">
                    <Download className="setting-icon" />
                    <div>
                      <label>Export Your Data</label>
                      <p>Download a copy of all your data</p>
                    </div>
                  </div>
                  <button className="secondary-btn" onClick={handleExportData}>
                    Export Data
                  </button>
                </div>

                <div className="setting-item">
                  <div className="setting-info">
                    <Upload className="setting-icon" />
                    <div>
                      <label>Import Data</label>
                      <p>Import data from another service</p>
                    </div>
                  </div>
                  <button className="secondary-btn">Import Data</button>
                </div>
              </div>

              <div className="setting-group danger-zone">
                <h3>Danger Zone</h3>
                <div className="setting-item">
                  <div className="setting-info">
                    <Trash2 className="setting-icon danger" />
                    <div>
                      <label>Delete Account</label>
                      <p>Permanently delete your account and all data</p>
                    </div>
                  </div>
                  <button className="danger-btn" onClick={handleDeleteAccount}>
                    Delete Account
                  </button>
                </div>
              </div>
            </div>
          )}

          <div className="settings-actions">
            <button className="primary-btn" onClick={handleSaveSettings}>
              <Save className="btn-icon" />
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;