<script setup lang="ts">
import { useQueryClient } from '@tanstack/vue-query'
import { getOrganizationsGetByUsernameQueryKey, getOrganizationsReadQueryKey, useOrganizationsPostReview } from '~/api'
import type { FormSubmitEvent } from '#ui/types'

const props = defineProps<{
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

const toast = useToast()
const queryClient = useQueryClient()
const { me } = useMe()
const reviewModalOpen = ref(false)
const reviewState = reactive({
  feedback: '',
  rating: 5,
})
const canReview = computed(() => !!(
  me.value
  && me.value.student_approvement?.status === 'approved'
  && me.value.student_approvement.organization_id === props.orgId
))
const reviewFormDisabled = computed(() => sendReview.isPending.value)

const sendReview = useOrganizationsPostReview({
  mutation: {
    onSuccess: () => {
      toast.add({ color: 'green', title: 'Отзыв отправлен!', icon: 'i-octicon-star-fill-24' })
      reviewModalOpen.value = false
      reviewState.feedback = ''
      reviewState.rating = 5
    },
    onError: () => {
      toast.add({ color: 'red', title: 'Произошла ошибка при отправке отзыва' })
    },
    onSettled: () => {
      queryClient.invalidateQueries({
        queryKey: getOrganizationsGetByUsernameQueryKey(props.orgUsername),
      })
      queryClient.invalidateQueries({
        queryKey: getOrganizationsReadQueryKey(props.orgId),
      })
    },
  },
})

function handleSubmit(event: FormSubmitEvent<{ feedback: string, rating: number }>) {
  sendReview.mutate({
    organizationId: props.orgId,
    data: {
      rate: event.data.rating,
      text: event.data.feedback,
    },
  })
}
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
            icon="i-mdi-pencil"
          >
            Редактировать
          </UButton>
          <UButton
            v-if="canReview"
            variant="outline"
            icon="i-octicon-star-24"
            color="yellow"
            @click="reviewModalOpen = true"
          >
            Оставить отзыв
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
    <UModal v-model="reviewModalOpen">
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
              {{ title }}
            </h3>
            <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1" @click="reviewModalOpen = false" />
          </div>
        </template>
        <UForm :state="reviewState" class="flex flex-col gap-2" @submit="handleSubmit">
          <Rating
            v-model="reviewState.rating"
            class="justify-center"
            :disabled="reviewFormDisabled"
          />
          <UFormGroup label="Ваш отзыв" required>
            <UTextarea
              v-model="reviewState.feedback"
              name="feedback"
              :rows="10"
              :disabled="reviewFormDisabled"
              placeholder="Расскажите всё самое важное и интересное, что должны знать абитуриенты..."
            />
          </UFormGroup>
          <div class="flex gap-2">
            <UButton class="self-start" type="submit" :disabled="reviewFormDisabled">
              Отправить отзыв
            </UButton>
            <UButton variant="outline" class="self-start" @click="reviewModalOpen = false">
              Отменить
            </UButton>
          </div>
        </UForm>
      </UCard>
    </UModal>
  </UContainer>
</template>
