<script setup lang="ts">
import { createError, useRoute } from '#app'
import { useChattingUpdateQueue, useOrganizationsGetByUsername } from '~/api'
import { getFileUrl } from '~/api/file'

const route = useRoute()
const {
  data: org,
  error: queryError,
  isLoading,
} = useOrganizationsGetByUsername((route.params.org as string), { query: { retry: 0 } })
const error = computed(() => {
  const err = queryError.value
  if (err && err.response?.status === 404) {
    return createError({
      statusCode: 404,
      statusMessage: 'Организация не найдена',
    })
  }
  return null
})

const chatModalOpen = ref(false)
const updateChattingQueue = useChattingUpdateQueue()

function handleWantChatClick() {
  if (!org)
    return

  chatModalOpen.value = true
}

const studentsOnline = ref(0)
const keepaliveChatQueueInterval = ref<any>(null)

function startKeepaliveChatQueue(orgId: string) {
  if (keepaliveChatQueueInterval.value)
    clearInterval(keepaliveChatQueueInterval.value)

  const start = () => {
    updateChattingQueue
      .mutateAsync({ organizationId: orgId })
      .then((res) => {
        const resp = res.data
        if (resp.type === 'join_dialog')
          navigateTo({ path: '/chats', query: { chat: resp.dialog_id } })
        else
          studentsOnline.value = resp.queue_students_online
      })
  }

  keepaliveChatQueueInterval.value = setInterval(start, 1500)
  start()
}

watch(chatModalOpen, (isOpen, _, onCleanup) => {
  if (isOpen && org.value?.data)
    startKeepaliveChatQueue(org.value.data.id)

  onCleanup(() => {
    clearInterval(keepaliveChatQueueInterval.value)
  })
}, { immediate: true })
</script>

<template>
  <ErrorPage v-if="error" :error="error" />
  <OrganizationPage
    v-else-if="org"
    :org-username="org.data.username"
    :org-id="org.data.id"
    :main-scene-id="org.data.main_scene || undefined"
    :title="org.data.name"
    :bio="org.data.region_name ?? '—'"
    :logo-url="org.data.logo ? getFileUrl(org.data.logo) : undefined"
    :contacts="{
      phone: org.data.contacts?.phone ?? undefined,
      email: org.data.contacts?.email ?? undefined,
      website: org.data.contacts?.website ?? undefined,
    }"
    @want-chat-click="handleWantChatClick"
  />
  <UContainer v-else-if="isLoading">
    <USkeleton class="w-full h-[300px] rounded-xl" />
  </UContainer>
  <UModal v-model="chatModalOpen">
    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
            Чат со студентом
          </h3>
          <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1" @click="chatModalOpen = false" />
        </div>
      </template>
      <div class="flex gap-2 items-center">
        <span class="live-circle" />
        Студентов онлайн: {{ studentsOnline }}
      </div>
    </UCard>
  </UModal>
</template>

<style scoped>
@keyframes live-circle-anim {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  80%,
  100% {
    transform: scale(3);
    opacity: 0;
  }
}

.live-circle {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: inline-block;
  background-color: #00c853;
}

.live-circle::before {
  content: '';
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: #00c853;
  animation: live-circle-anim 1.25s infinite;
  animation-timing-function: ease-in-out;
}
</style>
