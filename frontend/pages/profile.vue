<script lang="ts" setup>
import { useQueryClient } from '@tanstack/vue-query'
import { useOrganizationsRead, useUsersGetMyReviews, useUsersLogout } from '~/api'

const queryClient = useQueryClient()
const { me, loggedIn } = useMe()
const { data: reviews } = useUsersGetMyReviews()

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
      <Card class="p-4">
        <h3 class="mb-2">
          Имя: {{ me.name }}
        </h3>
        <UButton :loading="logout.isPending.value" icon="i-octicon-sign-out-16" variant="outline" color="red" @click="handleLogout">
          Выйти
        </UButton>
      </Card>
      <Card v-if="!me.student_approvement" class="p-4 col-span-2">
        Подтвердите статус студента
      </Card>
      <Card v-else-if="me.student_approvement.status === 'approved'" class="p-4 col-span-2">
        <h3 class="font-medium text-lg flex items-center gap-2">
          <UIcon class="text-green-500 text-[24px]" name="i-octicon-verified-24" />
          Статус студента подтверждён
        </h3>
        <div v-if="org">
          {{ org.data.name }}
        </div>
      </Card>
      <Card class="p-4 col-span-3">
        <h3 class="mb-2">
          Мои отзывы:
        </h3>
        <div v-if="reviews" class="flex flex-col gap-2">
          <Card v-for="review in reviews.data" :key="review.id" class="p-4 flex flex-col gap-2">
            <div class="flex justify-between">
              <Rating disabled :model-value="review.rate" />
              <UButton
                :to="`/${review.organization_username}`"
                :label="review.organization_name"
                class="w-fit"
                variant="ghost"
              />
            </div>
            <div class="flex justify-between">
              <p>{{ review.text }}</p>
              <p>{{ new Date(review.at).toLocaleString("ru-RU") }}</p>
            </div>
          </Card>
        </div>
      </Card>
    </div>
  </UContainer>
</template>
