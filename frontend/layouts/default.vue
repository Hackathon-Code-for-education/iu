<script setup lang="ts">
const { me, meLoading } = useMe()
</script>

<template>
  <div class="py-4">
    <header>
      <UContainer>
        <Card class="px-16 py-2 flex mb-4 items-center justify-between">
          <UHorizontalNavigation
            :links="[
              { label: 'Главная', to: '/' },
              { label: 'ВУЗы', to: '/orgs' },
              { label: 'Чаты', to: '/chats' },
            ]"
          />
          <div class="flex items-center">
            <UButton v-if="meLoading" loading variant="outline" label="Профиль" />
            <NuxtLink v-else-if="me" to="/profile">
              <UButton icon="i-heroicons-user-circle" variant="outline" label="Профиль" />
            </NuxtLink>
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
