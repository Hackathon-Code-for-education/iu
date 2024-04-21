import { defineConfig } from 'orval'

export default defineConfig({
  api: {
    input: {
      target: 'http://localhost/api/openapi.json',
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
          organizations_import_organizations: {
            formData: {
              path: './api/form-data.ts',
              name: 'customFormData',
            },
          },
          users_request_approvement: {
            formData: {
              path: './api/form-data.ts',
              name: 'customFormDataDocuments',
            },
          },
        },
      },
    },
  },
})
