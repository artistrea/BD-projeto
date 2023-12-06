/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.svelte"],
  theme: {
    extend: {
      textColor: {
        text: "rgba(var(--rgb-text), var(--tw-text-opacity, 1))",
        background: "rgba(var(--rgb-background), var(--tw-text-opacity, 1))",
        primary: "rgba(var(--rgb-primary), var(--tw-text-opacity, 1))",
        secondary: "rgba(var(--rgb-secondary), var(--tw-text-opacity, 1))",
        accent: "rgba(var(--rgb-accent), var(--tw-text-opacity, 1))",
      },
      backgroundColor: {
        text: "rgba(var(--rgb-text), var(--tw-bg-opacity, 1))",
        background: "rgba(var(--rgb-background), var(--tw-bg-opacity, 1))",
        primary: "rgba(var(--rgb-primary), var(--tw-bg-opacity, 1))",
        secondary: "rgba(var(--rgb-secondary), var(--tw-bg-opacity, 1))",
        accent: "rgba(var(--rgb-accent), var(--tw-bg-opacity, 1))",
      },
      colors: {
        text: "rgb(var(--rgb-text))",
        background: "rgb(var(--rgb-background))",
        primary: "rgb(var(--rgb-primary))",
        secondary: "rgb(var(--rgb-secondary))",
        accent: "rgb(var(--rgb-accent))",
      },
    },
  },
  plugins: [],
};
