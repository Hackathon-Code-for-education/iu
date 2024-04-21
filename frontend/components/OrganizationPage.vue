<script setup lang="ts">
defineProps<{
  orgUsername: string
  orgId: string
  mainSceneId?: string
  title: string
  bio: string
  logoUrl?: string
}>()

defineEmits<{
  wantChatClick: []
}>()

const { me } = useMe()
</script>

<template>
  <UContainer>
    <Card class="bg-neutral-900">
      <OrganizationPanorama v-if="mainSceneId" :org-username="orgUsername" :org-id="orgId" :main-scene-id="mainSceneId" />
      <div class="px-4 flex py-4 justify-between items-start">
        <div class="flex justify-between gap-5 items-end">
          <div v-if="logoUrl" class="w-20 h-1 relative">
            <UAvatar
              class="absolute bottom-0 box-content border-4 border-neutral-900"
              size="3xl"
              :src="logoUrl"
            />
          </div>
          <div>
            <h1 class="text-2xl font-medium line-clamp-1">
              {{ title }}
            </h1>
            <p class="text-neutral-500">
              {{ bio }}
            </p>
          </div>
        </div>
        <div class="flex flex-row gap-2 items-end flex-shrink-0">
          <UButton @click="$emit('wantChatClick')">
            Написать студентам
          </UButton>
          <UButton
            v-if="me?.role === 'admin' || me?.role === 'moderator'"
            variant="outline"
            :to="`/${orgUsername}/edit/scenes`"
            class="w-fit"
            icon="i-mdi-pencil"
          >
            Редактировать
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
      </Card>
      <Card class="p-4">
        <h3>Контакты</h3>
      </Card>
    </div>
  </UContainer>
</template>
