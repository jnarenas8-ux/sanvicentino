 /** @type {import('tailwindcss').Config} */
export default {
   content: ["./src/**/*.{html,js}"],
    theme: {
    extend: {
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