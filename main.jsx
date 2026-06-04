import { createRoot } from "react-dom/client";
import App from "./app.jsx";

/**
 * Artifact-compatible storage for local dev (localStorage).
 * Matches the API used in app.jsx store adapter: get/set/delete/list.
 */
if (!window.storage) {
  window.storage = {
    async get(key) {
      const value = localStorage.getItem(key);
      if (value === null) return null;
      return { value };
    },
    async set(key, value) {
      localStorage.setItem(key, typeof value === "string" ? value : String(value));
    },
    async delete(key) {
      localStorage.removeItem(key);
    },
    async list(prefix) {
      const keys = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith(prefix)) keys.push(key);
      }
      return { keys };
    },
  };
}

createRoot(document.getElementById("root")).render(<App />);
