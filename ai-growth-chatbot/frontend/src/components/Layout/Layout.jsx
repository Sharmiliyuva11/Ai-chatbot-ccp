import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../Sidebar/Sidebar';
import { useTheme } from '../../contexts/useTheme';
import './Layout.css';

const Layout = () => {
  const { theme } = useTheme();

  return (
    <div className={`layout ${theme}`}>
      <Sidebar />
      <div className="main-content">
        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;