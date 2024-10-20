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
    navigate("/contacts");
  };

  return (
    <div className="profile-container min-h-screen flex flex-col items-center justify-center bg-animated-gradient text-white p-8">
      <div className="w-full max-w-2xl bg-black bg-opacity-80 p-8 rounded-lg shadow-2xl transform transition duration-500 hover:scale-105">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-extrabold animate-fade-in">Welcome, User!</h1>
            <p className="text-lg mt-2 text-gray-400">Token Count: {tokenCount}</p>
          </div>
          <div className="flex space-x-4">
            <button
              onClick={handleNavigateToContacts}
              className="bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-700 hover:to-blue-900 px-4 py-2 rounded transition duration-300 shadow-lg"
            >
              Contacts
            </button>
            <button
              onClick={handleSignOut}
              className="bg-gradient-to-r from-red-500 to-red-700 hover:from-red-700 hover:to-red-900 px-4 py-2 rounded transition duration-300 shadow-lg"
            >
              Sign Out
            </button>
          </div>
        </div>

        <div className="flex justify-center mb-8">
          <button className="bg-gradient-to-r from-green-500 to-green-700 hover:from-green-700 hover:to-green-900 px-6 py-3 rounded-full shadow-xl transition duration-300 transform hover:scale-110 animate-fade-in">
            PayVoice
          </button>
        </div>

        <div className="transaction-history bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-4 animate-fade-in">Transaction History</h2>
          <table className="w-full text-left animate-fade-in">
            <thead>
              <tr className="border-b border-gray-600">
                <th className="py-2">Date</th>
                <th className="py-2">Action</th>
                <th className="py-2">Amount</th>
                <th className="py-2">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-gray-600 hover:bg-gray-700 transition duration-300">
                <td className="py-2">10/19/2024</td>
                <td className="py-2">Sent</td>
                <td className="py-2">50 Tokens</td>
                <td className="py-2 text-green-400">Completed</td>
              </tr>
              <tr className="border-b border-gray-600 hover:bg-gray-700 transition duration-300">
                <td className="py-2">10/18/2024</td>
                <td className="py-2">Received</td>
                <td className="py-2">30 Tokens</td>
                <td className="py-2 text-green-400">Completed</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Profile;
