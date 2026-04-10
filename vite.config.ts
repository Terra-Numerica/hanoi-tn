import { defineConfig } from 'vite';

export default defineConfig({
  root: '.',
  publicDir: false,
  build: {
    outDir: 'dist',
  },
  resolve: {
    alias: {
      'three': 'three',
    }
  }
});
