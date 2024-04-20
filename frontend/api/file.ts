export function getFileUrl(fileId: string) {
  const config = useRuntimeConfig()
  return `${config.public.apiUrl}/static/${fileId}`
}
