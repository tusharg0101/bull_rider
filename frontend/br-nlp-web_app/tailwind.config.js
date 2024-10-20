module.exports = {
  purge: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        'discord-gray': '#2c2f33',  // Base color
        'discord-purple': '#5865F2', // Highlight purple
        'discord-blue': '#7289da',   // Highlight blue
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
