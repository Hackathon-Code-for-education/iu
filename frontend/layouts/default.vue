<script setup lang="ts">
import { useQueryClient } from '@tanstack/vue-query'
import { useUsersLogout } from '~/api'

const queryClient = useQueryClient()
const { me, meLoading } = useMe()
const logout = useUsersLogout({
  mutation: {
    onSuccess: () => {
      queryClient.clear()
      queryClient.invalidateQueries()
    },
  },
})
function handleLogout() {
  logout.mutate()
}
</script>

<template>
  <div class="py-4">
    <header>
      <UContainer>
        <Card class="px-4 py-2 flex mb-4 items-center justify-between">
          <UHorizontalNavigation
            :links="[
              { label: 'Главная', to: '/' },
              { label: 'ВУЗы', to: '/orgs' },
              { label: 'Чаты', to: '/chats' },
            ]"
          />
          <div class="flex items-center">
            <UButton v-if="meLoading" loading variant="outline" label="Профиль" />
            <UDropdown
              v-else-if="me"
              mode="hover"
              :items="[
                [{ label: 'Профиль', icon: 'i-heroicons-user-circle', href: '/profile' }],
                [{ label: 'Выйти', icon: 'i-heroicons-arrow-right-start-on-rectangle', click: handleLogout, disabled: logout.isPending.value }],
              ]"
            >
              <UButton color="white" label="Профиль" trailing-icon="i-heroicons-chevron-down-20-solid" />
            </UDropdown>
            <NuxtLink v-else to="/login">
              <UButton icon="i-octicon-sign-in-16" variant="outline" label="Войти" />
            </NuxtLink>
          </div>
        </Card>
      </UContainer>
    </header>
    <main>
      <slot />
    </main>
  </div>
</template>
