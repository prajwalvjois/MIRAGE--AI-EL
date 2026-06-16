import path from 'path';
import { defineConfig, build } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig(() => {
  return {
    build: {
      outDir: 'dist',
      emptyOutDir: true,
      rollupOptions: {
        input: {
          background: path.resolve(__dirname, 'src/background.ts'),
          popup: path.resolve(__dirname, 'popup.html'),
        },
        output: {
          entryFileNames: '[name].js',
          assetFileNames: '[name][extname]',
          format: 'es'
        },
      },
    },
    plugins: [
      react(),
      tailwindcss(),
      {
        name: 'build-content',
        async closeBundle() {
          await build({
            configFile: false,
            plugins: [react(), tailwindcss()],
            build: {
              outDir: 'dist',
              emptyOutDir: false,
              rollupOptions: {
                input: {
                  content: path.resolve(__dirname, 'src/content.tsx'),
                },
                output: {
                  entryFileNames: '[name].js',
                  assetFileNames: 'content-style[extname]',
                  format: 'iife'
                },
              },
            },
          });
        }
      }
    ]
  };
});
