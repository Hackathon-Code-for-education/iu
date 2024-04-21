import antfu from '@antfu/eslint-config'
import nuxt from './.nuxt/eslint.config.mjs'

export default antfu(
  {
    ignores: ['api/__generated__.ts'],
    formatters: true,
    typescript: true,
    vue: true,
  },
  nuxt,
)
