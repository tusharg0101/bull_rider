import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import RecordRTC from "recordrtc";

const SignUp = () => {
  const [password, setPassword] = useState("");
  const [promptIndex, setPromptIndex] = useState(0);
  const [recording, setRecording] = useState(false);
  const [audioBlobs, setAudioBlobs] = useState([]);
  const recorderRef = useRef(null);
  const navigate = useNavigate(); // Call useNavigate at the top level

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

    recorderRef.current = new RecordRTC(stream, {
      type: "audio",
      mimeType: "audio/wav",
      recorderType: RecordRTC.StereoAudioRecorder,
      desiredSampRate: 16000,
    });

    recorderRef.current.startRecording();
  };

  // Stop recording and store the audio blob
  const stopRecording = async () => {
    recorderRef.current.stopRecording(() => {
      const blob = recorderRef.current.getBlob();
      setAudioBlobs((prevBlobs) => [...prevBlobs, blob]);
      setPromptIndex((prevIndex) => prevIndex + 1);
      setRecording(false);
    });
  };

  const handleSubmit = async () => {
    if (audioBlobs.length < 3) {
      alert("Please complete all three voice recordings.");
      return;
    }

    // Create a FormData object to send the password and audio files
    const formData = new FormData();
    formData.append("password", password);
    audioBlobs.forEach((blob, index) => {
      formData.append(`voice_${index + 1}`, blob, `voice_${index + 1}.wav`);
    });

    try {
      const response = await fetch(
        "http://localhost:8084/api/voice-auth/signup",
        {
          method: "POST",
          body: formData,
        }
      );

      if (response.ok) {
        const data = await response.json();
        console.log(data.message);
        navigate("/profile"); // Use navigate to redirect after successful signup
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
      }
    } catch (error) {
      console.error("Error submitting data:", error);
      alert("An error occurred while submitting data.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-900 to-black text-white">
      <div className="absolute top-4 left-4 flex items-center">
        <img
          src="/assets/icons/bull_icon.png"
          alt="Bull Rider Logo"
          className="h-10 w-10 mr-2"
        />
        <h1 className="text-2xl font-bold">Bull Rider</h1>
      </div>

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
              {recording ? "Stop Recording" : "Start Recording"}
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
