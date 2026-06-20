/// <reference types="vitest/config" />
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// The dev server proxies /api -> the backend so the browser talks to one origin.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  // Vitest = unit tests in src/ only. The Playwright e2e/ specs (also *.spec.ts)
  // are run by `npm run e2e`, not vitest — exclude them so vitest doesn't try
  // to collect a browser test.
  test: {
    include: ["src/**/*.{test,spec}.{ts,tsx}"],
  },
});
