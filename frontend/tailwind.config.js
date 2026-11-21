/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#E85D75',
        cream: '#F5F0EB',
        teal: '#4A90A4',
        background: '#FFFFFF',
        surface: '#FFF5FA',
        surface2: '#E8E8E8',
        border: '#E5E5E5',
        muted: '#1A1A1A',
        text: '#2D2D2D',
      },
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
      },
      borderRadius: {
        sm: '3px',
        md: '5px',
        lg: '6px',
        xl: '8px',
        '2xl': '10px',
        '3xl': '12px',
        '4xl': '13px',
        '5xl': '16px',
        full: '999px',
      },
      boxShadow: {
        sm: '0 1px 3px #0000001a, 0 1px 2px #0000000f',
        md: '0 1px 4px #00000040',
        lg: '0 2px 10px #0000001a',
      },
      transitionDuration: {
        DEFAULT: '150ms',
        200: '200ms',
        300: '300ms',
      },
      transitionTimingFunction: {
        ease: 'ease',
        cubic: 'cubic-bezier(.4,0,.2,1)',
        easeOut: 'cubic-bezier(.22,1,.36,1)',
      },
    },
  },
  plugins: [],
}
