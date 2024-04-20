<script setup lang="ts">
import { createError, useRoute } from '#app'
import { useChattingJoinDialog, useChattingUpdateQueue, useOrganizationsGetByUsername } from '~/api'

const route = useRoute()
const {
  data: org,
  error: queryError,
  isLoading,
} = useOrganizationsGetByUsername((route.params.org), { query: { retry: 0 } })
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
const joinDialog = useChattingJoinDialog()

function handleWantChatClick() {
  if (!org)
    return

  chatModalOpen.value = true
}

const studentsOnline = ref(0)
const repeatTimeout = ref < any > (null)

watch(chatModalOpen, (isOpen) => {
  if (repeatTimeout.value)
    clearTimeout(repeatTimeout.value)

  if (isOpen && org.value?.data) {
    updateChattingQueue
      .mutateAsync({ organizationId: org.value.data.id })
      .then((res) => {
        const resp = res.data
        if (resp.type === 'join_dialog') {
          //
          joinDialog
            .mutateAsync({ data: { dialog_pair: resp.dialog } })
            .then((res) => {
              const resp = res.data
              navigateTo(`/chats/${resp.id}`)
            })
        }
        else {
          studentsOnline.value = resp.queue_students_online
          const timeoutId = setTimeout(() => {}, 500)
          repeatTimeout.value = timeoutId
        }
      })
  }

  return () => {}
}, { immediate: true })
</script>

<template>
  <ErrorPage v-if="error" :error="error" />
  <OrganizationPage
    v-else-if="org"
    :title="org.data.name"
    bio="Example."
    @want-chat-click="handleWantChatClick"
  />
  <UContainer v-else-if="isLoading">
    <USkeleton class="w-full h-[300px] rounded-xl" />
  </UContainer>
  <UModal v-model="chatModalOpen">
    <div class="p-4">
      Студентов онлайн: {{ studentsOnline }}
    </div>
  </UModal>
</template>
