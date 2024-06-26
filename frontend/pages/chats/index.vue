<script lang="ts" setup>
import { useQueryClient } from '@tanstack/vue-query'
import { getChattingGetMyDialogsQueryKey, useChattingGetMyDialogs, useChattingPushMessage } from '~/api'
import type { Message } from '~/components/Chat.vue'

const client = useQueryClient()
const {
  data: chats,
  error,
  isLoading,
} = useChattingGetMyDialogs({ query: { refetchInterval: 500 } })
const route = useRoute()
const chatId = ref<string | null>(null)

watch(() => route.fullPath, () => {
  chatId.value = route.query.chatId as string | null ?? null
}, { immediate: true })

const { me, loggedIn } = useMe()
const sendMessage = useChattingPushMessage()
const draftMessages = ref<Record<string, string | undefined>>({})

watch(loggedIn, (newLoggedIn) => {
  if (newLoggedIn === false)
    return navigateTo({ path: '/login' })
}, { immediate: true })

const selectedChat = computed<{ id: string, title: string, messages: Message[] } | null>(() => {
  const selected = chats.value?.data.find(({ id }) => id === chatId.value) ?? null

  if (!selected)
    return null

  return {
    id: selected.id,
    title: selected.title ?? '—',
    messages: selected.messages.map(m => ({
      id: m.id,
      date: new Date(m.at),
      content: m.text,
      // @todo
      incoming: me.value?.id !== m.user_id,
    })),
  }
})

function handleSelectChat(newChatId: string | null) {
  navigateTo({ query: { chatId: newChatId } })
}

function handleSelectedChatInput(value: string) {
  if (!selectedChat.value)
    return

  draftMessages.value = {
    ...draftMessages.value,
    [selectedChat.value.id]: value,
  }
}

function handleSendMessage() {
  if (sendMessage.isPending.value)
    return

  if (!selectedChat.value)
    return

  const message = draftMessages.value[selectedChat.value.id]?.trim() ?? ''
  if (!message)
    return

  const chatId = selectedChat.value.id

  sendMessage.mutateAsync({ params: {
    dialog_id: selectedChat.value.id,
    message,
  } })
    .then(() => {
      draftMessages.value = {
        ...draftMessages.value,
        [chatId]: undefined,
      }
    })
    .finally(() => {
      return client.invalidateQueries({
        queryKey: getChattingGetMyDialogsQueryKey(),
      })
    })
}
</script>

<template>
  <UContainer class="w-full flex-1">
    <div v-if="error">
      <h2 class="text-red-500 text-center text-2xl">
        Произошла ошибка при загрузке чатов
      </h2>
    </div>
    <Card v-else-if="!(chats?.data.length)" class="py-8 flex items-center justify-center">
      <span class="text-lg text-center opacity-65">
        Здесь появятся ваши чаты
      </span>
    </Card>
    <Card v-else class="flex min-h-[calc(100vh-110px)] justify-stretch">
      <div class="flex flex-col min-h-full basis-[300px] grow-0 shrink-0 border-r dark:border-gray-700 border-gray-200">
        <template v-if="isLoading">
          <USkeleton
            v-for="i in new Array(5).fill(null)"
            :key="i"
            class="basis-[80px] grow-0 shrink-0 rounded-none last:border-0 border-b"
          />
        </template>
        <div
          v-for="chat in (chats?.data ?? [])"
          :key="chat.id"
          class="basis-[80px] p-3 grow-0 shrink-0 rounded-none border-b dark:border-gray-700 border-gray-200 cursor-pointer"
          :class="[chat.id === selectedChat?.id && 'dark:bg-gray-900 bg-gray-100']"
          @click="handleSelectChat(chat.id)"
        >
          <h4 class="font-medium text-sm">
            {{ chat.title }}
          </h4>
        </div>
      </div>
      <USkeleton v-if="isLoading" class="grow rounded-none" />
      <div v-else-if="!selectedChat" class="flex items-center justify-center self-stretch w-full">
        <span class="text-gray-600 pointer-events-none text-lg">Выберите чат</span>
      </div>
      <Chat
        v-else
        :title="selectedChat.title"
        :messages="selectedChat.messages"
        :input="draftMessages[selectedChat.id] ?? ''"
        :input-disabled="sendMessage.isPending.value"
        @update:input="handleSelectedChatInput"
        @send="handleSendMessage"
      />
    </Card>
  </UContainer>
</template>
