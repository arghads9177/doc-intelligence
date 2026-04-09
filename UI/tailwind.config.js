/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./projects/doc-intelligence-ui/src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1f2937',
        secondary: '#6366f1',
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
        info: '#3b82f6',
      },
      spacing: {
        '128': '32rem',
      }
    },
  },
  plugins: [],
}
