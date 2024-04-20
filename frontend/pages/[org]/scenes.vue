<script setup lang="ts">
import { createError, useRoute } from '#app'
import { useOrganizationsGetByUsername } from '~/api'

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
</script>

<template>
  <ErrorPage v-if="error" :error="error" />
  <ScenesEditPage
    v-else-if="org"
    :org-username="org.data.username"
    :org-id="org.data.id"
  />
  <UContainer v-else-if="isLoading">
    <USkeleton class="w-full h-[300px] rounded-xl" />
  </UContainer>
</template>
