import process from 'node:process'

export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxt/ui', '@nuxtjs/tailwindcss', '@nuxt/image'],
  tailwindcss: {},
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
})
