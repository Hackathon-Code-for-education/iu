import { useChattingUpdateStudentsQueue } from '~/api'

export default function () {
  const { me } = useMe()

  const chatKeepaliveInterval = ref<any>(null)
  const state = ref<'idle' | 'stopping' | 'starting' | 'active'>('idle')
  const stateOut = computed(() => state.value)
  const sendKeepaliveChatting = useChattingUpdateStudentsQueue()

  const stopChatting = () => {
    if (state.value !== 'active')
      return

    if (chatKeepaliveInterval.value)
      clearInterval(chatKeepaliveInterval.value)

    // @todo Send request to stop.
    state.value = 'idle'
  }
  const startChatting = () => {
    if (state.value !== 'idle')
      return

    const studentApprovement = me.value?.student_approvement

    if (studentApprovement?.status !== 'approved')
      return

    const start = () => {
      sendKeepaliveChatting.mutate(
        { organizationId: studentApprovement.organization_id },
        {
          onSuccess: (data) => {
            state.value = 'active'
            if (data.data.type === 'join_dialog') {
              stopChatting()
              navigateTo({ path: `/chats`, query: { chatId: data.data.dialog_id } })
            }
          },
          onError: (err) => {
            console.error('Failed to start chatting.', err)
            state.value = 'idle'
          },
        },
      )
    }
    state.value = 'starting'
    start()
    chatKeepaliveInterval.value = setInterval(start, 1000)
  }

  return {
    state: stateOut,
    startChatting,
    stopChatting,
  }
}
