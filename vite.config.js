import { fileURLToPath, URL } from "node:url";
import { defineConfig, loadEnv } from "vite"; // Added loadEnv here
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";
export default defineConfig(({ mode }) => {
    // Load env file based on the current mode (development, production, etc.)
    const env = loadEnv(mode, process.cwd(), '');

    const targetUrl = env.VITE_API_URL || "http://localhost:8080/";

    return {
        plugins: [vue(), vueDevTools()],
        server: {
            proxy: {
                "/api": {
                    target: targetUrl,
                    changeOrigin: true,
                    rewrite: (p) => p.replace(/^\/api/, ""),
                },
            }
        },
        resolve: {
            alias: {
                "@": fileURLToPath(new URL("./src", import.meta.url)),
            },
        },
    };
});
