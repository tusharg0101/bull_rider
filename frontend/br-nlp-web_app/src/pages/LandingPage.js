// src/pages/LandingPage.js
import React, { useState, useRef } from "react";
import RecordRTC from "recordrtc";
import { useNavigate } from "react-router-dom";
import "./LandingPage.css"; // Import CSS for custom styling

const LandingPage = () => {
  const [password, setPassword] = useState("");
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const recorderRef = useRef(null);
  const navigate = useNavigate();

  // Handle password input change
  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  // Start recording voice input
  const startRecording = async () => {
    setRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    recorderRef.current = new RecordRTC(stream, {
      type: "audio",
      mimeType: "audio/wav",
      recorderType: RecordRTC.StereoAudioRecorder,
      desiredSampRate: 16000,
    });

    recorderRef.current.startRecording();
  };

  // Stop recording and store the audio blob
  const stopRecording = () => {
    recorderRef.current.stopRecording(() => {
      const blob = recorderRef.current.getBlob();
      setAudioBlob(blob);
      setRecording(false);
    });
  };

  // Handle form submission for login
  const handleLogin = async () => {
    if (!audioBlob || !password) {
      alert("Please enter a password and complete the voice authentication.");
      return;
    }

    // Create a FormData object to send the password and audio file
    const formData = new FormData();
    formData.append("password", password);
    formData.append("voice", audioBlob, "voice_login.wav");

    try {
      const response = await fetch(
        "http://localhost:8084/api/voice-auth/login",
        {
          method: "POST",
          body: formData,
        }
      );

      if (response.ok) {
        const data = await response.json();
        console.log(data.message);
        navigate("/profile"); // Redirect to profile on successful login
      } else {
        const errorData = await response.json();
        alert(`Login failed: ${errorData.detail}`);
      }
    } catch (error) {
      console.error("Error during login:", error);
      alert("An error occurred while logging in.");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-login-gradient text-white">
      <div className="max-w-md w-full bg-gray-800 p-8 rounded-lg shadow-lg transform hover:scale-105 transition duration-500 ease-in-out">
        <h1 className="text-4xl font-bold text-center mb-8 text-discord-purple">
          Bull Rider Login
        </h1>
        <p className="text-center text-gray-300 mb-6">
          Please log in to continue.
        </p>
        <h1 className="text-4xl font-bold text-center mb-8 text-discord-purple">
          Sign In
        </h1>
        <div className="mb-6">
          <input
            type="password"
            value={password}
            onChange={handlePasswordChange}
            className="w-full px-4 py-2 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-discord-purple"
            placeholder="Enter your password"
          />
        </div>
        <div className="flex justify-between">
          <button
            onClick={recording ? stopRecording : startRecording}
            className={`w-5/12 py-2 ${
              recording ? "bg-red-600" : "bg-blue-600 hover:bg-blue-700"
            } text-white rounded-md`}
          >
            {recording ? "Stop Recording" : "Start Recording"}
          </button>
          <button
            onClick={handleLogin}
            className="w-5/12 py-2 bg-discord-purple text-white rounded-md hover:bg-discord-blue transition duration-300"
          >
            authVoice
          </button>
        </div>
        <p className="mt-4 text-center text-gray-400">
          When you are ready, click the button and say "Log me in" to
          authenticate.
        </p>
      </div>
    </div>
  );
};

export default LandingPage;
