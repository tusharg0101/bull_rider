import React, { useState, useRef } from "react";
import axios from "axios";
import RecordRTC from "recordrtc";

const SignUp = () => {
  const [password, setPassword] = useState("");
  const [audioFiles, setAudioFiles] = useState([]);
  const [promptIndex, setPromptIndex] = useState(0);
  const [recording, setRecording] = useState(false);
  const recorderRef = useRef(null); // Reference to store the recorder instance

  const prompts = [
    "Say 'Log me in' for the first time",
    "Say 'Log me in' for the second time",
    "Say 'Log me in' one last time",
  ];

  // Handle password input
  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  // Start recording
  const startRecording = async () => {
    setRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // Initialize RecordRTC with WAV settings
    recorderRef.current = new RecordRTC(stream, {
      type: "audio",
      mimeType: "audio/wav",
      recorderType: RecordRTC.StereoAudioRecorder,
      desiredSampRate: 16000, // Sample rate for the audio file
    });

    recorderRef.current.startRecording();
  };

  // Stop recording and save the WAV audio
  const stopRecording = async () => {
    recorderRef.current.stopRecording(async () => {
      const blob = recorderRef.current.getBlob();
      setAudioFiles((prevFiles) => [...prevFiles, blob]);
      setPromptIndex((prevIndex) => prevIndex + 1);
      setRecording(false);
    });
  };

  // Submit the password and audio files to the backend
  const handleSubmit = async () => {
    if (audioFiles.length < 3) {
      alert("Please complete all three voice recordings.");
      return;
    }

    const formData = new FormData();
    formData.append("password", password);
    audioFiles.forEach((file, index) => {
      formData.append(`audio_${index + 1}`, file, `audio_${index + 1}.wav`);
    });

    try {
      const response = await axios.post(
        "http://localhost:8084/api/voice-auth", // Make sure this is the correct endpoint
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          withCredentials: true,
        }
      );
      console.log("Response from server:", response.data);
    } catch (error) {
      console.error("Error submitting voice authentication:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-900 to-black text-white">
      {/* Header with logo */}
      <div className="absolute top-4 left-4 flex items-center">
        <img
          src="/assets/icons/bull_icon.png"
          alt="Bull Rider Logo"
          className="h-10 w-10 mr-2"
        />
        <h1 className="text-2xl font-bold">Bull Rider</h1>
      </div>

      {/* Sign-up form */}
      <div className="bg-white bg-opacity-10 p-8 rounded-lg shadow-lg max-w-md w-full">
        <h2 className="text-3xl font-semibold mb-6 text-center">Sign Up</h2>
        <div className="mb-4">
          <label className="block text-lg mb-2">Password</label>
          <input
            type="password"
            value={password}
            onChange={handlePasswordChange}
            className="w-full px-4 py-2 bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your password"
          />
        </div>

        {promptIndex < prompts.length ? (
          <div className="flex flex-col items-center">
            <button
              onClick={recording ? stopRecording : startRecording}
              className={`w-full py-2 mt-4 ${
                recording ? "bg-red-600" : "bg-blue-600 hover:bg-blue-700"
              } rounded-md text-lg font-semibold`}
            >
              {recording ? "Stop Recording" : "authVoice"}
            </button>
            <p className="mt-4 text-center text-gray-300">
              {prompts[promptIndex]}
            </p>
          </div>
        ) : (
          <button
            onClick={handleSubmit}
            className="w-full py-2 mt-4 bg-green-600 hover:bg-green-700 rounded-md text-lg font-semibold"
          >
            Submit
          </button>
        )}

        <p className="mt-4 text-center text-gray-300">
          When you are ready, click the button and say "Log me in" to set up
          your personal voice-based password.
        </p>
      </div>
    </div>
  );
};

export default SignUp;
