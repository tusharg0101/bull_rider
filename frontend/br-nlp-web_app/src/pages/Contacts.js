// src/pages/Contacts.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Contacts.css"; // Import CSS for styling

const Contacts = () => {
  const navigate = useNavigate();
  
  // State to manage contacts and form inputs
  const [contacts, setContacts] = useState([
    { alias: "Friend 1", passwordId: "pass-1234" },
    { alias: "Friend 2", passwordId: "pass-5678" },
    { alias: "Friend 3", passwordId: "pass-9101" },
    { alias: "Friend 4", passwordId: "pass-1121" },
  ]);
  const [newAlias, setNewAlias] = useState("");
  const [newPasswordId, setNewPasswordId] = useState("");

  // Handle adding a new contact
  const handleAddContact = (e) => {
    e.preventDefault();
    if (newAlias && newPasswordId) {
      const newContact = { alias: newAlias, passwordId: newPasswordId };
      setContacts([...contacts, newContact]);
      setNewAlias("");
      setNewPasswordId("");
    }
  };

  // Handle removing a contact
  const handleRemoveContact = (index) => {
    const updatedContacts = contacts.filter((_, i) => i !== index);
    setContacts(updatedContacts);
  };

  return (
    <div className="contacts-container bg-gradient-to-r from-gray-900 via-gray-800 to-gray-700 text-white min-h-screen p-8">
      {/* Navigation Button */}
      <div className="flex justify-end mb-4">
        <button
          onClick={() => navigate("/profile")}
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-all duration-300"
        >
          Profile
        </button>
      </div>

      {/* Add Contact Form */}
      <div className="bg-gray-800 p-4 rounded-lg mb-6 shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Add New Contact</h2>
        <form onSubmit={handleAddContact} className="flex space-x-4 mb-4">
          <input
            type="text"
            placeholder="Alias"
            value={newAlias}
            onChange={(e) => setNewAlias(e.target.value)}
            className="bg-gray-700 text-white px-4 py-2 rounded focus:outline-none"
          />
          <input
            type="text"
            placeholder="Password ID"
            value={newPasswordId}
            onChange={(e) => setNewPasswordId(e.target.value)}
            className="bg-gray-700 text-white px-4 py-2 rounded focus:outline-none"
          />
          <button
            type="submit"
            className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded transition-all duration-300"
          >
            Add
          </button>
        </form>
      </div>

      {/* Contacts List */}
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Contacts List</h2>
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-gray-600">
              <th className="py-2">Alias</th>
              <th className="py-2">Password ID</th>
              <th className="py-2">Remove</th>
            </tr>
          </thead>
          <tbody>
            {contacts.map((contact, index) => (
              <tr key={index} className="border-b border-gray-600 hover:bg-gray-700 transition duration-300">
                <td className="py-2">{contact.alias}</td>
                <td className="py-2">{contact.passwordId}</td>
                <td className="py-2">
                  <button
                    onClick={() => handleRemoveContact(index)}
                    className="text-red-500 hover:text-red-700 transition duration-300"
                  >
                    &#10006; {/* Unicode for a red X */}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Contacts;
