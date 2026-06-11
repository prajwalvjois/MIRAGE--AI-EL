import path from 'path';
import { defineConfig } from 'vite';

export default defineConfig(() => {
  return {
    build: {
      outDir: 'dist',
      emptyOutDir: true,
      rollupOptions: {
        input: {
          background: path.resolve(__dirname, 'src/background.ts'),
          content: path.resolve(__dirname, 'src/content.ts'),
        },
        output: {
          entryFileNames: '[name].js',
          format: 'iife' // IIFE prevents ES Module strictness errors in Chrome content scripts
        },
      },
    },
  };
});
