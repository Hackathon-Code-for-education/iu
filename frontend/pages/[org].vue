<script setup lang="ts">
import logo from '~/assets/images/logo.jpg'

const route = useRoute()
</script>

<template>
  <UContainer>
    <Card class="bg-neutral-900">
      <NuxtImg src="bg.jpg" class="w-full h-auto max-h-[300px]" />
      <div class="px-12 flex py-4 justify-between items-start">
        <div class="flex justify-between gap-5 items-end">
          <div class="w-20 h-1 relative">
            <UAvatar
              class="absolute bottom-0 box-content border-4 border-neutral-900"
              :src="logo"
              size="3xl"
            />
          </div>
          <div>
            <h1 class="text-2xl font-medium">
              Университет Иннополис
            </h1>
            <p class="text-neutral-500">
              Example!
            </p>
          </div>
        </div>
        <div class="flex justify-between gap-2">
          <UButton>Буду поступать</UButton>
          <UButton variant="outline">
            Написать студентам
          </UButton>
        </div>
      </div>
    </Card>
    <div class="grid grid-cols-3 gap-4 mt-4">
      <Card class="p-4">
        <h3>Социальные сети</h3>
        <div class="flex flex-col gap-2">
          <UButton
            icon="i-mdi-telegram"
            size="sm"
            variant="ghost"
            color="gray"
            to="https://t.me/@universityinnopolis" target="_blank"
            label="Telegram"
          />
          <UButton
            icon="i-mdi-vk"
            size="sm"
            variant="ghost"
            color="gray"
            to="https://vk.com/innopolisu" target="_blank"
            label="ВКонтакте"
          />
        </div>
      </Card>
      <Card class="p-4">
        <h3>FAQ</h3>
        <div class="flex flex-col gap-2" />
      </Card>
    </div>
  </UContainer>
</template>
