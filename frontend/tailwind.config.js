/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        nb: {
          bg:     '#E8E8E8',
          card:   '#FFFFFF',
          yellow: '#FDE047',
          orange: '#FB923C',
          red:    '#F87171',
          pink:   '#FF4081',
          'pink-light': '#FFD6E5',
          purple: '#C084FC',
          blue:   '#60A5FA',
          cyan:   '#22D3EE',
          green:  '#4ADE80',
          lime:   '#A3E635',
          text:   '#000000',
          muted:  '#555555',
        },
      },
      boxShadow: {
        nb:        '4px 4px 0px 0px #000000',
        'nb-sm':   '2px 2px 0px 0px #000000',
        'nb-lg':   '6px 6px 0px 0px #000000',
        'nb-xl':   '8px 8px 0px 0px #000000',
        'nb-pink': '4px 4px 0px 0px #FF4081',
      },
      borderRadius: {
        nb: '5px',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
