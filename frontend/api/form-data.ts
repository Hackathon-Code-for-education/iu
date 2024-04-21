import type { MaybeRef } from 'vue'

export function customFormData(body: MaybeRef<{ upload_file_obj: Blob }>): FormData {
  const formData = new FormData()
  formData.append('upload_file_obj', unref(body).upload_file_obj)
  return formData
}

export function customFormDataDocuments(body: MaybeRef<{ upload_file_obj?: Blob | null }>): FormData | undefined {
  const file = unref(body).upload_file_obj
  if (file) {
    const formData = new FormData()
    formData.append('upload_file_obj', file)
    return formData
  }
  return undefined
}
