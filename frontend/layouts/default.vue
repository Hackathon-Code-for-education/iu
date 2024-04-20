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
            <NuxtLink to="/login">
              <UButton icon="i-octicon-sign-in-16" variant="outline">
                Войти
              </UButton>
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
