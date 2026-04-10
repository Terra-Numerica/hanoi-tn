import { defineConfig } from 'vite';

export default defineConfig({
  base: '/hanoi-tn/', 
  root: '.',
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  },
  resolve: {
    alias: {
      'three': 'three',
    }
  }
});
