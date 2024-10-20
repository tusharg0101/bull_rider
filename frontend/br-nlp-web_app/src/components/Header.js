// src/components/Header.js
import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
  const location = useLocation();

  // Exclude the header from these paths
  const excludedPaths = ["/signup", "/login"];
  const showHeader = !excludedPaths.includes(location.pathname);

  // If the header shouldn't be shown, return null
  if (!showHeader) return null;

  return (
    <header className="header flex justify-between items-center px-8 py-4">
      <div className="header-title text-xl font-bold">Bull Rider</div>
      <Link to="/login">
        <button className="bg-discord-purple px-4 py-2 rounded-md hover:bg-discord-blue">
          Login
        </button>
      </Link>
    </header>
  );
};

export default Header;
