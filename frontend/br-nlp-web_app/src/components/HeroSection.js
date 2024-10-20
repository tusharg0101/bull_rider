// src/components/HeroSection.js

import React from "react";
import { Link } from "react-router-dom";

const HeroSection = () => {
  return (
    <section
      id="hero"
      className="h-screen flex flex-col items-center justify-center bg-gradient-to-b from-black via-gray-900 to-black text-white relative overflow-hidden"
    >
      {/* Decorative diffused gradient circles */}
      <div className="absolute -top-20 left-10 w-96 h-96 bg-gradient-to-r from-blue-500 to-purple-600 opacity-30 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-0 right-32 w-80 h-80 bg-gradient-to-r from-purple-500 to-pink-500 opacity-25 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute top-20 right-10 w-64 h-64 bg-gradient-to-r from-blue-500 to-green-400 opacity-20 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute -bottom-32 left-32 w-72 h-72 bg-gradient-to-r from-pink-500 to-orange-400 opacity-30 rounded-full blur-3xl animate-pulse"></div>

      <div className="text-center z-10">
        <h2 className="text-7xl font-extrabold text-transparent bg-clip-text text-gradient mb-4 tracking-wide drop-shadow-lg animate-fade-in">
          Welcome to Bull Rider
        </h2>
        <p className="text-xl mb-8 text-gray-300 animate-fade-in">
          Seamless blockchain transactions made easy.
        </p>
        <Link to="/signup">
          <button className="px-10 py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full text-lg font-semibold shadow-lg hover:scale-105 transition-transform duration-300 transform hover:shadow-xl">
            Get Started
          </button>
        </Link>
      </div>
    </section>
  );
};

export default HeroSection;
