import React, { useContext } from 'react';
import { Bell, Search, User, Sun, Moon } from 'lucide-react';
import { useTheme } from '../../contexts/useTheme';
import './Header.css';

const Header = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="header">
      <div className="header-left">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Welcome back! Here's your mental wellness overview for today.</p>
      </div>
      
      <div className="header-right">
        <div className="search-container">
          <Search className="search-icon" />
          <input 
            type="text" 
            placeholder="Search..." 
            className="search-input"
          />
        </div>
        
          <div className="header-actions">
            <button className="theme-toggle-btn" onClick={toggleTheme}>
              {theme === 'light' ? <Moon className="icon" /> : <Sun className="icon" />}
            </button>
            <Link to="/notifications" className="notification-btn">
              <Bell className="icon" />
              <span className="notification-badge">3</span>
            </Link>
            <Link to="/profile" className="user-profile">
              <img 
                src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face" 
                alt="User Avatar" 
                className="user-avatar"
              />
            </Link>
          </div>
      </div>
    </header>
  );
};

export default Header;