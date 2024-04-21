<script setup lang="ts">
import { createError, useRoute } from '#app'
import { useOrganizationsGetByUsername } from '~/api'

const route = useRoute()
const orgUsername = route.params.org as string

const {
  data: org,
  error: queryError,
  isLoading,
} = useOrganizationsGetByUsername(orgUsername, { query: { retry: 0 } })

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
  <OrganizationEditHeader
    v-if="org"
    :org-username="orgUsername"
    :org-id="org.data.id"
  />
  <ScenesEditPage
    v-if="org"
    :org-username="orgUsername"
    :org-id="org.data.id"
  />
  <UContainer v-else-if="isLoading">
    <USkeleton class="w-full h-[300px] rounded-xl" />
  </UContainer>
</template>
