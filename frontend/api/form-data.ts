import type { MaybeRef } from 'vue'
import type { BodyFilesUploadFile } from '~/api/__generated__'

export function customFormData(body: MaybeRef<BodyFilesUploadFile>): FormData {
  const formData = new FormData()
  formData.append('upload_file_obj', unref(body).upload_file_obj)
  return formData
}
