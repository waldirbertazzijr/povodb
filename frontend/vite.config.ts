import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import { fileURLToPath } from "node:url";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            "@": path.resolve(
                path.dirname(fileURLToPath(import.meta.url)),
                "./src",
            ),
        },
    },
    server: {
        port: 3000,
        host: true,
        hmr: {
            clientPort: 3000,
        },
        allowedHosts: ["app.povodb.test"],
    },
});
