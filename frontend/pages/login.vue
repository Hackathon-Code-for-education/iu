<template>
  <UContainer class="flex items-center justify-center">
    <Card class="py-4 px-8 m-auto">
      <h1 class="text-center text-2xl">
        Авторизация
      </h1>
      <div class="flex flex-col gap-2 mt-4 w-[250px]">
        <UButton icon="i-heroicons-user" color="gray" size="xl">
          Войти как абитуриент
        </UButton>
        <UButton icon="i-heroicons-academic-cap" color="gray" size="xl">
          Войти как студент
        </UButton>
        <UButton icon="i-heroicons-building-office-2" color="gray" size="xl">
          Войти как ВУЗ
        </UButton>
      </div>
    </Card>
  </UContainer>
</template>
