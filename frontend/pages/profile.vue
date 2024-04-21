<script lang="ts" setup>
import { useQueryClient } from '@tanstack/vue-query'
import { useOrganizationsRead, useUsersLogout } from '~/api'

const queryClient = useQueryClient()
const { me, loggedIn } = useMe()

watch(loggedIn, (newLoggedIn) => {
  if (newLoggedIn === false)
    navigateTo('/login')
}, { immediate: true })

const approvementOrganizationId = computed(() => me.value?.student_approvement?.organization_id ?? '')
const suspendApprovementOrganizationFetching = computed(() => approvementOrganizationId.value === '')

const {
  data: org,
  // isLoading: orgLoading,
  // error: orgError,
} = useOrganizationsRead(approvementOrganizationId, { query: { suspense: suspendApprovementOrganizationFetching } })

const logout = useUsersLogout()

function handleLogout() {
  logout
    .mutateAsync()
    .then(() => {
      queryClient.clear()
      queryClient.invalidateQueries()
    })
}
</script>

<template>
  <UContainer>
    <div v-if="!me">
      <USkeleton class="w-[300px] h-[200px] rounded-xl" />
    </div>

    <div v-else class="grid grid-cols-3 gap-4">
      <Card class="p-6">
        <h3>Имя: {{ me.name }}</h3>
        <UButton :loading="logout.isPending.value" icon="i-octicon-sign-out-16" variant="outline" color="red" @click="handleLogout">
          Выйти
        </UButton>
      </Card>
      <Card v-if="!me.student_approvement">
        Подтвердите статуса студента
      </Card>
      <Card v-else-if="me.student_approvement.status === 'approved'" class="p-4">
        <h3 class="font-medium text-lg flex items-center gap-2">
          <UIcon class="text-green-500 text-[24px]" name="i-octicon-verified-24" />
          Статус студента подтверждён
        </h3>
        <div v-if="org">
          {{ org.data.name }}
        </div>
      </Card>
    </div>
  </UContainer>
</template>
