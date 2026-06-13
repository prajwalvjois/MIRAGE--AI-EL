import path from 'path';
import { defineConfig, build } from 'vite';

export default defineConfig(() => {
  return {
    build: {
      outDir: 'dist',
      emptyOutDir: true,
      rollupOptions: {
        input: {
          background: path.resolve(__dirname, 'src/background.ts'),
        },
        output: {
          entryFileNames: '[name].js',
          format: 'iife'
        },
      },
    },
    plugins: [
      {
        name: 'build-content',
        async closeBundle() {
          await build({
            configFile: false,
            build: {
              outDir: 'dist',
              emptyOutDir: false,
              rollupOptions: {
                input: {
                  content: path.resolve(__dirname, 'src/content.ts'),
                },
                output: {
                  entryFileNames: '[name].js',
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
