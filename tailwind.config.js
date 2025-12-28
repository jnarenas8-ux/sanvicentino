
/** @type {import('tailwindcss').Config} */
export default {
   content: ["./**/*.{html,js,py,jsx,ts,vue}", "./app/templates/**/*.{html,js}", "./app/static/js/**/*.js"],
    theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#00b8ff',
          600: '#009fe6'
        }
      },
      keyframes: {
        'fade-slide': {
          '0%':   { transform: 'translateY(100%)',  opacity: '0' },
          '8%':   { transform: 'translateY(0)',     opacity: '1' },
          '33%':  { transform: 'translateY(0)',     opacity: '1' },
          '41%':  { transform: 'translateY(-100%)', opacity: '0' },
          '100%': { transform: 'translateY(-100%)', opacity: '0' }
        }
      },
      animation: {
        'fade-slide': 'fade-slide 12s ease-in-out infinite'
      }
    }
  },
   
   plugins: [],
 }