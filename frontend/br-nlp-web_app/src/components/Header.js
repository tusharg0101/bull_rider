// Header.js

import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <nav className="bg-black bg-opacity-70 backdrop-blur-sm text-white p-4 shadow-lg fixed w-full top-0 z-50">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-500">
          Bull Rider
        </h1>
        <ul className="flex space-x-6">
          <li>
            <Link
              to="/login"
              className="hover:text-blue-400 text-lg transition duration-300"
            >
              Log In
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Header;
