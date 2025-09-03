import React from 'react';
import './SimplePage.css';

const SimplePage = ({ title, subtitle, children }) => {
  return (
    <div className="simple-page">
      <div className="container">
        <header className="simple-page-header">
          <h1>{title}</h1>
          {subtitle && <p>{subtitle}</p>}
        </header>
        <div className="simple-page-content">
          {children}
        </div>
      </div>
    </div>
  );
};

export default SimplePage;