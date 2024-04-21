<script setup lang="ts">
import { useQueryClient } from '@tanstack/vue-query'
import {
  getOrganizationsGetByUsernameQueryKey,
  getOrganizationsReadQueryKey,
  useOrganizationsGetReviews,
  useOrganizationsPostReview,
  useUsersRequestApprovement,
} from '~/api'
import type { FormSubmitEvent } from '#ui/types'

const props = defineProps<{
  orgUsername: string
  orgId: string
  mainSceneId?: string
  title: string
  bio: string
  logoUrl?: string
  contacts: {
    phone?: string
    email?: string
    website?: string
    documentsUrl?: string
  }
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

const { data: reviews } = useOrganizationsGetReviews(props.orgId)

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
const reviewFormDisabled = computed(() => sendReview.isPending.value)

function handleSubmit(event: FormSubmitEvent<{ feedback: string, rating: number }>) {
  sendReview.mutate({
    organizationId: props.orgId,
    data: {
      rate: event.data.rating,
      text: event.data.feedback,
    },
  })
}

const approveStudentOpen = ref(false)
const approveState = reactive({
  files: FileList,
})

const requestApprovement = useUsersRequestApprovement()

const approveFormDisabled = computed(() => requestApprovement.isPending.value)

function handleApproveSubmit(event: FormSubmitEvent<{ files: FileList }>) {
  requestApprovement.mutate({
    organizationId: props.orgId,
    data: {
      upload_file_obj: event.data.files.length > 0 ? event.data.files[0] : undefined,
    },
  }, {
    onSuccess() {
      approveStudentOpen.value = false
    },
  })
}
</script>

<template>
  <UContainer>
    <Card class="dark:bg-neutral-900 bg-neutral-50">
      <OrganizationPanorama v-if="mainSceneId" :org-username="orgUsername" :org-id="orgId" :main-scene-id="mainSceneId" />
      <div class="px-4 flex py-4 justify-between items-start">
        <div class="flex justify-between gap-5 items-end">
          <div v-if="logoUrl" class="w-20 h-1 relative">
            <UAvatar
              class="absolute bottom-0 box-content border-4 dark:border-neutral-900 border-neutral-50"
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
          <UButton
            v-if="!canReview"
            icon="i-heroicons-chat-bubble-left-ellipsis"
            @click="$emit('wantChatClick')"
          >
            Написать студентам
          </UButton>
          <UButton
            v-if="me?.role === 'admin' || me?.role === 'moderator'"
            variant="outline"
            :to="`/${orgUsername}/edit`"
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
          <UButton
            v-if="me?.student_approvement?.status !== 'approved'"
            variant="outline"
            color="yellow"
            @click="approveStudentOpen = true"
          >
            Я студент
          </UButton>
        </div>
      </div>
    </Card>
    <div class="grid grid-cols-3 gap-4 mt-4">
      <Card class="p-4 self-start">
        <h3 class="font-medium text-lg mb-2">
          Контакты
        </h3>
        <div class="flex flex-col gap-1">
          <UButton v-if="contacts.website" icon="i-heroicons-globe-alt" variant="link" :to="contacts.website" target="_blank">
            {{ contacts.website }}
          </UButton>
          <UButton v-if="contacts.email" icon="i-heroicons-envelope" variant="link" :to="`mailto:${contacts.email}`" target="_blank">
            {{ contacts.email }}
          </UButton>
          <UButton v-if="contacts.phone" icon="i-heroicons-phone" variant="link" :to="`tel:${contacts.phone}`" target="_blank">
            {{ contacts.phone }}
          </UButton>
          <UButton v-if="contacts.documentsUrl" icon="i-heroicons-document-text" variant="link" :to="contacts.documentsUrl" target="_blank">
            Документы
          </UButton>
        </div>
      </Card>
      <Card v-if="reviews" class="p-4 col-span-2">
        <h3 class="font-medium text-lg mb-2">
          Отзывы
        </h3>
        <div v-if="reviews.data.length > 0" class="flex flex-col gap-2">
          <div v-for="review in reviews.data" :key="review.id" class="p-4 flex flex-col gap-2 border-b dark:border-gray-700 last:border-0">
            <div class="flex justify-between">
              <Rating readonly :model-value="review.rate" size="sm" />
              <p class="italic text-md">
                {{ review.anonymous_name }}
                {{ review.mine && '(это вы)' }}
              </p>
            </div>
            <p>{{ review.text }}</p>
            <div class="flex justify-between">
              <UButton :icon="review.liked_by_me ? 'i-mdi-heart' : 'i-mdi-heart-outline'" color="red" variant="ghost" :label="review.likes.toString()" />
              <date class="text-sm opacity-60">
                {{ new Date(review.at).toLocaleDateString("ru-RU") }}
              </date>
            </div>
          </div>
        </div>
        <div v-else class="w-full my-auto flex items-center justify-center">
          <span class="opacity-40 text-lg">
            Здесь ещё нет отзывов
          </span>
        </div>
      </Card>
      <USkeleton v-else class="col-span-2 h-full min-[80px]" />
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
    <UModal v-model="approveStudentOpen">
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
              {{ title }}
            </h3>
            <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1" @click="approveStudentOpen = false" />
          </div>
        </template>
        <UForm :state="approveState" class="flex flex-col gap-2" @submit="handleApproveSubmit">
          <p>Приложите подтверждающие документы, чтобы получить доступ к возможностям студента вуза.</p>
          <UFormGroup label="Загрузить документы">
            <UInput
              name="files"
              type="file"
              @change="file => approveState.files = file"
            />
          </UFormGroup>
          <div class="flex gap-2">
            <UButton class="self-start" type="submit" :disabled="approveFormDisabled">
              Отправить на проверку
            </UButton>
            <UButton variant="outline" class="self-start" @click="approveStudentOpen = false">
              Отменить
            </UButton>
          </div>
        </UForm>
      </UCard>
    </UModal>
  </UContainer>
</template>
