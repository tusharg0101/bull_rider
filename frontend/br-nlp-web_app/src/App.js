// App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes, useLocation } from "react-router-dom";
import "./App.css";
import Header from "./components/Header";
import HeroSection from "./components/HeroSection";
import Footer from "./components/Footer";
import SignUp from "./pages/SignUp";
import LandingPage from "./pages/LandingPage";
import Profile from "./pages/Profile";
import Contacts from "./pages/Contacts"; // Import the Contacts component

function AppWrapper() {
  const location = useLocation();
  
  // Hide header on specific pages
  const hideHeaderPages = ["/profile", "/contacts", "/login"];
  const isHeaderVisible = !hideHeaderPages.includes(location.pathname);

  return (
    <div className="bg-discord-gray text-white min-h-screen flex flex-col">
      {/* Render Header only if it's not a hidden page */}
      {isHeaderVisible && <Header />}

      <main className="flex-grow">
        <Routes>
          <Route path="/" element={<HeroSection />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<LandingPage />} /> {/* Login page */}
          <Route path="/profile" element={<Profile />} />
          <Route path="/contacts" element={<Contacts />} />
        </Routes>
      </main>

      <Footer />
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppWrapper />
    </Router>
  );
}

export default App;
