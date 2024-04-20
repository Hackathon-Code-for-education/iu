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
        </Card>
      </UContainer>
    </header>
    <main>
      <slot />
    </main>
  </div>
</template>
