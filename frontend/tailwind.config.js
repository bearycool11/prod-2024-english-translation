/** @type {import('tailwindcss').Config} */
export default {
  content: [
    'node_modules/flowbite-vue/**/*.{js,jsx,ts,tsx,vue}',
    'node_modules/flowbite/**/*.{js,jsx,ts,tsx}',
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}",
  ],
  theme: {
    fontFamily: {
      'sans': ['Golos Text', 'Inter', 'Segoe UI']
    },
    extend: {},
  },
  darkMode: 'class',
  plugins: [
    // eslint-disable-next-line no-undef
    require('flowbite/plugin')
  ],
}

