<template>
  <div>
    <header class="my-6">
      <UContainer>
        <Card class="px-16 py-2 flex items-center justify-between">
          <UHorizontalNavigation
            :links="[
              { label: 'Главная', to: '/' },
              { label: 'ВУЗы', to: '/orgs' },
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
