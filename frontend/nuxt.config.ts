import process from 'node:process'

export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: true },
  modules: ['@nuxt/ui', '@nuxt/image', '@nuxt/eslint'],
  ui: {
    global: true,
    icons: ['mdi', 'heroicons', 'octicon'],
  },
  image: {
    dir: 'assets/images',
  },
  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL,
    },
  },
  eslint: {
    config: {
      standalone: false,
    },
  },
  css: ['~/assets/css/main.css'],
  app: {
    rootId: 'root',
  },
})
