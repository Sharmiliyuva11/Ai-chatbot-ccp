import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../Sidebar/Sidebar';
import './Layout.css';

const Layout = () => {
  return (
    <div className="layout">
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