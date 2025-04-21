/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      './templates/**/*.html', // adjust if your templates are in a different folder
      './**/*.html',
      './forum/templates/**/*.html',
      './accounts/templates/**/*.html',
      './private_chat/templates/**/*.html',
    ],
    theme: {
      extend: {
        colors: {
          cyber: '#0ff',
          umbra: '#5b21b6',
        },
      },
    },
    darkMode: 'class',
    plugins: [],
  }
  
