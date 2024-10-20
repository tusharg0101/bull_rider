// src/pages/LandingPage.js
import React, { useState } from "react";
import './LandingPage.css'; // Import CSS for custom styling

const LandingPage = () => {
  const [password, setPassword] = useState("");

  // Handle password input change
  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  // Handle form submission
  const handleAuthVoice = () => {
    console.log("authVoice button clicked");
    // Backend interaction to be implemented later
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-login-gradient text-white">
      <div className="max-w-md w-full bg-gray-800 p-8 rounded-lg shadow-lg transform hover:scale-105 transition duration-500 ease-in-out">
        <h1 className="text-4xl font-bold text-center mb-8 text-discord-purple">Sign In</h1>
        <div className="mb-6">
          <input
            type="password"
            value={password}
            onChange={handlePasswordChange}
            className="w-full px-4 py-2 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-discord-purple"
            placeholder="Enter your password"
          />
        </div>
        <button
          onClick={handleAuthVoice}
          className="w-full py-2 bg-discord-purple text-white rounded-md hover:bg-discord-blue transition duration-300"
        >
          authVoice
        </button>
        <p className="mt-4 text-center text-gray-400">
          When you are ready, click the button and say "Log me in" to authenticate.
        </p>
      </div>
    </div>
  );
};

export default LandingPage;
