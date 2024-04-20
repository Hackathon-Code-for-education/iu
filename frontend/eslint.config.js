import antfu from '@antfu/eslint-config'
import tailwindcss from 'eslint-plugin-tailwindcss'
import vueParser from 'vue-eslint-parser'
import nuxt from './.nuxt/eslint.config.mjs'

export default antfu(
  {
    ignores: ['api/__generated__.ts'],
    formatters: true,
  },
  {
    rules: {
      'tailwindcss/classnames-order': 'error',
      'tailwindcss/enforces-negative-arbitrary-values': 'error',
      'tailwindcss/enforces-shorthand': 'error',
      'tailwindcss/migration-from-tailwind-2': 'error',
      'tailwindcss/no-arbitrary-value': 'off',
      'tailwindcss/no-custom-classname': 'error',
      'tailwindcss/no-contradicting-classname': 'error',
      'tailwindcss/no-unnecessary-arbitrary-value': 'error',
    },
    plugins: { tailwindcss },
    files: ['*.vue'],
    languageOptions: {
      parser: vueParser,
    },
  },
  nuxt,
)
