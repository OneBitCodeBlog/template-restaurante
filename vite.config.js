import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  build: {
    rolldownOptions: {
      input: {
        main: fileURLToPath(new URL('./index.html', import.meta.url)),
        styleguide: fileURLToPath(new URL('./styleguide.html', import.meta.url)),
      },
    },
  },
});
