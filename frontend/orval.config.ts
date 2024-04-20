import { defineConfig } from 'orval'

export default defineConfig({
  api: {
    input: {
      target: 'http://10.91.13.230:8000/openapi.json',
      validation: false,
    },
    output: {
      mode: 'single',
      target: './api/__generated__.ts',
      client: 'vue-query',
      override: {
        operations: {
          files_upload_file: {
            formData: {
              path: './api/form-data.ts',
              name: 'customFormData',
            },
          },
        },
      },
    },
  },
})
