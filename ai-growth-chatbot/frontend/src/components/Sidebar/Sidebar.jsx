import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Code,
  Users, 
  Brain, 
  MessageSquare, 
  Shield, 
  User, 
  Settings, 
  LogOut,
  Bot,
  Calendar,
  Bell,
  Sun, // Add Sun icon
  Moon // Add Moon icon
} from 'lucide-react';
import { useTheme } from '../../contexts/useTheme'; // Import useTheme
import './Sidebar.css';

const Sidebar = () => {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme(); // Use theme context

  const handleLogout = () => {
    // Clear authentication
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('user');
    console.log('Logging out...');
    navigate('/login');
  };

  const menuItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard', exact: true },
    { path: '/dashboard/coding-space', icon: Code, label: 'Coding Space' },
    { path: '/dashboard/roundtable', icon: Users, label: 'Roundtable' },
    { path: '/dashboard/mind-space', icon: Brain, label: 'Mind Space' },
    { path: '/dashboard/speak-up', icon: MessageSquare, label: 'Speak Up' },
    { path: '/dashboard/safe-link', icon: Shield, label: 'Safe Link' },
    { path: '/dashboard/reminders', icon: Bell, label: 'Reminders' },
    { path: '/dashboard/profile', icon: User, label: 'Profile' },
    { path: '/dashboard/settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <div className={`sidebar ${theme}`}>
      <div className="sidebar-header">
        <div className="logo">
          <Bot className="logo-icon" />
          <span className="logo-text">Coby</span>
          <span className="logo-subtitle">AI Assistant</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <ul className="nav-list">
          {menuItems.map((item) => (
            <li key={item.path} className="nav-item">
              <NavLink
                to={item.path}
                className={({ isActive }) => 
                  `nav-link ${isActive ? 'active' : ''}`
                }
                end={item.exact}
              >
                <item.icon className="nav-icon" />
                <span className="nav-label">{item.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="sidebar-footer">
        <button className="theme-toggle-btn" onClick={toggleTheme}>
          {theme === 'light' ? <Moon className="theme-icon" /> : <Sun className="theme-icon" />}
          <span className="nav-label">{theme === 'light' ? 'Dark Mode' : 'Light Mode'}</span>
        </button>
        <button className="logout-btn" onClick={handleLogout}>
          <LogOut className="nav-icon" />
          <span className="nav-label">Logout</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;