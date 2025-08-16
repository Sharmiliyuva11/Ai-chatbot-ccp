import React from 'react';
import { Bell, Search, User } from 'lucide-react';
import './Header.css';

const Header = () => {
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
          <button className="notification-btn">
            <Bell className="icon" />
            <span className="notification-badge">3</span>
          </button>
          
          <div className="user-profile">
            <img 
              src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face" 
              alt="User Avatar" 
              className="user-avatar"
            />
            <div className="user-info">
              <span className="user-name">John Doe</span>
              <span className="user-role">Member</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;