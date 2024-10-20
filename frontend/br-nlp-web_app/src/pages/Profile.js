// src/pages/Profile.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './Profile.css';

const Profile = () => {
  const [tokenCount, setTokenCount] = useState(1000);
  const navigate = useNavigate();

  const handleSignOut = () => {
    navigate("/");
  };

  const handleNavigateToContacts = () => {
    navigate("/contacts"); // Navigate to the Contacts page
  };

  return (
    <div className="profile-container bg-gradient-to-r from-gray-900 via-gray-800 to-gray-700 text-white min-h-screen p-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Welcome, User!</h1>
          <p className="text-lg mt-2">Token Count: {tokenCount}</p>
        </div>
        <div className="flex space-x-4">
          <button 
            onClick={handleNavigateToContacts} 
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded"
          >
            Contacts
          </button>
          <button 
            onClick={handleSignOut} 
            className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded"
          >
            Sign Out
          </button>
        </div>
      </div>

      <div className="flex justify-center mb-8">
        <button className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-full mb-4 transition-all duration-300">PayVoice</button>
      </div>

      <div className="transaction-history bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Transaction History</h2>
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-gray-600">
              <th className="py-2">Date</th>
              <th className="py-2">Action</th>
              <th className="py-2">Amount</th>
              <th className="py-2">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-b border-gray-600">
              <td className="py-2">10/19/2024</td>
              <td className="py-2">Sent</td>
              <td className="py-2">50 Tokens</td>
              <td className="py-2 text-green-400">Completed</td>
            </tr>
            <tr className="border-b border-gray-600">
              <td className="py-2">10/18/2024</td>
              <td className="py-2">Received</td>
              <td className="py-2">30 Tokens</td>
              <td className="py-2 text-green-400">Completed</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Profile;
