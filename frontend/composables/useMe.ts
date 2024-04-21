import type { AxiosError } from 'axios'
import { useUsersGetMe } from '~/api'

export default function () {
  const toast = useToast()
  const { data, isLoading: meLoading, error: originalError } = useUsersGetMe({
    query: {
      retry(failureCount, error) {
        if (isAuthError(error))
          return false
        return failureCount < 3
      },
    },
  })

  const meError = computed(() => {
    const err = originalError.value
    if (err && isAuthError(err))
      return null
    return err
  })
  const me = computed(() => data.value?.data ?? null)
  const loggedIn = computed(() => {
    if (!meLoading.value && me.value)
      return true
    else if (meLoading.value)
      return null
    return false
  })

  watch(meError, (newError) => {
    if (newError) {
      toast.add({
        id: 'me_error',
        title: 'Не удалось получить информацию о текущем пользователе',
        color: 'red',
      })
    }
  })

  return {
    me,
    meLoading,
    meError,
    loggedIn,
  }
}

function isAuthError(error: AxiosError) {
  return (error.response?.status && (error.response.status === 401 || error.response.status === 403))
}
