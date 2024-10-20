// src/components/Header.js
import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const Header = () => {
  const location = useLocation();

  // Exclude the header from these paths
  const excludedPaths = ["/signup", "/login"];
  const showHeader = !excludedPaths.includes(location.pathname);

  // Show the login button only on the home page and not on the login screen
  const showLoginButton = location.pathname === "/";

  // If the header shouldn't be shown, return null
  if (!showHeader) return null;

  return (
    <header className="flex justify-between p-4 bg-gray-800 text-white">
      <h1 className="text-xl">Bull Rider</h1>
      {/* Only show the login button on the home page */}
      {showLoginButton && (
        <Link to="/login">
          <button className="bg-discord-purple px-4 py-2 rounded-md hover:bg-discord-blue">
            Login
          </button>
        </Link>
      )}
    </header>
  );
};

export default Header;
